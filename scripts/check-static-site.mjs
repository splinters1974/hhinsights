#!/usr/bin/env node
// Phase 1 static-site checks. No external packages or network requests.
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve('site');
const publicOrigin = 'https://halfhourlyinsights.netlify.app';
const errors = [];
const warnings = [];
const htmlFiles = fs.readdirSync(root).filter(n => n.endsWith('.html'));
const checkedLinks = new Set();
const assetNames = [
 'guides','get-your-data','example-office-analysis','example-school-analysis',
 'reading-a-heatmap','out-of-hours-electricity','base-load','supply-capacity',
 'proving-savings','half-hourly-settlement','glossary','how-it-works',
 'schools-electricity','offices-council-buildings','leisure-centres',
 'healthcare-electricity','industrial-warehouses','retail-hospitality',
 'sectors','estate-town','town-street','faq','contact','contact-photo','og-image'
];
for (const name of assetNames) {
 const file = path.join(root, 'images/phase1', name + '.svg');
 if (!fs.existsSync(file)) {errors.push('Missing phase-1 asset: ' + name);continue;}
 const svg = fs.readFileSync(file, 'utf8');
 if (!svg.startsWith('<svg') || !svg.includes('base64,') || svg.includes('<script')) errors.push('Invalid staged SVG: ' + name);
}
// Verify the native raster files actually used by the live pages and social cards.
const photoNames = new Set(['estate-town','town-street','contact-photo']);
for (const name of assetNames) {
 const rel = name === 'og-image' ? 'images/og-image.png'
   : photoNames.has(name) ? 'images/photos/'+name+'.jpg'
   : 'images/guides/'+name+'.jpg';
 const target = path.join(root, rel);
 if (!fs.existsSync(target)) {errors.push('Missing native raster: '+rel); continue;}
 const data = fs.readFileSync(target);
 const isPng = name === 'og-image';
 const valid = isPng
   ? data.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10]))
   : data[0] === 0xff && data[1] === 0xd8;
 if (!valid || data.length < 1000) errors.push('Invalid native image: '+rel);
}
for (const name of htmlFiles) {
 const full = path.join(root, name);
 const text = fs.readFileSync(full, 'utf8');
 const isUtility = name === '404.html' || name === 'thanks.html';
 if (!isUtility && !text.includes('rel="canonical"')) errors.push(name + ': no canonical URL');
 if (!isUtility && !text.includes('property="og:url"')) errors.push(name + ': no Open Graph URL');
 if (!isUtility && !/<meta property="og:image" content="https:\/\//.test(text)) errors.push(name + ': social image URL not absolute');
 if (/\[Retention period|PLACEHOLDER|FIXME/.test(text)) errors.push(name + ': draft placeholder found');
 for (const [, attr, value] of text.matchAll(/(?:\s|^)(href|src)="([^"]+)"/g)) {
  if (!value || value.startsWith('#') || /^(https?:|mailto:|tel:|data:|javascript:)/i.test(value)) continue;
  const clean = value.split(/[?#]/)[0];
  if (!clean || clean.startsWith('/')) continue;
  const resolved = path.resolve(path.dirname(full), clean);
  const key = name + ' -> ' + clean;
  if (!resolved.startsWith(root + path.sep)) {errors.push('Path outside site: ' + key);continue;}
  if (!fs.existsSync(resolved)) errors.push('Broken reference: ' + key);
  else checkedLinks.add(clean);
 }
}
const home = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
if (!home.includes('href="sample-report.html"')) errors.push('Homepage missing sample report CTA');
const sample = fs.readFileSync(path.join(root, 'sample-report.html'), 'utf8');
if (!sample.includes('made-up office') && !sample.includes('fictional meter data')) errors.push('Sample report not clearly fictional');
const privacy = fs.readFileSync(path.join(root, 'privacy.html'), 'utf8');
if (privacy.includes('[Retention period')) errors.push('Privacy placeholder remains');
const robots = fs.readFileSync(path.join(root, 'robots.txt'), 'utf8');
if (!robots.includes('Sitemap: ' + publicOrigin + '/sitemap.xml')) errors.push('robots.txt missing sitemap');
const sitemap = fs.readFileSync(path.join(root, 'sitemap.xml'), 'utf8');
if (!sitemap.includes('<urlset') || sitemap.includes('/thanks.html')) errors.push('Sitemap invalid or includes noindex thanks page');
if (!fs.existsSync(path.join(root, 'analyser/index.html'))) warnings.push('Analyser entry not found at site/analyser/index.html; verify actual build layout');
console.log(JSON.stringify({htmlPages:htmlFiles.length,stagedImages:assetNames.length,checkedUniqueLinks:checkedLinks.size,errors,warnings},null,2));
if (errors.length) process.exit(1);
