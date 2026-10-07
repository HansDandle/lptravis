// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { rehypeBaseUrls } from './src/plugins/rehype-base-urls.mjs';

// When the party moves to its own domain, set `site` to https://lptravis.org
// and change `base` to '/'. Nothing else needs to change.
const BASE = '/lptravis';

export default defineConfig({
  site: 'https://hansdandle.github.io',
  base: BASE,
  trailingSlash: 'ignore',
  integrations: [sitemap()],
  markdown: {
    rehypePlugins: [[rehypeBaseUrls, { base: BASE }]],
    shikiConfig: { theme: 'github-light', wrap: true },
  },
});
