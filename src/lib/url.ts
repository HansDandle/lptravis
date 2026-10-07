const BASE = import.meta.env.BASE_URL.replace(/\/$/, '');

/** The site's base path, without a trailing slash. */
export const base = BASE;

/**
 * Prefix a root-relative path with the site's base path.
 *
 * Content frontmatter stores plain paths like `/images/2023/09/photo.png` so the
 * files stay portable; templates run them through this before rendering.
 * External URLs and already-prefixed paths pass through untouched.
 */
export function url(path: string): string {
  if (!path) return path;
  if (/^[a-z]+:/i.test(path) || path.startsWith('//')) return path;
  if (!path.startsWith('/')) return path;
  if (BASE && (path === BASE || path.startsWith(`${BASE}/`))) return path;
  return BASE + path;
}
