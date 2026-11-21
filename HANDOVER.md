# vireault-site — Handover (21 Nov 2026)

> **Status: ACTIVE.** The site publishes one SEO guide a day to GitHub Pages via `deploy/publish-gh-pages.sh`. Search Console is verified with the `google-site-verification` meta tag in `BaseLayout.astro`.

## What it is
Static SEO and marketing site for the Android app **Vireault** (`com.vireault.app`; app repo: Dixonchoi22/Vireault, private). Astro 7, static output. See `README.md` and `SEO-PLAYBOOK.md`.

## What's live
- GitHub Pages from branch **`gh-pages`** (build output): https://dixonchoi22.github.io/vireault-site/ (privacy policy at `/privacy.html`, used by Play Console). Publish with `./deploy/publish-gh-pages.sh`. Default `SITE_URL` / `BASE_PATH` keep links under `/vireault-site/`.
- Custom domain `vireault.app` is a placeholder (currently HTTP 500). Buying and configuring it is Dixon's call.

## Build and deploy
- `npm install && npm run build` (Node ≥ 22). `python3 scripts/check_site.py --rebuild` checks titles, meta, canonicals, internal links, Play UTMs and word counts.
- Deploy: `./deploy/publish-gh-pages.sh` builds and pushes `dist/` to `gh-pages`.
- **CI: none active.** `deploy/github-pages-workflow.yml` is a ready GitHub Actions alternative. Moving it into `.github/workflows/` needs a token with the `workflow` scope, then set the Pages source to GitHub Actions.
- **Do not merge `gh-pages` into `main`.** It is the generated build output, not source.

## Accounts and secrets (names only)
- GitHub repo variables (optional, for a custom domain): `SITE_URL`, `BASE_PATH`. No secrets are used.
- Play listing UTMs: `utm_source=vireault-site&utm_medium=guide&utm_campaign=<slug>`.
- Search Console: verified by the meta tag in `src/layouts/BaseLayout.astro`. Do not remove it.

## Open tasks
1. Daily SEO loop: one guide, then internal links (`SEO-PLAYBOOK.md`). Only claim features that ship.
2. Terms-of-service page. Custom domain (Dixon).

## Design files
Desktop and mobile comparison screenshots (Vaultaire vs Vireault, old vs new) are in `docs/handover/design-comparisons/`. `previews/` holds page previews.

## Rules
No development Monday–Friday 09:00–16:00 London. Never force-push or rewrite history. This repo is **public**: never commit secrets, keystores or private business data.
