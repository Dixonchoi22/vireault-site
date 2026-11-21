// Helpers for guide pages: per-guide images (optional, with fallback) and
// FAQPage / HowTo / BreadcrumbList / ItemList JSON-LD.
//
// Images live in public/images/guides/<slug>/ :
//   hero.(webp|png|jpg|jpeg|avif|svg)        unique hero for the guide
//   step-1.(...), step-2.(...)               optional step screenshots (how-to guides)
// Anything missing is simply skipped; the site-wide default image is used
// where a social/Article image is needed.
import { existsSync } from 'node:fs';
import { join } from 'node:path';
import { SITE } from './site';

export const DEFAULT_IMAGE = '/images/feature-graphic.png';
const EXTENSIONS = ['webp', 'png', 'jpg', 'jpeg', 'avif', 'svg'];
const PUBLIC_DIR = join(process.cwd(), 'public');

/** Root-relative path of public/images/guides/<slug>/<name>.<ext>, or null if no such file. */
export function guideAsset(slug: string, name: string): string | null {
  for (const ext of EXTENSIONS) {
    const rel = `/images/guides/${slug}/${name}.${ext}`;
    if (existsSync(join(PUBLIC_DIR, rel))) return rel;
  }
  return null;
}

/** Social / Article image for a guide: its unique hero, else the site default. */
export function guideImagePath(slug: string): string {
  return guideAsset(slug, 'hero') ?? DEFAULT_IMAGE;
}

export const absUrl = (path: string): string => `${SITE.domain}${path}`;

export interface FaqItem {
  question: string;
  answer: string;
}

/** FAQPage. Question/answer text must be rendered visibly on the same page. */
export function faqLd(items: FaqItem[]): Record<string, unknown> {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: items.map((i) => ({
      '@type': 'Question',
      name: i.question,
      acceptedAnswer: { '@type': 'Answer', text: i.answer },
    })),
  };
}

export interface HowToStepInput {
  /** Plain text identical to the visible step. */
  text: string;
  /** Optional screenshot base name in the guide's image folder, e.g. 'step-1'. */
  image?: string;
}

/** HowTo. Steps must be the same steps rendered visibly on the page. */
export function howToLd(opts: {
  slug: string;
  name: string;
  description: string;
  steps: HowToStepInput[];
}): Record<string, unknown> {
  return {
    '@context': 'https://schema.org',
    '@type': 'HowTo',
    name: opts.name,
    description: opts.description,
    step: opts.steps.map((s, i) => {
      const img = s.image ? guideAsset(opts.slug, s.image) : null;
      return {
        '@type': 'HowToStep',
        position: i + 1,
        text: s.text,
        ...(img ? { image: absUrl(img) } : {}),
      };
    }),
  };
}

export interface Crumb {
  href?: string;
  label: string;
}

/** BreadcrumbList matching the visible breadcrumb trail. */
export function breadcrumbLd(items: Crumb[]): Record<string, unknown> {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((c, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: c.label,
      ...(c.href ? { item: absUrl(c.href === '/' ? '/' : c.href) } : {}),
    })),
  };
}

/** ItemList for the guides index, in the same order as the visible cards. */
export function itemListLd(guides: readonly { title: string; href: string }[]): Record<string, unknown> {
  return {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    itemListElement: guides.map((g, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: g.title,
      url: absUrl(g.href),
    })),
  };
}
