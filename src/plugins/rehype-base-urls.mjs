/**
 * Prefix root-relative URLs in Markdown content with the configured `base`.
 *
 * Content files store plain absolute paths (/news/..., /images/...) so they stay
 * portable: if the site later moves to its own domain, only astro.config changes.
 */
export function rehypeBaseUrls({ base = '' } = {}) {
  const prefix = base.replace(/\/$/, '');

  return (tree) => {
    if (!prefix) return;

    const visit = (node) => {
      if (node.type === 'element') {
        const attrs = node.tagName === 'a' ? ['href']
          : node.tagName === 'img' ? ['src']
          : node.tagName === 'source' ? ['src', 'srcset']
          : [];

        for (const attr of attrs) {
          const value = node.properties?.[attr];
          // Only rewrite root-relative paths; leave protocol, anchors and
          // already-prefixed URLs alone.
          if (
            typeof value === 'string' &&
            value.startsWith('/') &&
            !value.startsWith('//') &&
            !value.startsWith(`${prefix}/`)
          ) {
            node.properties[attr] = prefix + value;
          }
        }
      }
      for (const child of node.children ?? []) visit(child);
    };

    visit(tree);
  };
}
