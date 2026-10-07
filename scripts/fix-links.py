"""Rewrite internal links left over from WordPress to the new URL scheme.

Old post permalinks were /YYYY/MM/DD/slug/; posts now live at /news/YYYY-MM-DD-slug.
A handful of pages also moved or were replaced by purpose-built templates.
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS = os.path.join(ROOT, 'src', 'content', 'news')
PAGES = os.path.join(ROOT, 'src', 'content', 'pages')

# Pages whose WordPress path differs from where they now live.
PAGE_MAP = {
    '/': '/',
    '/contact-us/': '/contact',
    '/contact/': '/contact',
    '/calendar/': '/events',
    '/news/': '/news',
    '/about/': '/about',
    '/bylaws/': '/bylaws',
    '/getgear/': '/gear',
    '/donate-to-lp-travis/': '/donate-to-lp-travis',
    '/2012-candidates/': '/2012-candidates',
    '/2014-candidates/': '/2014-candidates',
    '/candidates/': '/candidates',
}

POST_PERMALINK = re.compile(r'^/(\d{4})/(\d{2})/(\d{2})/([^/)]+)/?$')


def build_post_index():
    """slug -> new path, for resolving old dated permalinks."""
    index = {}
    for name in os.listdir(NEWS):
        if not name.endswith('.md'):
            continue
        stem = name[:-3]
        slug = stem[11:]  # strip the YYYY-MM-DD- prefix
        index[slug] = '/news/' + stem
    return index


def main():
    posts = build_post_index()
    link_re = re.compile(r'(\]\()(/[^)]*)(\))')
    changed = 0
    unresolved = []

    for folder in (NEWS, PAGES):
        for name in sorted(os.listdir(folder)):
            if not name.endswith('.md'):
                continue
            path = os.path.join(folder, name)
            src = io.open(path, encoding='utf-8').read()

            def repl(m):
                target = m.group(2)
                if target.startswith('/images/'):
                    return m.group(0)
                pm = POST_PERMALINK.match(target)
                if pm:
                    slug = pm.group(4)
                    if slug in posts:
                        return m.group(1) + posts[slug] + m.group(3)
                    unresolved.append((name, target))
                    return m.group(1) + '/news' + m.group(3)
                if target in PAGE_MAP:
                    return m.group(1) + PAGE_MAP[target] + m.group(3)
                unresolved.append((name, target))
                return m.group(0)

            out = link_re.sub(repl, src)
            if out != src:
                io.open(path, 'w', encoding='utf-8', newline='').write(out)
                changed += 1

    print('files rewritten:', changed)
    if unresolved:
        print('unresolved:')
        for n, t in unresolved:
            print('  ', n, '->', t)


main()
