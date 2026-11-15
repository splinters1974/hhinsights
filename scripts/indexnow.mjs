#!/usr/bin/env node
// Tell Bing (and other IndexNow search engines) which pages are new or changed,
// so they are crawled straight away. Bing's index also feeds ChatGPT search
// and Copilot.
//
// SWITCHED OFF until launch: the brief is not to submit pages for indexing
// until the final domain is live. To use it, set SITE_URL in tools/kit.py to
// the final domain, deploy, then run:
//
//   INDEXNOW_ENABLED=1 node scripts/indexnow.mjs            # every page in the sitemap
//   INDEXNOW_ENABLED=1 node scripts/indexnow.mjs about faq  # just these pages
//
// or the "Notify search engines (IndexNow)" workflow in GitHub Actions.
// The key file site/b73d5d5500eab79bfcc73f3ffc5f8ae4.txt must be live at the site root.
import fs from 'node:fs';

const KEY = 'b73d5d5500eab79bfcc73f3ffc5f8ae4';
const kit = fs.readFileSync('tools/kit.py', 'utf8');
const origin = (kit.match(/^SITE_URL = '([^']*)'/m) || [])[1];

if (process.env.INDEXNOW_ENABLED !== '1') {
  console.log('IndexNow is switched off. Set INDEXNOW_ENABLED=1 once the final domain is live.');
  process.exit(0);
}
if (!origin || /netlify\.app/.test(origin)) {
  console.error(`Refusing to submit: SITE_URL is ${origin || 'empty'}, not the final domain.`);
  process.exit(1);
}
if (!fs.existsSync(`site/${KEY}.txt`)) { console.error('Key file missing from site/'); process.exit(1); }

const only = process.argv.slice(2);
const sitemap = fs.readFileSync('site/sitemap.xml', 'utf8');
const all = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
const urlList = only.length ? only.map((p) => `${origin}/${p.replace(/^\//, '')}`) : all;

const res = await fetch('https://api.indexnow.org/indexnow', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json; charset=utf-8' },
  body: JSON.stringify({ host: new URL(origin).host, key: KEY, keyLocation: `${origin}/${KEY}.txt`, urlList }),
});
console.log(`IndexNow: HTTP ${res.status} for ${urlList.length} URL(s)`);
process.exit(res.ok || res.status === 202 ? 0 : 1);
