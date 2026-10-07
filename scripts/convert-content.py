"""Convert the WordPress WXR export into Astro content collections.

Posts become src/content/news/<slug>.md, pages become src/content/pages/<slug>.md.
WordPress block comments are stripped, Gutenberg HTML is reduced to clean Markdown
where it maps cleanly, and uploads URLs are rewritten to local /images/ paths.
"""
import html
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime

NS = {
    'wp': 'http://wordpress.org/export/1.2/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XML = os.path.join(ROOT, 'libertarianpartyoftravixcounty.WordPress.2026-10-07.xml')
NEWS_DIR = os.path.join(ROOT, 'src', 'content', 'news')
PAGES_DIR = os.path.join(ROOT, 'src', 'content', 'pages')

UPLOADS = 'https://lptravis.org/wp-content/uploads/'

# Pages that the new site renders from bespoke Astro templates rather than Markdown.
SKIP_PAGES = {
    'welcome-to-the-libertarian-party-of-travis-county',
    'news', 'calendar', 'contact', 'donate-to-lp-travis', 'getgear',
}


def rewrite_urls(text):
    """Point uploads at the local copies and make internal links relative."""
    text = text.replace(UPLOADS, '/images/')
    text = re.sub(r'https?://(?:www\.)?(?:lptravis|travislp)\.org/?', '/', text)
    # Strip WordPress' resize query strings now that files are served statically.
    text = re.sub(r'(/images/[^\s"\')<>]+?)\?[\w=&;%.-]+', r'\1', text)
    return text


def strip_blocks(text):
    """Remove Gutenberg block delimiters and WordPress shortcodes."""
    text = re.sub(r'<!--\s*/?wp:.*?-->', '', text, flags=re.S)
    text = re.sub(r'<!--\s*/?more\s*-->', '', text, flags=re.S)
    text = re.sub(r'\[googleapps[^\]]*\]', '', text)
    text = re.sub(r'\[/?caption[^\]]*\]', '', text)
    text = re.sub(r'\[embed[^\]]*\]|\[/embed\]', '', text)
    return text


def tag_to_md(text):
    """Convert the small set of HTML tags this site actually uses into Markdown."""
    # Figures: keep the image, keep the caption as italic text beneath it.
    def figure(m):
        block = m.group(0)
        img = re.search(r'<img[^>]*?src="([^"]+)"[^>]*?>', block)
        cap = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', block, re.S)
        if not img:
            return ''
        alt = re.search(r'alt="([^"]*)"', block)
        out = '![%s](%s)' % (alt.group(1) if alt else '', img.group(1))
        if cap:
            caption = re.sub(r'<[^>]+>', ' ', cap.group(1))
            caption = ' '.join(html.unescape(caption).split())
            if caption:
                out += '\n\n*%s*' % caption
        return '\n\n' + out + '\n\n'

    text = re.sub(r'<figure.*?</figure>', figure, text, flags=re.S)

    def img(m):
        src = re.search(r'src="([^"]+)"', m.group(0))
        alt = re.search(r'alt="([^"]*)"', m.group(0))
        if not src:
            return ''
        return '\n\n![%s](%s)\n\n' % (alt.group(1) if alt else '', src.group(1))

    text = re.sub(r'<img[^>]*>', img, text)

    # Links -> Markdown, preserving the visible text.
    def link(m):
        href, inner = m.group(1), m.group(2)
        inner = re.sub(r'<[^>]+>', '', inner)
        inner = ' '.join(html.unescape(inner).split())
        if not inner:
            return ''
        if inner.startswith('!['):
            return inner
        return '[%s](%s)' % (inner, href)

    text = re.sub(r'<a[^>]*?href="([^"]*)"[^>]*>(.*?)</a>', link, text, flags=re.S)

    for lvl in range(2, 7):
        text = re.sub(r'<h%d[^>]*>(.*?)</h%d>' % (lvl, lvl),
                      lambda m, l=lvl: '\n\n' + '#' * l + ' ' +
                      ' '.join(re.sub(r'<[^>]+>', '', m.group(1)).split()) + '\n\n',
                      text, flags=re.S)

    text = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>', r'**\2**', text, flags=re.S)
    text = re.sub(r'<(em|i)[^>]*>(.*?)</\1>', r'*\2*', text, flags=re.S)
    text = re.sub(r'<li[^>]*>(.*?)</li>',
                  lambda m: '\n- ' + ' '.join(m.group(1).split()), text, flags=re.S)
    text = re.sub(r'</?(ul|ol)[^>]*>', '\n\n', text)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'</p>|</div>|</blockquote>', '\n\n', text)
    text = re.sub(r'<blockquote[^>]*>', '\n\n> ', text)
    text = re.sub(r'<iframe[^>]*?src="([^"]+)"[^>]*>.*?</iframe>',
                  r'\n\n[Embedded video](\1)\n\n', text, flags=re.S)
    text = re.sub(r'<[^>]+>', '', text)
    return text


def tidy(text):
    text = html.unescape(text)
    text = text.replace(' ', ' ').replace('�', "'")
    lines = [ln.rstrip() for ln in text.split('\n')]
    text = '\n'.join(lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    return text.strip()


def to_markdown(raw):
    return tidy(tag_to_md(strip_blocks(rewrite_urls(raw))))


def yaml_str(s):
    return '"%s"' % s.replace('\\', '\\\\').replace('"', '\\"')


def first_image(md):
    m = re.search(r'!\[[^\]]*\]\((/images/[^)]+)\)', md)
    return m.group(1) if m else None


def summarize(md, limit=200):
    body = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', md)
    body = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', body)
    body = re.sub(r'[#*>`]', '', body)
    body = ' '.join(body.split())
    if len(body) <= limit:
        return body
    cut = body[:limit].rsplit(' ', 1)[0]
    return cut + '...'


def main():
    os.makedirs(NEWS_DIR, exist_ok=True)
    os.makedirs(PAGES_DIR, exist_ok=True)
    tree = ET.parse(XML)
    ch = tree.getroot().find('channel')

    counts = {'news': 0, 'pages': 0, 'skipped': 0}
    for it in ch.findall('item'):
        ptype = it.findtext('wp:post_type', namespaces=NS)
        status = it.findtext('wp:status', namespaces=NS)
        if ptype not in ('post', 'page') or status != 'publish':
            counts['skipped'] += 1
            continue

        title = html.unescape(it.findtext('title') or '').replace('�', "'").strip()
        slug = it.findtext('wp:post_name', namespaces=NS) or ''
        raw = it.findtext('content:encoded', namespaces=NS) or ''
        date_s = it.findtext('wp:post_date', namespaces=NS) or ''
        if not title or not slug:
            counts['skipped'] += 1
            continue

        body = to_markdown(raw)
        if ptype == 'page' and slug in SKIP_PAGES:
            counts['skipped'] += 1
            continue
        if not body.strip():
            counts['skipped'] += 1
            continue

        cats = [html.unescape(c.text or '') for c in it.findall('category')
                if c.get('domain') == 'category' and c.text]
        cats = [c for c in cats if c.lower() != 'uncategorized']

        fm = ['---', 'title: ' + yaml_str(title)]
        if ptype == 'post':
            dt = datetime.strptime(date_s, '%Y-%m-%d %H:%M:%S')
            fm.append('date: %s' % dt.strftime('%Y-%m-%d'))
            desc = summarize(body)
            if desc:
                fm.append('description: ' + yaml_str(desc))
            hero = first_image(body)
            if hero:
                fm.append('image: ' + yaml_str(hero))
            if cats:
                fm.append('tags: [%s]' % ', '.join(yaml_str(c) for c in cats))
            out_dir, key = NEWS_DIR, 'news'
            name = '%s-%s.md' % (dt.strftime('%Y-%m-%d'), slug)
        else:
            desc = summarize(body)
            if desc:
                fm.append('description: ' + yaml_str(desc))
            out_dir, key = PAGES_DIR, 'pages'
            name = '%s.md' % slug
        fm.append('---')

        with open(os.path.join(out_dir, name), 'w', encoding='utf-8') as f:
            f.write('\n'.join(fm) + '\n\n' + body + '\n')
        counts[key] += 1

    print('news=%(news)d pages=%(pages)d skipped=%(skipped)d' % counts)


main()
