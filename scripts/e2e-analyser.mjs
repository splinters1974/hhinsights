#!/usr/bin/env node
// End-to-end checks for the built analyser (site/analyser/index.html) in a real
// browser, served locally. Loads the example files (CSV and an Excel copy),
// checks the figures the website quotes, downloads every PDF and Excel export
// and records every network request: the site promises that meter data never
// leaves the computer, so any request to another host fails the run.
//
// Needs Playwright and the analyser's npm packages (for reading the Excel
// exports): run `npm ci` in analyser/ first.
import { spawn } from 'node:child_process';
import { createRequire } from 'node:module';
import { setTimeout as delay } from 'node:timers/promises';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const XLSX = createRequire(path.resolve('analyser/package.json'))('xlsx');

const PORT = 8766;
const base = `http://127.0.0.1:${PORT}/`;
const app = base + 'analyser/';
const shots = 'site-screenshots';
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'hhi-e2e-'));
const errors = [];
const passed = [];
const check = (ok, msg) => (ok ? passed.push(msg) : errors.push(msg));

// Test files: the published examples, an Excel copy of the office file and a junk file.
const officeCsv = 'site/samples/example-office.csv';
const schoolCsv = 'site/samples/example-school.csv';
const officeXlsx = path.join(tmp, 'example-office-copy.xlsx');
{
  const rows = fs.readFileSync(officeCsv, 'utf8').trim().split(/\r?\n/).map((l) => l.split(','));
  const aoa = rows.map((r, i) => (i === 0 ? r : [r[0], ...r.slice(1).map(Number)]));
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(aoa), 'Readings');
  XLSX.writeFile(wb, officeXlsx);
}
const junk = path.join(tmp, 'notes.csv');
fs.writeFileSync(junk, 'Meeting notes\nNothing to see here,really\n');

fs.mkdirSync(shots, { recursive: true });
const server = spawn('python3', ['scripts/serve.py', String(PORT)], { stdio: 'ignore' });
async function waitForServer() {
  for (let i = 0; i < 50; i++) { try { if ((await fetch(base)).ok) return; } catch {} await delay(200); }
  throw new Error('local server did not start');
}

const external = [];
const pageErrors = [];
async function newPage(browser, opts = {}) {
  const context = await browser.newContext({ acceptDownloads: true, locale: 'en-GB', viewport: { width: 1366, height: 900 }, ...opts });
  context.on('request', (r) => { const u = r.url(); if (!u.startsWith(base) && !/^(data|blob):/.test(u)) external.push(u); });
  const page = await context.newPage();
  page.on('pageerror', (e) => pageErrors.push(String(e)));
  page.on('dialog', (d) => d.accept());
  await page.goto(app, { waitUntil: 'load' });
  await page.waitForSelector('input[type=file][multiple]', { state: 'attached', timeout: 20000 });
  return { context, page };
}
const upload = (page, files) => page.locator('input[type=file][multiple]').setInputFiles(files);
const text = (page) => page.locator('body').innerText();

async function download(page, buttonName, label) {
  const [dl] = await Promise.all([
    page.waitForEvent('download', { timeout: 60000 }),
    page.getByRole('button', { name: buttonName, exact: true }).click(),
  ]);
  const file = path.join(tmp, `${label}-${dl.suggestedFilename()}`);
  await dl.saveAs(file);
  return { file, name: dl.suggestedFilename(), bytes: fs.readFileSync(file) };
}
function checkPdf(d, label) {
  const head = d.bytes.subarray(0, 5).toString();
  const pages = (d.bytes.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
  check(head === '%PDF-' && d.bytes.length > 20000 && pages >= 1, `${label}: valid PDF (${d.name}, ${Math.round(d.bytes.length / 1024)} KB, ${pages} pages)`);
}
function checkXlsx(d, label, mustContain) {
  let wb;
  try { wb = XLSX.read(d.bytes, { type: 'buffer' }); } catch (e) { check(false, `${label}: Excel file opens (${e.message})`); return; }
  const all = wb.SheetNames.map((n) => XLSX.utils.sheet_to_csv(wb.Sheets[n])).join('\n');
  check(wb.SheetNames.length > 0, `${label}: Excel file opens (${d.name}; sheets: ${wb.SheetNames.join(', ')})`);
  for (const [what, re] of mustContain) check(re.test(all), `${label}: Excel contains ${what}`);
}

let browser;
try {
  await waitForServer();
  browser = await chromium.launch();

  // 1. Office CSV: figures match the sample report, every export downloads.
  {
    const { context, page } = await newPage(browser);
    await upload(page, officeCsv);
    await page.getByText('£2,776').first().waitFor({ timeout: 30000 });
    const t = await text(page);
    check(/£2,776/.test(t) && /£19,798/.test(t) && /79,191/.test(t) && /33%/.test(t), 'office CSV: portfolio shows £2,776, £19,798, 79,191 kWh and 33%, as the sample report says');
    check(/not a guaranteed saving/i.test(t), 'office CSV: closed-hours cost labelled as not a guaranteed saving');
    const stored = await page.evaluate(async () => ({ idb: (await indexedDB.databases()).length, ls: localStorage.length, ss: sessionStorage.length, cookie: document.cookie }));
    check(stored.idb === 0 && stored.ls === 0 && stored.ss === 0 && stored.cookie === '', `nothing stored in the browser, as the privacy notice says (${JSON.stringify(stored)})`);
    await page.screenshot({ path: `${shots}/analyser-portfolio.png` });

    checkPdf(await download(page, 'Portfolio report (PDF)', 'portfolio'), 'portfolio report');
    checkXlsx(await download(page, 'Export to Excel', 'portfolio'), 'portfolio Excel', [['annual kWh 79,191', /79,?191/], ['the site name', /example-office/]]);
    checkXlsx(await download(page, 'Table to Excel', 'table'), 'sites table Excel', [['£2,776 excess', /2,?776/]]);

    await page.getByText('example-office', { exact: true }).first().click();
    await page.getByRole('button', { name: 'Site summary (PDF)' }).waitFor();
    const s = await text(page);
    check(/2\.6 kW/.test(s) && /25\.5 kW/.test(s) && /99\.5%/.test(s), 'office CSV: site view shows base load 2.6 kW, peak 25.5 kW, 99.5% coverage');
    check(/£629/.test(s) && /£5,698/.test(s) && /7 bank holidays/.test(s), 'office CSV: findings match the sample report (£629, £5,698, 7 bank holidays)');
    await page.screenshot({ path: `${shots}/analyser-site.png`, fullPage: false });
    checkPdf(await download(page, 'Site summary (PDF)', 'site'), 'site summary');
    await page.locator('button', { hasText: /^Data review/ }).first().click();
    await page.getByText('Clock changes').first().waitFor({ timeout: 10000 });
    check(/2 clock-change days \(2024-10-27, 2025-03-30\)/.test(await text(page)), 'office CSV: both clock-change days held back and shown on the data review tab');
    checkXlsx(await download(page, 'Export to Excel', 'site'), 'site Excel', [['annual kWh 79,191', /79,?191/]]);
    // Solar: the Solar tab estimates self-consumption and links to the calculator with a summary after the #.
    await page.locator('button', { hasText: /^Overview/ }).first().click();
    check(/Solar:.*kWp system would supply about/.test(await text(page)), 'site overview shows a one-line solar estimate pointing to the Solar tab');
    await page.getByRole('button', { name: 'See the Solar tab →' }).click();
    await page.getByText('Solar: how much would you use?').waitFor({ timeout: 10000 });
    const solarHref = await page.getByRole('link', { name: /Size solar for this site/ }).getAttribute('href');
    check(/^https:\/\/uksolarcalculator\.co\.uk\/calculator\.html#hhi=1&y=905&use=\d+&sc=[\d.:,]+$/.test(solarHref || '') && solarHref.length < 300,
      `solar hand-off link carries only a short summary after the # (${(solarHref || '').slice(0, 70)}...)`);
    await page.screenshot({ path: `${shots}/analyser-solar.png`, fullPage: false });
    await context.close();
  }

  // 1b. The All sites page points to solar, and its button opens the Solar tab.
  {
    const { context, page } = await newPage(browser);
    await upload(page, officeCsv);
    await page.getByText('£2,776').first().waitFor({ timeout: 30000 });
    check(/Thinking about solar\?/.test(await text(page)), 'All sites page has a solar pointer');
    await page.getByRole('button', { name: 'Open the Solar tab →' }).click();
    await page.getByText('Solar: how much would you use?').waitFor({ timeout: 10000 });
    check(true, 'solar pointer opens the site on its Solar tab');
    await context.close();
  }

  // 2. The same readings as Excel give the same answer; a second meter adds to the estate.
  {
    const { context, page } = await newPage(browser);
    await upload(page, [officeXlsx, schoolCsv]);
    await page.getByText('example-office-copy', { exact: true }).first().waitFor({ timeout: 30000 });
    await page.getByText(/2 meters/).first().waitFor({ timeout: 30000 }).catch(() => {});
    const t = await text(page);
    check(/example-office-copy/.test(t) && /£2,776/.test(t) && /79,191/.test(t), 'Excel copy of the office file: same £2,776 and 79,191 kWh as the CSV');
    check(/example-school/.test(t) && /2 meters/.test(t), 'school CSV loads alongside as a second meter');
    await context.close();
  }

  // 3. The same file twice is refused, so totals cannot double.
  {
    const { context, page } = await newPage(browser);
    await upload(page, officeCsv);
    await page.getByText('£2,776').first().waitFor({ timeout: 30000 });
    await upload(page, officeCsv);
    await delay(2500);
    const t = await text(page);
    check(/already loaded/.test(t) && /not doubled/.test(t) && /1 meter\b/.test(t) && !/2 meters/.test(t), 'loading the same file twice is refused with a message, one meter kept (no double counting)');
    await context.close();
  }

  // 4. A file that is not meter data gives a message, not a crash.
  {
    const { context, page } = await newPage(browser);
    const before = pageErrors.length;
    await upload(page, junk);
    await delay(2500);
    const t = await text(page);
    check(/notes\.csv/.test(t) && /Drag and drop/.test(t), 'a non-meter file is rejected with a message naming it');
    check(pageErrors.length === before, 'a non-meter file causes no script error');
    await context.close();
  }

  // 5. Phone width: loads a file and fits the screen.
  {
    const { context, page } = await newPage(browser, { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
    await upload(page, officeCsv);
    await page.getByText('£2,776').first().waitFor({ timeout: 30000 });
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    check(overflow <= 1, `phone: results fit the screen width (overflow ${overflow}px)`);
    await page.screenshot({ path: `${shots}/analyser-mobile.png` });
    await context.close();
  }
} catch (e) {
  errors.push(`test run failed: ${e.message}`);
} finally {
  await browser?.close();
  server.kill('SIGTERM');
}

check(external.length === 0, `no network requests to any other site during upload, analysis and export${external.length ? ': ' + [...new Set(external)].join(', ') : ''}`);
check(pageErrors.length === 0, `no script errors${pageErrors.length ? ': ' + pageErrors.join(' | ') : ''}`);
console.log(JSON.stringify({ passed: passed.length, failed: errors.length, errors, passedChecks: passed }, null, 2));
process.exit(errors.length ? 1 : 0);
