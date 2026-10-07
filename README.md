# lptravis.org

The website of the Libertarian Party of Travis County, rebuilt as a static site
and hosted free on GitHub Pages. It replaces the old WordPress site; all posts,
pages, and images were migrated out of the WordPress export.

## Quick start

```bash
npm install
npm run dev      # local preview at http://localhost:4321/lptravis
npm run build    # production build into dist/
npm run preview  # serve the built site
```

Node 20 or newer is required.

## How it is put together

| Path | What it holds |
| --- | --- |
| `src/pages/` | One file per route. `.astro` files are hand-built pages; `[...slug].astro` renders Markdown. |
| `src/content/news/` | Blog posts, one Markdown file each. |
| `src/content/pages/` | Standalone pages (bylaws, archived candidate lists). |
| `src/site.config.ts` | **Meeting time, venue, officers, social links.** Edit this first. |
| `src/layouts/`, `src/components/` | Shared page shell, header, footer, cards. |
| `src/styles/global.css` | Design tokens and shared styles. Colors live at the top. |
| `public/images/` | All 124 images migrated from WordPress, in their original `YYYY/MM` folders. |
| `scripts/` | One-off migration scripts (see below). |

Content is plain Markdown with YAML frontmatter, validated by a schema in
`src/content.config.ts`. A build fails loudly if a post is missing a title or has
a malformed date, which is deliberate.

## Editing the site

Non-technical editing is documented for officers in
**[docs/EDITING.md](docs/EDITING.md)** — start there.

In short:

- **Change the meeting time or venue:** edit `src/site.config.ts`.
- **Write a post:** add a Markdown file to `src/content/news/`, or use the web
  editor at `/admin/` once it is connected.
- **Add an image:** drop it in `public/images/` and reference it as
  `/images/your-file.jpg`.

## Deployment

Pushing to `main` triggers `.github/workflows/deploy.yml`, which builds the site
and publishes it to GitHub Pages. Enable this once, under
**Settings → Pages → Source → GitHub Actions**.

The site currently builds for `https://hansdandle.github.io/lptravis`.

### Moving to the lptravis.org domain

1. In `astro.config.mjs`, set `site: 'https://lptravis.org'` and `BASE = '/'`.
2. In `src/site.config.ts`, set `url` to `https://lptravis.org`.
3. Add a `public/CNAME` file containing `lptravis.org`.
4. Point the domain's DNS at GitHub Pages and set the custom domain under
   **Settings → Pages**.

Because every internal link is written as a root-relative path and prefixed at
build time, nothing else needs to change.

## The migration

Three scripts in `scripts/` performed the one-time move off WordPress. They are
kept for reference and are safe to re-run, but should not be needed again.

| Script | Purpose |
| --- | --- |
| `fetch-images.py` | Downloaded all 124 images from lptravis.org into `public/images/`. |
| `convert-content.py` | Converted the WordPress XML export into Markdown. |
| `fix-links.py` | Rewrote old WordPress permalinks to the new URL scheme. |

The original export, `libertarianpartyoftravixcounty.WordPress.2026-10-07.xml`,
is kept in the repository as the source of record.

### What changed from the old site

- Posts moved from `/2023/09/02/slug/` to `/news/2023-09-02-slug`.
- The old `Calendar` and `What's New?` pages became `/events` and `/news`.
- `Get Gear` became `/gear`; `Contact Us` became `/contact`.
- The 2012 and 2014 candidate pages are kept at their original slugs but marked
  archived, and are listed under `/archive`.
- Six empty or draft pages in the export were not migrated.

A `404` page points visitors at the news index and archive when an old link
misses.
