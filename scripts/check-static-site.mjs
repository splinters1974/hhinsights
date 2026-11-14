#!/usr/bin/env node
// Static checks for the built site in site/. No packages, no network.
// Run after `python3 tools/build_pages.py`. Exits 1 on any error.
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve('site');
const kit = fs.readFileSync('tools/kit.py', 'utf8');
const origin = (kit.match(/^SITE_URL = '([^']*)'/m) || [])[1];
const errors = [];
const warnings = [];
const err = (m) => errors.push(m);

if (!origin) err('SITE_URL is empty in tools/kit.py: canonical links and the sitemap are disabled');

// The 25 approved images: 21 guide, sector and page cards, two scene
// illustrations, the contact photo and the default share image.
const cards = ['guides', 'get-your-data', 'example-office-analysis', 'example-school-analysis', 'reading-a-heatmap',
  'out-of-hours-electricity', 'base-load', 'supply-capacity', 'proving-savings', 'half-hourly-settlement', 'glossary',
  'how-it-works', 'schools-electricity', 'offices-council-buildings', 'leisure-centres', 'healthcare-electricity',
  'industrial-warehouses', 'retail-hospitality', 'sectors', 'faq', 'contact'];
const approved = [...cards.map((n) => `images/guides/${n}.jpg`),
  'images/photos/estate-town.jpg', 'images/photos/town-street.jpg', 'images/photos/contact-photo.jpg', 'images/og-image.png'];
if (approved.length !== 25) err(`expected 25 approved images, listed ${approved.length}`);

const isPng = (b) => b.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]));
const isJpg = (b) => b[0] === 0xff && b[1] === 0xd8;
for (const rel of approved) {
  const f = path.join(root, rel);
  if (!fs.existsSync(f)) { err(`missing approved image ${rel}`); continue; }
  const b = fs.readFileSync(f);
  if (!(rel.endsWith('.png') ? isPng(b) : isJpg(b)) || b.length < 5000) err(`not a valid image: ${rel}`);
}

const pages = fs.readdirSync(root).filter((n) => n.endsWith('.html')).sort();
const referenced = new Set();
const indexable = [];
const localTarget = (from, ref) => {
  const clean = ref.split(/[?#]/)[0];
  if (!clean) return null;
  return path.resolve(path.dirname(path.join(root, from)), clean);
};

for (const name of pages) {
  const html = fs.readFileSync(path.join(root, name), 'utf8');
  const noindex = /<meta name="robots" content="noindex">/.test(html);
  const title = (html.match(/<title>([^<]*)<\/title>/) || [])[1];
  const desc = (html.match(/<meta name="description" content="([^"]*)"/) || [])[1];
  if (!title) err(`${name}: no <title>`);
  if (!desc) err(`${name}: no meta description`);
  if ((html.match(/<h1[\s>]/g) || []).length !== 1) err(`${name}: should have exactly one <h1>`);
  if (/\[Retention period|\bPLACEHOLDER\b|\bFIXME\b|\bTODO\b|[Ll]orem ipsum/.test(html)) err(`${name}: draft placeholder text`);
  if (!/<html lang="en-GB">/.test(html)) err(`${name}: missing lang="en-GB"`);

  const canonical = (html.match(/<link rel="canonical" href="([^"]+)">/) || [])[1];
  const ogImage = (html.match(/<meta property="og:image" content="([^"]+)">/) || [])[1];
  if (noindex) {
    if (canonical) err(`${name}: noindex page should not declare a canonical URL`);
  } else {
    indexable.push(name);
    const expected = name === 'index.html' ? `${origin}/` : `${origin}/${name.replace(/\.html$/, '')}`;
    if (canonical !== expected) err(`${name}: canonical is ${canonical}, expected ${expected}`);
    if (!/<meta property="og:url" content="https:\/\//.test(html)) err(`${name}: og:url missing or not absolute`);
    if (!ogImage || !ogImage.startsWith(`${origin}/`)) err(`${name}: og:image missing or not on ${origin}`);
  }
  if (ogImage) {
    const rel = ogImage.replace(`${origin}/`, '');
    referenced.add(rel);
    if (!fs.existsSync(path.join(root, rel))) err(`${name}: og:image file not found: ${rel}`);
  }

  // Structured data must parse.
  for (const [, json] of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    try { JSON.parse(json); } catch (e) { err(`${name}: invalid JSON-LD (${e.message})`); }
  }

  // Every local href, src and srcset entry must exist; every <img> needs alt and a size.
  const refs = [...html.matchAll(/\s(?:href|src)="([^"]+)"/g)].map((m) => m[1]);
  for (const [, set] of html.matchAll(/\ssrcset="([^"]+)"/g)) refs.push(...set.split(',').map((s) => s.trim().split(/\s+/)[0]));
  for (const ref of refs) {
    if (/^(https?:|mailto:|tel:|data:|#)/.test(ref)) continue;
    const t = localTarget(name, ref);
    if (!t) continue;
    if (!t.startsWith(root)) { err(`${name}: link leaves the site: ${ref}`); continue; }
    // Clean addresses: /base-load is served from base-load.html, ./ from index.html.
    const exists = (fs.existsSync(t) && (fs.statSync(t).isFile() || fs.existsSync(path.join(t, 'index.html')))) || fs.existsSync(t + '.html');
    if (!exists) err(`${name}: broken reference ${ref}`);
    else referenced.add(path.relative(root, fs.existsSync(t + '.html') && !fs.existsSync(t) ? t + '.html' : t));
  }
  for (const [tag] of html.matchAll(/<img\b[^>]*>/g)) {
    if (!/\salt="/.test(tag)) err(`${name}: <img> without alt: ${tag.slice(0, 80)}`);
    if (!/\swidth="\d+"/.test(tag) || !/\sheight="\d+"/.test(tag)) err(`${name}: <img> without width/height: ${tag.slice(0, 80)}`);
  }
  // Same-page anchors must point at an id on the page.
  for (const [, id] of html.matchAll(/href="#([^"]+)"/g)) if (!html.includes(`id="${id}"`)) err(`${name}: anchor #${id} has no target`);
}

for (const rel of approved) if (!referenced.has(rel)) err(`approved image not used on any page: ${rel}`);

// Sitemap and robots.
const sitemap = fs.existsSync(path.join(root, 'sitemap.xml')) ? fs.readFileSync(path.join(root, 'sitemap.xml'), 'utf8') : '';
const locs = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
for (const name of indexable) {
  const u = name === 'index.html' ? `${origin}/` : `${origin}/${name.replace(/\.html$/, '')}`;
  if (!locs.includes(u)) err(`sitemap missing ${u}`);
}
for (const u of locs) {
  if (!u.startsWith(`${origin}/`)) err(`sitemap URL on the wrong host: ${u}`);
  if (/\/(thanks|404)(\.html)?$/.test(u)) err(`sitemap lists a noindex page: ${u}`);
}
const robots = fs.readFileSync(path.join(root, 'robots.txt'), 'utf8');
if (!robots.includes(`Sitemap: ${origin}/sitemap.xml`)) err('robots.txt does not point at the sitemap');
if (/Disallow:\s*\/\s*$/m.test(robots)) err('robots.txt blocks the whole site');

// Content safeguards.
const read = (n) => fs.readFileSync(path.join(root, n), 'utf8');
if (!read('index.html').includes('href="sample-report"')) err('home page does not link to the sample report');
if (!/Made-up example/.test(read('sample-report.html'))) err('sample report is not labelled as made-up');
if (!/not a promised saving/.test(read('sample-report.html'))) err('sample report does not separate cost from saving');
const contact = read('contact.html');
if (!/<form[^>]+action="https:\/\/formspree\.io\/f\/[a-z0-9]+"/i.test(contact)) err('contact form is not wired to Formspree');
if (!/name="_gotcha"/.test(contact)) err('contact form has no spam honeypot');
if (!/href="mailto:/.test(contact)) err('contact page has no email fallback');
if (/data-netlify/.test(contact)) err('contact form still carries Netlify Forms attributes');
if (!fs.existsSync(path.join(root, 'analyser/index.html'))) err('analyser missing at site/analyser/index.html');
if (!fs.existsSync(path.join(root, 'downloads/half-hourly-insights-user-guide.pdf'))) err('user guide PDF missing');

const unused = fs.readdirSync(path.join(root, 'images/guides')).filter((f) => !f.endsWith('-600.jpg'))
  .map((f) => `images/guides/${f}`).filter((r) => !referenced.has(r));
if (unused.length) warnings.push(`card images not referenced by any page: ${unused.join(', ')}`);

console.log(JSON.stringify({ origin, pages: pages.length, indexable: indexable.length, sitemapUrls: locs.length,
  approvedImages: approved.length, errors, warnings }, null, 2));
process.exit(errors.length ? 1 : 0);
