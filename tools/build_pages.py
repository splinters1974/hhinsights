"""
Builds the Half Hourly Insights site in site/: every page from one layout,
plus robots.txt, llms.txt and (once the domain is set) sitemap.xml.

    python3 tools/build_pages.py

Settings, layout and structured data: tools/kit.py
Core pages: tools/pages_core.py
Guides and sector pages: tools/pages_guides.py
"""
import datetime as dt
import hashlib
import json
from pathlib import Path

import kit
from kit import NAME, OPERATOR, SITE_URL, layout, url
from pages_core import core_pages
from pages_guides import PAGES as GUIDE_PAGES
from pages_data import PAGES as DATA_PAGES

SITE = Path(__file__).resolve().parent.parent / 'site'
DATES_FILE = Path(__file__).resolve().parent / 'page_dates.json'

# Crawlers that answer questions and cite sources, listed explicitly (as on
# the UK Solar Calculator) so a later change to the wildcard can't shut them out.
AI_SEARCH = ['OAI-SearchBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot', 'Claude-SearchBot', 'Google-Extended']
AI_TRAINING = ['GPTBot', 'Applebot-Extended', 'CCBot', 'Meta-ExternalAgent']


def robots():
    lines = ['# Half Hourly Insights. Everything here is public and intended to be found, indexed and cited.', '',
             'User-agent: *', 'Allow: /', '', '# Search engines', 'User-agent: Googlebot', 'Allow: /', '',
             'User-agent: Bingbot', 'Allow: /', '', '# AI answer engines that cite their sources']
    for bot in AI_SEARCH:
        lines += [f'User-agent: {bot}', 'Allow: /', '']
    lines += ['# AI training crawlers: allowed so models know the site exists. Change to Disallow to opt out.']
    for bot in AI_TRAINING:
        lines += [f'User-agent: {bot}', 'Allow: /', '']
    if SITE_URL:
        lines.append(f'Sitemap: {SITE_URL}/sitemap.xml')
    return '\n'.join(lines).rstrip() + '\n'


def llms(pages):
    """llms.txt: a plain summary for AI tools, in the format the solar site uses."""
    out = [f'# {NAME}', '',
           '> A free tool for analysing UK half-hourly (HH) electricity meter data. Load one Excel or CSV file per meter and see '
           'out-of-hours use priced at your rates, base load, peaks against agreed supply capacity, unusual days and lasting '
           'changes, with savings scenarios, PDF and Excel reports and password-protected customer dashboards.', '',
           f'Operated by {OPERATOR}. Free to use, no sign-up. The analyser runs entirely in the browser: meter data is never uploaded.', '',
           'Scope: UK businesses and public sector organisations. Results are indicative estimates from the data loaded: costs are '
           'energy cost at the rates entered, not guaranteed savings, and whole-site data shows when energy is used, not which '
           'equipment uses it. The method is set out on the How it works page.', '',
           'Method in brief: base load is the 5th percentile of valid half-hourly demand; out-of-hours (closed-hours) excess is '
           'energy used outside the opening hours above that base load; missing readings are left out, never counted as zero; '
           'annual figures are scaled from valid hours and withheld under 180 days of data; kVA is kW divided by an assumed power factor.', '']
    out += ['## Tool', '', f'- [Analyser]({url("analyser/")}): the tool itself, in the browser.', '']
    for section in ['Core pages', 'Guides', 'Sectors']:
        items = [p for p in pages if p.section == section and p.summary]
        if items:
            out += [f'## {section}', ''] + [f'- [{p.title.split(" | ")[0]}]({url(p.file)}): {p.summary}' for p in items] + ['']
    out += ['## Related', '', f'- [UK Solar Calculator]({kit.SOLAR_URL}): sister site from the same team, for commercial solar PV estimates.', '']
    return '\n'.join(out)


def fingerprint(p):
    """What a reader sees: title, description and body (not the layout around it)."""
    return hashlib.sha256('\n'.join([p.title, p.description, p.body]).encode()).hexdigest()[:16]


def update_dates(pages):
    """Give a page today's date when its content changes; keep it otherwise."""
    today = dt.date.today().isoformat()
    old = json.loads(DATES_FILE.read_text()) if DATES_FILE.exists() else {}
    new = {}
    for p in pages:
        h, prev = fingerprint(p), old.get(p.file)
        if prev is None:
            new[p.file] = {'published': today, 'modified': today, 'fingerprint': h}
        elif prev['fingerprint'] != h:
            new[p.file] = {**prev, 'modified': today, 'fingerprint': h}
        else:
            new[p.file] = prev
    DATES_FILE.write_text(json.dumps(dict(sorted(new.items())), indent=1) + '\n')
    kit.PAGE_DATES.update(new)


def sitemap(pages):
    rows = ''.join(f'  <url><loc>{url(p.file)}</loc><lastmod>{kit.page_dates(p.file)[1]}</lastmod></url>\n'
                   for p in pages if not p.noindex)
    rows += f'  <url><loc>{url("analyser/")}</loc><lastmod>{max(d["modified"] for d in kit.PAGE_DATES.values())}</lastmod></url>\n'
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}</urlset>\n'


def main():
    pages = core_pages() + GUIDE_PAGES + DATA_PAGES
    update_dates(pages)
    for p in pages:
        (SITE / p.file).write_text(layout(p), encoding='utf-8')
    (SITE / 'robots.txt').write_text(robots(), encoding='utf-8')
    (SITE / 'llms.txt').write_text(llms(pages), encoding='utf-8')
    if SITE_URL:
        (SITE / 'sitemap.xml').write_text(sitemap(pages), encoding='utf-8')
    print(f'wrote {len(pages)} pages, robots.txt, llms.txt' + (', sitemap.xml' if SITE_URL else ' (sitemap waits for SITE_URL)'))


if __name__ == '__main__':
    main()
