// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { rehypeBaseUrls } from './src/plugins/rehype-base-urls.mjs';

// The site is served from its own domain, so there is no base path.
// (On a project page such as <user>.github.io/lptravis, BASE would be '/lptravis'.)
const BASE = '/';

export default defineConfig({
  site: 'https://lptravis.org',
  base: BASE,
  trailingSlash: 'ignore',
  integrations: [sitemap()],
  markdown: {
    rehypePlugins: [[rehypeBaseUrls, { base: BASE }]],
    shikiConfig: { theme: 'github-light', wrap: true },
  },
});
