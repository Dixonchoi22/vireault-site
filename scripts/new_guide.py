#!/usr/bin/env python3
"""Scaffold a new /guides/<slug> Astro page and register it in src/data/site.ts.

Usage:
  python3 scripts/new_guide.py <slug> "Title" "Meta description" ["Breadcrumb label"]

Play CTAs use the site Cta component + playUrl(), which tags:
  utm_source=vireault-site&utm_medium=guide&utm_campaign=<slug>
"""
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDES_DIR = ROOT / "src" / "pages" / "guides"
SITE_TS = ROOT / "src" / "data" / "site.ts"

PLAY_UTM = (
    "https://play.google.com/store/apps/details?id=com.vireault.app"
    "&utm_source=vireault-site&utm_medium=guide&utm_campaign={slug}"
)


def js_string(s: str) -> str:
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def slug_ok(slug: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug))


def register_guide(slug: str, title: str, description: str) -> None:
    text = SITE_TS.read_text()
    if f"slug: '{slug}'" in text or f'slug: "{slug}"' in text:
        print(f"site.ts already lists slug {slug}; skipping GUIDES insert")
        return
    entry = (
        "  {\n"
        f"    slug: '{slug}',\n"
        f"    title: {js_string(title)},\n"
        f"    description: {js_string(description)},\n"
        f"    href: '/guides/{slug}',\n"
        "  },\n"
    )
    m = re.search(r"export const GUIDES = \[.*?\] as const;", text, re.S)
    if not m:
        raise SystemExit("Could not find export const GUIDES in site.ts")
    block = m.group(0)
    new_block = block[: -len("] as const;")] + entry + "] as const;"
    SITE_TS.write_text(text[: m.start()] + new_block + text[m.end() :])
    print(f"Registered /guides/{slug} in src/data/site.ts")


def main(argv: list[str]) -> int:
    if len(argv) < 4:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    slug, title, description = argv[1], argv[2], argv[3]
    crumb = argv[4] if len(argv) > 4 else title
    if not slug_ok(slug):
        print("slug must be lowercase kebab-case", file=sys.stderr)
        return 2
    out = GUIDES_DIR / f"{slug}.astro"
    if out.exists():
        print(f"Refusing to overwrite existing {out}", file=sys.stderr)
        return 1
    today = date.today().isoformat()
    title_js = js_string(title)
    desc_js = js_string(description)
    crumb_js = js_string(crumb)
    body = f"""---
import BaseLayout from '../../layouts/BaseLayout.astro';
import Breadcrumbs from '../../components/Breadcrumbs.astro';
import Cta from '../../components/Cta.astro';
const pageSlug = '{slug}';
const articleLd = {{
  '@context': 'https://schema.org',
  '@type': 'Article',
  headline: {title_js},
  description: {desc_js},
  author: {{ '@type': 'Organization', name: 'Vireault' }},
  datePublished: '{today}',
  dateModified: '{today}',
  mainEntityOfPage: 'https://vireault.app/guides/{slug}',
}};
---
<BaseLayout
  title={title_js}
  description={desc_js}
  path="/guides/{slug}"
  pageSlug={{pageSlug}}
  ogType="article"
  jsonLd={{articleLd}}
  article={{{{ published: '{today}', modified: '{today}' }}}}
>
  <div class="container">
    <Breadcrumbs items={{[{{ href: '/', label: 'Home' }}, {{ href: '/guides', label: 'Guides' }}, {{ label: {crumb_js} }}]}} />
    <article class="section prose">
      <h1>{title}</h1>
      <p>Write the job-to-be-done answer in the first screen. Cite primary sources. Only claim shipping Vireault features.</p>
      <h2>What this guide covers</h2>
      <p>Replace this scaffold body with researched sections.</p>
      <Cta pageSlug={{pageSlug}} heading="Need encrypted storage on the phone?" body="Vireault encrypts photos, videos and files on your Android phone. No account. Offline and local only." />
      <h2>Where Vireault fits</h2>
      <p>Link to <a href="/features/encryption">encryption</a>, <a href="/features/offline">offline</a>, and related guides.</p>
      <h2>Related reading</h2>
      <ul>
        <li><a href="/guides/how-to-hide-photos-on-android">How to hide photos on Android</a></li>
        <li><a href="/security">How Vireault encrypts</a></li>
      </ul>
    </article>
    <Cta pageSlug={{pageSlug}} />
  </div>
</BaseLayout>
"""
    out.write_text(body)
    print(f"Wrote {out.relative_to(ROOT)}")
    print(f"Play CTA pattern: {PLAY_UTM.format(slug=slug)}")
    register_guide(slug, title, description)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
