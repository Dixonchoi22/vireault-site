import type { APIRoute } from 'astro';
import { FEATURES, COMPARES, GUIDES, SITE } from '../data/site';

export const GET: APIRoute = () => {
  const staticPaths = [
    '/',
    '/features',
    '/pricing',
    '/faq',
    '/about',
    '/whats-new',
    '/compare',
    '/guides',
    '/security',
    '/privacy',
  ];
  const paths = [
    ...staticPaths,
    ...FEATURES.map((f) => f.href),
    ...COMPARES.map((c) => c.href),
    ...GUIDES.map((g) => g.href),
  ];
  const lastmod = '2026-11-05';
  const body = `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
    paths
      .map((path) => {
        const loc = path === '/' ? SITE.domain + '/' : `${SITE.domain}${path}/`;
        return `  <url>\n    <loc>${loc}</loc>\n    <lastmod>${lastmod}</lastmod>\n  </url>`;
      })
      .join('\n') +
    `\n</urlset>\n`;
  return new Response(body, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' },
  });
};
