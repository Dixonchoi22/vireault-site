// @ts-check
import { defineConfig } from 'astro/config';
import basePathLinks from './integrations/base-path-links.mjs';

// Hosting is configurable. Defaults target GitHub Pages:
//   https://dixonchoi22.github.io/vireault-site/
// When a custom domain is ready, build with:
//   SITE_URL=https://example.com BASE_PATH=/ npm run build
// (and add public/CNAME). Nothing else needs to change.
const SITE_URL = process.env.SITE_URL || 'https://dixonchoi22.github.io';
const BASE_PATH = process.env.BASE_PATH ?? '/vireault-site';

export default defineConfig({
  site: SITE_URL,
  base: BASE_PATH,
  trailingSlash: 'ignore',
  build: { format: 'directory' },
  integrations: [basePathLinks()],
});
