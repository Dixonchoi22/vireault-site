# Vireault marketing site

Static SEO site for **Vireault** (`com.vireault.app`), an Android encrypted photo and file vault.

- Framework: Astro 7 (static output)
- Domain placeholder: `https://vireault.app` (set in `astro.config.mjs` and `src/data/site.ts`)
- Do not confuse with `/workspace/vaultdroid` (the Android app repo)

## Commands

```bash
npm install
npm run build
npm run preview   # http://127.0.0.1:4321
npm run dev
```

## Content rules

Only claim shipping features. Never copy Vaultaire branding or text. See `SEO-PLAYBOOK.md` for the daily Search Console → one guide → internal links routine.

## Hosting

Deployed to GitHub Pages (branch `gh-pages`, built by `./deploy/publish-gh-pages.sh`) at https://dixonchoi22.github.io/vireault-site/.
`/privacy.html` is the original published privacy policy, kept byte-for-byte in `public/`.

To move to a custom domain later: set repo variables `SITE_URL=https://yourdomain` and `BASE_PATH=/`,
add `public/CNAME` with the domain, and configure it in Settings → Pages. Canonicals, sitemap, robots and links follow automatically.

`deploy/github-pages-workflow.yml` is a ready GitHub Actions alternative; move it to `.github/workflows/` once the gh token has the `workflow` scope (`gh auth refresh -s workflow`), then set Pages source to GitHub Actions.
