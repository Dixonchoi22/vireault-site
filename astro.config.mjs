// @ts-check
import { defineConfig } from 'astro/config';

// Domain placeholder — change SITE.domain / site value together when the real domain is ready.
export default defineConfig({
  site: 'https://vireault.app',
  trailingSlash: 'never',
  build: {
    format: 'directory',
  },
});
