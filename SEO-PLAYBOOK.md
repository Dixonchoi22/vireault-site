# Vireault SEO playbook (daily routine)

Copy the Vaultaire growth loop in process — not in branding or prose. Incumbents own Play Store search; the open web is still under-served for Android vault keywords.

## Goal

Rank for Android privacy / vault intents (hide photos, private gallery, lock folder, encrypt files, comparisons) and convert readers with mid-article and end-of-page Play Store CTAs.

Play CTA pattern:

`https://play.google.com/store/apps/details?id=com.vireault.app&utm_source=web&utm_medium=guide&utm_campaign=<page-slug>`

## Daily routine (about 45–90 minutes)

### 1. Pull Search Console opportunities

In Google Search Console (once the property for `vireault.app` exists):

1. Open **Performance → Search results**.
2. Filter last 28 days.
3. Sort by **Impressions** descending.
4. Find queries with **impressions but near-zero clicks** (or CTR far below page average).
5. Prefer queries that match Android intent and that incumbents under-serve on the web.
6. Skip branded queries you already rank #1 for; skip queries you cannot answer honestly with shipping features.

Save the chosen query and the landing page that currently receives the impressions (if any).

### 2. Write ONE quality guide

Create a single new `/guides/<slug>` page (or substantially expand one thin page — still count as the day’s one piece):

- Target one primary query in the title / H1.
- Answer the job-to-be-done in the first screen.
- Use original explanations; never paste Vaultaire (or competitor) copy.
- Only claim shipping Vireault capabilities (see product truth list below).
- Add a **mid-article CTA** and an **end CTA** with the correct `utm_campaign` slug.
- Include internal links to 2–4 relevant feature, compare, pricing or guide pages.
- Add title, meta description, canonical, Open Graph, and `Article` JSON-LD.

Ship the page the same day. Google often indexes new guides within a few days when the site already has crawl equity.

### 3. Add internal links from pages that already get traffic

After publishing:

1. From the Search Console landing page (or other high-impression URLs), add one contextual link to the new guide.
2. Link from the guides index and, when relevant, from a compare or feature page.
3. Avoid dumping identical footer spam; prefer in-body links.

### 4. Log the day

Keep a simple log (spreadsheet or `docs/seo-log.md`):

| Date (Europe/London) | Query | Slug | Linked from | Notes |
|---|---|---|---|---|

## Weekly extras

- Refresh one compare page if a competitor’s public positioning changed.
- Recheck pricing / feature claims against the app so the site never lies.
- Inspect CTA click-through roughly (Search Console + Play campaign UTM in Play Console once public).

## Product truth list (do not invent)

**Claim freely when accurate:** offline/local only; no account; Argon2id; AES-256-GCM; random master key; encrypted index / hidden names; PIN, 3×3 pattern or passphrase; several vaults; lockout; import/view photos, video, audio, PDF; search/sort/filter; encrypted backup + restore; auto-lock on background or ~5 minutes idle; screenshot blocking; optional delete original after import; free 1 vault / 50 items; Pro $1.99/week, $19.99/year with 3-day trial, $29.99 lifetime.

**Do not claim:** cloud sync; biometrics; decoy vaults; in-app camera. **Folders:** say “coming soon” only.

## On-page standards for every URL

- Unique `<title>` and meta description
- Canonical to `https://vireault.app/...` (placeholder domain until live)
- Open Graph tags
- JSON-LD: `SoftwareApplication` sitewide; `FAQPage` on FAQ; `Article` on guides/features/compares
- Mobile-first layout, visible focus states, skip link
- Strong internal linking hub: home ↔ features ↔ guides ↔ compare ↔ pricing ↔ FAQ ↔ privacy

## What not to do

- Do not buy a domain or deploy from this playbook alone without an explicit request.
- Do not copy Vaultaire trademarks, screenshots, or wording.
- Do not publish thin AI doorway pages; one solid guide beats five stubs.
- Do not attack competitors with unverifiable claims — stay factual and fair.
