"""
Prepare the tab page header photos.

    python3 tools/make_heroes.py how-it-works=path/to/photo.png guides=... sectors=... faq=... contact=...

Writes site/images/heroes/<name>.jpg (1600 px wide) and <name>-900.jpg for
phones, each also as WebP, then rebuild the pages with tools/build_pages.py. Needs Pillow.
"""
import os
import sys

from PIL import Image

OUT = os.path.join(os.path.dirname(__file__), '..', 'site', 'images', 'heroes')
NAMES = {'how-it-works', 'guides', 'sectors', 'solar', 'faq', 'contact',
         # guide pages: the name is the page's file name without .html
         'get-your-data', 'example-office-analysis', 'example-school-analysis', 'reading-a-heatmap',
         'out-of-hours-electricity', 'base-load', 'supply-capacity', 'proving-savings', 'half-hourly-settlement',
         'mpan-profile-class', 'electricity-benchmarks', 'business-electricity-price', 'non-energy-charges',
         'electricity-prices-ten-years', 'non-energy-costs-outlook', 'glossary'}


def save(src, name):
    os.makedirs(OUT, exist_ok=True)
    with Image.open(src) as im:
        im = im.convert('RGB')
        for width, suffix, q in [(1600, '', 80), (900, '-900', 78)]:
            h = round(im.height * width / im.width)
            small = im.resize((width, h), Image.LANCZOS)
            small.save(os.path.join(OUT, f'{name}{suffix}.jpg'), quality=q, optimize=True, progressive=True)
            small.save(os.path.join(OUT, f'{name}{suffix}.webp'), quality=q - 2, method=6)  # served first; JPEG is the fallback


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        name, src = arg.split('=', 1)
        if name not in NAMES:
            sys.exit(f'unknown page {name}: use one of {", ".join(sorted(NAMES))}')
        save(src, name)
        print(f'wrote {name}')
