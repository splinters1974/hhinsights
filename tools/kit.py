"""
Shared pieces for the page builder: site settings, the page layout, and the
structured data (schema.org JSON-LD) every page carries.
"""
import json
from dataclasses import dataclass, field
from html import escape

NAME = 'Half Hourly Insights'
YEAR = 2026
# Date the guides were last reviewed; shown on each guide and in its schema.
UPDATED = '2026-11-14'
UPDATED_TEXT = '14 November 2026'
# Domain to be confirmed. Leave empty until then: once set (e.g.
# 'https://www.example.co.uk', no trailing slash) every page gains canonical and
# absolute share links, robots.txt points at the sitemap, and sitemap.xml is written.
SITE_URL = ''

# Run by Kinetic Energy Consulting, as with the UK Solar Calculator.
OPERATOR = 'Kinetic Energy Consulting'
OPERATOR_URL = 'https://www.kinetic-energy.co.uk'
CONTACT_NAME = 'Paul Johnston'
CONTACT_EMAIL = 'pjohnston663@gmail.com'
SOLAR_URL = 'https://uksolarcalculator.co.uk/'

MARK = ('<svg viewBox="0 0 34 34" aria-hidden="true">'
        '<rect x="3" y="15" width="5" height="10" rx="1" fill="#0065A4"/>'
        '<rect x="10" y="9" width="5" height="16" rx="1" fill="#0065A4"/>'
        '<rect x="17" y="3" width="5" height="22" rx="1" fill="#F8C05D"/>'
        '<rect x="24" y="12" width="5" height="13" rx="1" fill="#0065A4"/>'
        '<rect x="1" y="26" width="32" height="3" rx="1.5" fill="{base}"/></svg>')

NAV = [
    ('index.html', 'Home'),
    ('how-it-works.html', 'How it works'),
    ('guides.html', 'Guides'),
    ('sectors.html', 'Sectors'),
    ('faq.html', 'FAQ'),
    ('contact.html', 'Contact'),
]
# Pages that belong under a nav item, so it stays highlighted on them.
NAV_PARENT = {}


def url(path):
    """Absolute URL once the domain is set, otherwise the relative path."""
    if not SITE_URL:
        return path
    return f'{SITE_URL}/' if path == 'index.html' else f'{SITE_URL}/{path}'


@dataclass
class Page:
    file: str
    title: str
    description: str
    body: str
    crumbs: list = field(default_factory=list)   # [(label, file)], home first, this page last
    faqs: list = field(default_factory=list)     # [(question, answer html)], marked up as FAQPage
    article: bool = False                        # a guide: gets Article schema with dates
    schema: list = field(default_factory=list)   # extra JSON-LD nodes
    noindex: bool = False
    extra_head: str = ''
    summary: str = ''                            # one line for llms.txt; empty leaves it out
    section: str = ''                            # llms.txt heading


# ── Structured data ────────────────────────────────────────────────────
ORG_ID = f'{OPERATOR_URL}/#organization'
ORG = {
    '@type': 'Organization', '@id': ORG_ID, 'name': OPERATOR, 'url': OPERATOR_URL,
    'email': CONTACT_EMAIL, 'sameAs': ['https://www.linkedin.com/company/kinetic-energy-consulting'],
    'areaServed': {'@type': 'Country', 'name': 'United Kingdom'},
    'contactPoint': {'@type': 'ContactPoint', 'contactType': 'Sales', 'email': CONTACT_EMAIL, 'areaServed': 'GB'},
}
WEBSITE = {
    '@type': 'WebSite', '@id': '#website', 'name': NAME, 'inLanguage': 'en-GB',
    'description': 'Free half-hourly electricity analysis for UK businesses and public bodies',
    'publisher': {'@id': ORG_ID},
}
APP = {
    '@type': 'WebApplication', 'name': f'{NAME} analyser', 'url': url('analyser/'),
    'applicationCategory': 'BusinessApplication', 'operatingSystem': 'Any (runs in Chrome or Edge)',
    'browserRequirements': 'A recent desktop browser; works offline once loaded',
    'isAccessibleForFree': True, 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'GBP'},
    'description': ('Analyses UK half-hourly electricity meter data in the browser: out-of-hours use, base load, '
                    'peaks against supply capacity, unusual days, savings scenarios, PDF and Excel reports. '
                    'Meter data is never uploaded.'),
    'featureList': ['Excel and CSV half-hourly files', 'Data quality checks', 'Out-of-hours use priced at your rates',
                    'Base load', 'Supply capacity and headroom', 'Unusual days', 'Savings scenarios',
                    'PDF and Excel reports', 'Password-protected customer dashboards'],
    'provider': {'@id': ORG_ID},
}
if SITE_URL:
    WEBSITE['url'] = url('index.html')
    WEBSITE['@id'] = f'{SITE_URL}/#website'


def strip_tags(html):
    import re
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', html)).strip()


def jsonld(page):
    graph = [ORG, WEBSITE]
    if page.crumbs:
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': label, 'item': url(href)}
            for i, (label, href) in enumerate(page.crumbs)]})
    if page.article:
        graph.append({'@type': 'Article', 'headline': page.title.split(' | ')[0], 'description': page.description,
                      'inLanguage': 'en-GB', 'datePublished': UPDATED, 'dateModified': UPDATED,
                      'author': {'@id': ORG_ID}, 'publisher': {'@id': ORG_ID},
                      'isPartOf': {'@id': WEBSITE['@id']}, **({'mainEntityOfPage': url(page.file)} if SITE_URL else {})})
    if page.faqs:
        graph.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': strip_tags(a)}}
            for q, a in page.faqs]})
    graph += page.schema
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)
    return f'  <script type="application/ld+json">\n{data}\n  </script>\n'


# ── Building blocks ────────────────────────────────────────────────────
def page_hero(kicker, title, lead, extra='', crumbs=None):
    trail = ''
    if crumbs:
        trail = '<nav class="breadcrumb" aria-label="Breadcrumb">' + ' <span aria-hidden="true">/</span> '.join(
            f'<a href="{href}">{escape(label)}</a>' if i < len(crumbs) - 1 else f'<span aria-current="page">{escape(label)}</span>'
            for i, (label, href) in enumerate(crumbs)) + '</nav>\n    '
    return f'''<section class="page-hero">
  <div class="page-hero-inner">
    {trail}<span class="page-hero-kicker">{kicker}</span>
    <h1 class="page-hero-title">{title}</h1>
    <p class="page-hero-lead">{lead}</p>{extra}
  </div>
</section>'''


def cta(title, lead):
    return f'''<section class="cta-strip">
  <div class="cta-strip-inner">
    <h2 class="cta-strip-title">{title}</h2>
    <div class="cta-strip-btns">
      <a href="analyser/" class="btn btn-gold btn-lg">Open the analyser</a>
      <a href="contact.html" class="btn btn-outline-white btn-lg">Talk to an expert</a>
    </div>
    <p class="cta-strip-lead">{lead}</p>
  </div>
</section>'''


def faq_section(faqs, title='Questions people ask'):
    """Visible questions and answers; the same list feeds the FAQPage schema."""
    return f'<h2 id="questions">{title}</h2>\n<div class="faq">' + ''.join(
        f'<details><summary>{q}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faqs) + '</div>'


def related(links):
    """'Read next' cards at the end of a guide: [(file, title, one line)]."""
    return '<h2 id="next">Read next</h2>\n<div class="link-grid">' + ''.join(
        f'<a class="link-card" href="{f}"><h3>{t}</h3><p>{d}</p><span class="more">Read the guide</span></a>'
        for f, t, d in links) + '</div>'


def updated_line():
    return f'<p class="byline">Last updated <time datetime="{UPDATED}">{UPDATED_TEXT}</time></p>'


def toc(items):
    return ('    <nav class="toc" aria-label="On this page"><div class="toc-title">On this page</div><ol>'
            + ''.join(f'<li><a href="#{a}">{t}</a></li>' for a, t in items) + '</ol></nav>')


def guide(main, side=''):
    return f'''<div class="guide">
  <article class="guide-main prose">
{main}
  </article>
  <aside class="guide-side">
{side}
    <div class="side-cta"><strong>Try it on your own data</strong><p>Free, no sign-up, and your file stays on your computer.</p><a href="analyser/" class="btn">Open the analyser</a></div>
  </aside>
</div>'''


def layout(page):
    current = NAV_PARENT.get(page.file, page.file)
    active = ' class="active" aria-current="page"'
    links = ''.join(f'<li><a href="{href}"{active if href == current else ""}>{label}</a></li>' for href, label in NAV)
    canonical = f'  <link rel="canonical" href="{url(page.file)}">\n  <meta property="og:url" content="{url(page.file)}">\n' if SITE_URL else ''
    robots = '  <meta name="robots" content="noindex">\n' if page.noindex else ''
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page.title}</title>
  <meta name="description" content="{escape(page.description)}">
{canonical}{robots}  <meta property="og:type" content="{'article' if page.article else 'website'}">
  <meta property="og:locale" content="en_GB">
  <meta property="og:title" content="{escape(page.title)}">
  <meta property="og:description" content="{escape(page.description)}">
  <meta property="og:image" content="{url('images/og-image.png')}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:site_name" content="{NAME}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/svg+xml" href="images/favicon.svg">
  <link rel="preload" href="fonts/schibsted-grotesk-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="css/site.css">
{jsonld(page)}{page.extra_head}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<nav class="site-nav" id="siteNav" aria-label="Main">
  <div class="nav-inner">
    <a href="index.html" class="nav-logo" aria-label="{NAME} home">
      {MARK.format(base='#063C55')}
      <span class="nav-logo-name">{NAME}</span>
    </a>
    <ul class="nav-links" id="navLinks">
      {links}
      <li><a href="analyser/" class="nav-cta">Open the analyser</a></li>
    </ul>
    <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false" aria-controls="navLinks">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>
<main id="main">
{page.body}
</main>
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="footer-logo">{MARK.format(base='#FFFFFF')}<span class="footer-logo-name">{NAME}</span></div>
        <p class="footer-desc">Free half-hourly electricity analysis for UK businesses and public sector organisations, run by {OPERATOR}. It runs in your browser: your meter data never leaves your computer.</p>
        <div class="footer-contact-item">Email: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></div>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Analyser</div>
        <ul><li><a href="analyser/">Open the analyser</a></li><li><a href="how-it-works.html">How it works</a></li><li><a href="example-office-analysis.html">Worked example</a></li><li><a href="samples/example-office.csv" download>Example data file</a></li><li><a href="faq.html">FAQ</a></li></ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Guides</div>
        <ul><li><a href="get-your-data.html">Getting your half-hourly data</a></li><li><a href="out-of-hours-electricity.html">Out-of-hours electricity use</a></li><li><a href="base-load.html">Base load</a></li><li><a href="supply-capacity.html">Supply capacity and kVA</a></li><li><a href="sectors.html">By sector</a></li></ul>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">About</div>
        <ul><li><a href="contact.html">Contact</a></li><li><a href="privacy.html">Privacy</a></li><li><a href="{SOLAR_URL}">UK Solar Calculator</a>, our sister site</li></ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="footer-copy">&copy; {YEAR} {OPERATOR}</div>
      <div class="footer-disclaimer">All analyser outputs are indicative estimates from the data you load, not a guarantee of savings. Guides are general information, not financial, tax or legal advice.</div>
    </div>
  </div>
</footer>
<script>
  document.getElementById('navToggle').addEventListener('click', function (e) {{
    var open = document.getElementById('siteNav').classList.toggle('nav-mobile-open');
    e.currentTarget.setAttribute('aria-expanded', open ? 'true' : 'false');
    e.currentTarget.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }});
</script>
</body>
</html>
'''
