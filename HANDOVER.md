# vireault-site — Handover (15 Nov 2026, app work frozen)

> **Status: FROZEN.** On 15 Nov 2026 Dixon put the team all-in on YouTube clipping. Vireault marketing (including this site) is stopped until Dixon reopens it. Any future work is done with **cloud Claude Code (web)** on Dixon's Pro account, straight from this repo.

## What it is
Static SEO and marketing site for the Android app **Vireault** (`com.vireault.app`; app repo: Dixonchoi22/Vireault, private). Astro 7, static output. See `README.md` and `SEO-PLAYBOOK.md`.

## What's live
- GitHub Pages from branch **`gh-pages`** (build output, last deploy 7 Nov 2026 of `d061873`): https://dixonchoi22.github.io/vireault-site/ (privacy policy at `/privacy.html`, used by Play Console).
- **Not deployed yet:** everything merged into `main` after 7 Nov, including PR #1 (guide "How to hide photos on Android without an app", `scripts/new_guide.py`, `scripts/check_site.py`, merged 15 Nov). Publishing is an outside post, so **Dixon must approve a deploy**.
- Custom domain `vireault.app` is a placeholder (currently HTTP 500). Buying and configuring it is Dixon's call.

## Build and deploy
- `npm install && npm run build` (Node ≥ 22). `python3 scripts/check_site.py --rebuild` checks titles, meta, canonicals, internal links, Play UTMs and word counts.
- Deploy (after Dixon approves): `./deploy/publish-gh-pages.sh` builds and pushes `dist/` to `gh-pages`.
- **CI: none active.** `deploy/github-pages-workflow.yml` is a ready GitHub Actions alternative. Moving it into `.github/workflows/` needs a token with the `workflow` scope, then set the Pages source to GitHub Actions.
- **Do not merge `gh-pages` into `main`.** It is the generated build output, not source.

## Accounts and secrets (names only)
- GitHub repo variables (optional, for a custom domain): `SITE_URL`, `BASE_PATH`. No secrets are used.
- Play listing UTMs: `utm_source=vireault-site&utm_medium=guide&utm_campaign=<slug>`.

## Open tasks (when Dixon reopens)
1. Dixon approves deploying `main` (new guide) to GitHub Pages.
2. Daily SEO loop: Search Console, then one guide, then internal links (`SEO-PLAYBOOK.md`). Only claim features that ship.
3. Terms-of-service page. Custom domain (Dixon).

## Design files
Desktop and mobile comparison screenshots (Vaultaire vs Vireault, old vs new) are in `docs/handover/design-comparisons/`. `previews/` holds page previews.

## Rules
No development Monday–Friday 09:00–16:00 London. Deploys and any other outside posts need Dixon. Never force-push or rewrite history. This repo is **public**: never commit secrets, keystores or private business data.
