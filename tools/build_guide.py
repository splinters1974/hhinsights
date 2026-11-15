"""
Builds the downloadable user guide: fills tools/guide/guide.html with the
site's name and contact details (the logo is tools/guide/img/hhi-logo.png), then renders it to
site/downloads/half-hourly-insights-user-guide.pdf with Playwright.

Screenshots in tools/guide/img come from the analyser (site/analyser) with
example data; retake them if the analyser's layout changes.
"""
import os
import subprocess

from kit import CONTACT_EMAIL, NAME, OPERATOR

HERE = os.path.dirname(os.path.abspath(__file__))
GUIDE = os.path.join(HERE, 'guide')
OUT = os.path.join(HERE, '..', 'site', 'downloads', 'half-hourly-insights-user-guide.pdf')
GUIDE_URL = 'downloads/half-hourly-insights-user-guide.pdf'

if __name__ == '__main__':
    src = open(os.path.join(GUIDE, 'guide.html'), encoding='utf-8').read()
    built = (src.replace('{{OPERATOR}}', OPERATOR).replace('{{EMAIL}}', CONTACT_EMAIL))
    assert '{{' not in built, 'unfilled placeholder'
    path = os.path.join(GUIDE, 'guide-built.html')
    open(path, 'w', encoding='utf-8').write(built)
    subprocess.run(['node', os.path.join(GUIDE, 'render.cjs'), path, os.path.abspath(OUT),
                    f'{NAME} &middot; User guide &middot; November 2026'], check=True)
    os.remove(path)
    print('wrote', os.path.relpath(OUT, os.path.join(HERE, '..')), os.path.getsize(OUT) // 1024, 'KB')
