// Prefixes root-relative href/src/srcset values in built HTML with the Astro base path,
// so source files can keep writing "/features" and still work under a sub-path.
import { readdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

async function* walk(dir) {
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) yield* walk(p);
    else if (e.name.endsWith('.html')) yield p;
  }
}

export default function basePathLinks() {
  let base = '/';
  return {
    name: 'base-path-links',
    hooks: {
      'astro:config:done': ({ config }) => { base = config.base.replace(/\/$/, ''); },
      'astro:build:done': async ({ dir }) => {
        if (!base) return;
        const root = fileURLToPath(dir);
        for await (const file of walk(root)) {
          const html = await readFile(file, 'utf8');
          if (html.includes('data-legacy-static')) continue; // preserved legacy pages
          const out = html.replace(/\b(href|src|action)="\/(?!\/)([^"]*)"/g, (m, attr, rest) =>
            ('/' + rest).startsWith(base + '/') || '/' + rest === base ? m : `${attr}="${base}/${rest}"`);
          if (out !== html) await writeFile(file, out);
        }
      },
    },
  };
}
