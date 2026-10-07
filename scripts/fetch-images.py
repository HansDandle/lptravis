"""Download every attachment referenced by the WordPress export into public/images,
preserving the wp-content/uploads/YYYY/MM path so content rewrites are mechanical."""
import os, re, sys, time, urllib.request, urllib.error
import xml.etree.ElementTree as ET

NS = {'wp': 'http://wordpress.org/export/1.2/',
      'content': 'http://purl.org/rss/1.0/modules/content/'}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XML = os.path.join(ROOT, 'libertarianpartyoftravixcounty.WordPress.2026-10-07.xml')
OUT = os.path.join(ROOT, 'public', 'images')

# Any uploads URL, stopping at whitespace or the characters that delimit it in HTML.
_STOP = ''.join(['\\s', '"', "'", '<', '>', ')', '\\\\'])
IMG_RE = r'https://lptravis\.org/wp-content/uploads/[^' + _STOP + r']+'

def local_path(url):
    m = re.search(r'/wp-content/uploads/(.+)$', url)
    rel = m.group(1) if m else os.path.basename(url)
    rel = rel.split('?')[0]
    return os.path.join(OUT, *rel.split('/'))

def collect():
    tree = ET.parse(XML)
    ch = tree.getroot().find('channel')
    urls = set()
    for it in ch.findall('item'):
        u = it.findtext('wp:attachment_url', namespaces=NS)
        if u:
            urls.add(u)
        body = it.findtext('content:encoded', namespaces=NS) or ''
        for m in re.findall(IMG_RE, body):
            urls.add(m.split('?')[0])
    return sorted(urls)

def main():
    urls = collect()
    print(f'{len(urls)} unique image URLs', flush=True)
    ok = skip = fail = 0
    failures = []
    for i, url in enumerate(urls, 1):
        dest = local_path(url)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            skip += 1
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (site-migration)'})
            with urllib.request.urlopen(req, timeout=45) as r:
                data = r.read()
            if not data:
                raise ValueError('empty response')
            with open(dest, 'wb') as f:
                f.write(data)
            ok += 1
        except Exception as e:
            fail += 1
            failures.append(f'{url}\t{e}')
        if i % 20 == 0:
            print(f'  {i}/{len(urls)} ok={ok} skip={skip} fail={fail}', flush=True)
        time.sleep(0.15)
    print(f'DONE ok={ok} skip={skip} fail={fail}', flush=True)
    if failures:
        with open(os.path.join(ROOT, 'scripts', 'image-failures.txt'), 'w') as f:
            f.write('\n'.join(failures))
        print('failures written to scripts/image-failures.txt', flush=True)

main()
