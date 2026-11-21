#!/usr/bin/env python3
"""Inspect the Astro dist/ output for SEO and Play UTM hygiene.

Runs `npm run build` when dist/ is missing or --rebuild is passed.
Checks every HTML page for title, meta description, canonical; walks internal
links; requires Vireault Play Store links to carry utm_source, utm_medium,
utm_campaign; reports approximate word counts for guide pages.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PLAY_HOST = "play.google.com"
PACKAGE = "com.vireault.app"


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u2019", "'")).strip()


def ld_types(block: dict) -> str:
    t = block.get("@type")
    return t if isinstance(t, str) else ""


def check_structured_data(rel: str, page_path: str, parser: "PageParser") -> list[str]:
    """JSON-LD hygiene for guides and the guides index; schema must match visible content."""
    problems: list[str] = []
    blocks: list[dict] = []
    for raw in parser.ld_blocks:
        try:
            data = json.loads(raw)
        except ValueError as e:
            problems.append(f"{rel}: invalid JSON-LD ({e})")
            continue
        blocks.extend(data if isinstance(data, list) else [data])
    by_type: dict[str, list[dict]] = {}
    for b in blocks:
        by_type.setdefault(ld_types(b), []).append(b)
    visible = parser.visible_text

    if "BreadcrumbList" not in by_type:
        problems.append(f"{rel}: missing BreadcrumbList JSON-LD")
    if is_guide_page(page_path):
        if "Article" not in by_type:
            problems.append(f"{rel}: missing Article JSON-LD")
        elif not by_type["Article"][0].get("image"):
            problems.append(f"{rel}: Article JSON-LD has no image")
    else:  # guides index
        lists = by_type.get("ItemList", [])
        if not lists:
            problems.append(f"{rel}: missing ItemList JSON-LD")
        else:
            urls = [e.get("url", "") for e in lists[0].get("itemListElement", [])]
            card_paths = [
                h.split("#", 1)[0].rstrip("/")
                for h in parser.links
                if re.search(r"/guides/[^/]+/?$", h)
            ]
            ld_paths = [urlparse(u).path.rstrip("/") for u in urls]
            seen: list[str] = []
            for cp in card_paths:  # footer/nav may repeat guide links; keep first occurrence
                if cp not in seen:
                    seen.append(cp)
            if seen != ld_paths:
                problems.append(f"{rel}: ItemList does not match visible guide cards/order")
    for q in by_type.get("FAQPage", []):
        entities = q.get("mainEntity", [])
        if not entities:
            problems.append(f"{rel}: FAQPage has no questions")
        for e in entities:
            for text in (e.get("name", ""), e.get("acceptedAnswer", {}).get("text", "")):
                if not text or norm(text) not in visible:
                    problems.append(f"{rel}: FAQPage text not visible on page: {text[:60]!r}")
    for h in by_type.get("HowTo", []):
        steps = h.get("step", [])
        if not steps:
            problems.append(f"{rel}: HowTo has no steps")
        for st in steps:
            text = st.get("text", "")
            if not text or norm(text) not in visible:
                problems.append(f"{rel}: HowTo step text not visible on page: {text[:60]!r}")
    for src, alt in parser.img_alts:
        if not (alt or "").strip():
            problems.append(f"{rel}: guide image {src} has no alt text")
    return problems


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title_parts: list[str] = []
        self.in_title = False
        self.in_body = False
        self.meta_description: str | None = None
        self.robots: str = ""
        self.canonical: str | None = None
        self.links: list[str] = []
        self.verification: str | None = None
        self.ld_blocks: list[str] = []
        self._in_ld = False
        self.img_alts: list[tuple[str, str | None]] = []
        self.text_chunks: list[str] = []
        self._skip_text = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = {k: (v or "") for k, v in attrs}
        if tag == "title":
            self.in_title = True
        elif tag == "body":
            self.in_body = True
        elif tag == "meta" and ad.get("name", "").lower() == "description":
            self.meta_description = ad.get("content") or ""
        elif tag == "meta" and ad.get("name", "").lower() == "google-site-verification":
            self.verification = ad.get("content") or ""
        elif tag == "img" and "/images/guides/" in ad.get("src", ""):
            self.img_alts.append((ad.get("src", ""), ad.get("alt")))
        elif tag == "meta" and ad.get("name", "").lower() == "robots":
            self.robots = (ad.get("content") or "").lower()
        elif tag == "link" and ad.get("rel", "").lower() == "canonical":
            self.canonical = ad.get("href") or ""
        elif tag == "a" and "href" in ad:
            self.links.append(ad["href"])
        elif tag in {"script", "style", "noscript"}:
            self._skip_text = True
            if tag == "script" and ad.get("type") == "application/ld+json":
                self._in_ld = True
                self.ld_blocks.append("")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        elif tag in {"script", "style", "noscript"}:
            self._skip_text = False
            self._in_ld = False

    def handle_data(self, data: str) -> None:
        if self._in_ld and self.ld_blocks:
            self.ld_blocks[-1] += data
        if self.in_title:
            self.title_parts.append(data)
        if self.in_body and not self._skip_text:
            self.text_chunks.append(data)

    @property
    def title(self) -> str:
        return "".join(self.title_parts).strip()

    @property
    def visible_text(self) -> str:
        return norm("".join(self.text_chunks))

    @property
    def word_count(self) -> int:
        text = re.sub(r"\s+", " ", "".join(self.text_chunks)).strip()
        return len(text.split()) if text else 0


def ensure_build(rebuild: bool) -> None:
    if rebuild or not DIST.exists():
        print("Building site (npm run build)...")
        subprocess.run(["npm", "run", "build"], cwd=ROOT, check=True)


def html_files() -> list[Path]:
    return sorted(p for p in DIST.rglob("*.html") if p.is_file())


def page_url_path(html: Path) -> str:
    rel = html.relative_to(DIST).as_posix()
    if rel == "404.html":
        return "/404"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    if rel.endswith(".html"):
        return "/" + rel[: -len(".html")] + "/"
    return "/" + rel


def resolve_internal(base_path: str, href: str, base_prefix: str) -> str | None:
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    parsed = urlparse(href)
    if parsed.scheme in {"http", "https"}:
        host = parsed.netloc or ""
        if "dixonchoi22.github.io" in host or "vireault.app" in host:
            path = parsed.path or "/"
            if base_prefix and path.startswith(base_prefix):
                path = path[len(base_prefix) :] or "/"
            return path.split("#", 1)[0].split("?", 1)[0]
        return None
    if href.startswith("//"):
        return None
    if href.startswith("/"):
        path = href
        if base_prefix and path.startswith(base_prefix):
            path = path[len(base_prefix) :] or "/"
        return path.split("#", 1)[0].split("?", 1)[0]
    base_dir = base_path if base_path.endswith("/") else base_path.rsplit("/", 1)[0] + "/"
    joined = str(Path(base_dir) / href)
    parts: list[str] = []
    for part in joined.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return "/" + "/".join(parts)


def path_exists(path: str) -> bool:
    clean = path.split("#", 1)[0].split("?", 1)[0]
    candidates = [
        DIST / clean.lstrip("/"),
        DIST / clean.lstrip("/").rstrip("/") / "index.html",
        DIST / (clean.lstrip("/").rstrip("/") + ".html"),
    ]
    if not clean or clean == "/":
        candidates.append(DIST / "index.html")
    return any(c.exists() for c in candidates)


def is_vireault_play(href: str) -> bool:
    parsed = urlparse(href)
    if PLAY_HOST not in (parsed.netloc or ""):
        return False
    qs = parse_qs(parsed.query)
    return qs.get("id", [None])[0] == PACKAGE or f"id={PACKAGE}" in href


def check_play_link(href: str) -> list[str]:
    if not is_vireault_play(href):
        return []
    problems: list[str] = []
    qs = parse_qs(urlparse(href).query)
    for key in ("utm_source", "utm_medium", "utm_campaign"):
        if key not in qs or not qs[key][0]:
            problems.append(f"missing {key}")
    src = (qs.get("utm_source") or [""])[0]
    med = (qs.get("utm_medium") or [""])[0]
    if src and src not in {"vireault-site", "web"}:
        problems.append(f"unexpected utm_source={src}")
    if med and med != "guide":
        problems.append(f"unexpected utm_medium={med}")
    return problems


def detect_base_prefix() -> str:
    index = DIST / "index.html"
    if not index.exists():
        return ""
    text = index.read_text(errors="ignore")
    m = re.search(r'rel="canonical"\s+href="([^"]+)"', text)
    if m and "/vireault-site" in m.group(1):
        return "/vireault-site"
    return ""


def is_guide_page(page_path: str) -> bool:
    parts = [p for p in page_path.split("/") if p]
    return len(parts) >= 2 and parts[0] == "guides"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rebuild", action="store_true", help="Force npm run build before checks")
    args = ap.parse_args()
    try:
        ensure_build(args.rebuild)
    except subprocess.CalledProcessError as e:
        print(f"BUILD FAILED: {e}", file=sys.stderr)
        return 1

    files = html_files()
    if not files:
        print("No HTML files in dist/", file=sys.stderr)
        return 1

    base_prefix = detect_base_prefix()
    errors: list[str] = []
    warnings: list[str] = []
    guide_words: list[tuple[str, int]] = []

    for html in files:
        rel = html.relative_to(DIST).as_posix()
        if rel == "404.html":
            continue
        raw = html.read_text(errors="ignore")
        parser = PageParser()
        parser.feed(raw)
        page_path = page_url_path(html)

        noindex = "noindex" in (parser.robots or "")
        if not parser.title:
            errors.append(f"{rel}: missing <title>")
        if noindex:
            # Legacy redirect stubs under public/ (and Astro privacy redirect) are noindex by design.
            warnings.append(f"{rel}: noindex stub skipped for meta/canonical/word-count rules")
        else:
            if not parser.meta_description:
                errors.append(f"{rel}: missing meta description")
            elif len(parser.meta_description) > 160:
                warnings.append(
                    f"{rel}: meta description length {len(parser.meta_description)} > 160"
                )
            if not parser.canonical:
                errors.append(f"{rel}: missing canonical")
            if (is_guide_page(page_path) and html.name == "index.html") or page_path == "/guides/":
                if not parser.verification:
                    errors.append(f"{rel}: missing google-site-verification meta")
                errors.extend(check_structured_data(rel, page_path, parser))
            # Only count Astro guide routes: dist/guides/<slug>/index.html
            if is_guide_page(page_path) and html.name == "index.html":
                guide_words.append((page_path, parser.word_count))

        for href in parser.links:
            for problem in check_play_link(href):
                errors.append(f"{rel}: Play link {href} — {problem}")

            internal = resolve_internal(page_path, href, base_prefix)
            if internal is None:
                continue
            if re.search(r"\.(css|js|png|jpg|jpeg|webp|svg|ico|xml|txt|json|woff2?)(/)?$", internal, re.I):
                continue
            if not path_exists(internal):
                errors.append(
                    f"{rel}: broken internal link -> {href} (resolved {internal})"
                )

    print(
        f"Checked {len(files)} HTML files under dist/ "
        f"(base_prefix={base_prefix or '/'})"
    )
    if guide_words:
        print("Guide word counts:")
        for path, wc in sorted(guide_words):
            flag = " OK" if wc >= 400 else (" THIN" if wc < 300 else " short")
            print(f"  {path}: {wc} words{flag}")
    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print("Failures:")
        for e in errors:
            print(f"  - {e}")
        print(f"RESULT: FAIL ({len(errors)} error(s), {len(warnings)} warning(s))")
        return 1
    print(f"RESULT: PASS (0 errors, {len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
