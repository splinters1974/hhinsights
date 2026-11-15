#!/usr/bin/env node
// Browser smoke tests for the built site in site/, served locally (never the
// live website). Desktop and mobile. Saves screenshots to site-screenshots/.
//
// Images: the home page banner drifts on a CSS animation, so nothing here
// waits for elements to be "stable". The browser runs with reduced motion
// (the site then holds the banner still), lazy images are switched to eager
// and each image's load outcome is awaited directly, without scrolling.
import { spawn } from 'node:child_process';
import { createRequire } from 'node:module';
import { setTimeout as delay } from 'node:timers/promises';
import fs from 'node:fs';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const PORT = 8765;
const base = `http://127.0.0.1:${PORT}/`;
const out = 'site-screenshots';
// Clean addresses, as the live host serves them (/guides serves guides.html).
const pages = ['', 'guides', 'sectors', 'sample-report', 'contact', 'how-it-works', 'about', 'business-electricity-price', 'analyser/'];
const views = [{ label: 'desktop', width: 1366, height: 900 }, { label: 'mobile', width: 390, height: 844, mobile: true }];
const errors = [];
const passed = [];
const check = (ok, msg) => (ok ? passed.push(msg) : errors.push(msg));

fs.mkdirSync(out, { recursive: true });
const server = spawn('python3', ['scripts/serve.py', String(PORT)], { stdio: 'ignore' });

async function waitForServer() {
  for (let i = 0; i < 50; i++) {
    try { if ((await fetch(base)).ok) return; } catch {}
    await delay(200);
  }
  throw new Error('local server did not start');
}

// Load every image on the page and report any that fail.
async function imageReport(page) {
  return page.evaluate(async () => {
    const imgs = [...document.images];
    for (const img of imgs) img.loading = 'eager';
    await Promise.all(imgs.map((img) => (img.complete ? null : new Promise((res) => {
      img.addEventListener('load', res, { once: true });
      img.addEventListener('error', res, { once: true });
      setTimeout(res, 15000);
    }))));
    return {
      total: imgs.length,
      broken: imgs.filter((i) => !i.complete || i.naturalWidth === 0).map((i) => i.getAttribute('src')),
      noAlt: imgs.filter((i) => !i.hasAttribute('alt')).map((i) => i.getAttribute('src')),
    };
  });
}

let browser;
try {
  await waitForServer();
  browser = await chromium.launch();
  for (const view of views) {
    const context = await browser.newContext({
      viewport: { width: view.width, height: view.height }, isMobile: !!view.mobile, hasTouch: !!view.mobile,
      reducedMotion: 'reduce', locale: 'en-GB',
    });
    const page = await context.newPage();
    const pageErrors = [];
    const external = [];
    page.on('pageerror', (e) => pageErrors.push(String(e)));
    page.on('console', (m) => { if (m.type() === 'error') pageErrors.push(m.text()); });
    page.on('request', (r) => { if (!r.url().startsWith(base) && !r.url().startsWith('data:') && !r.url().startsWith('blob:')) external.push(r.url()); });

    for (const route of pages) {
      const tag = `${view.label} /${route}`;
      pageErrors.length = 0; external.length = 0;
      const resp = await page.goto(base + route, { waitUntil: 'load', timeout: 60000 });
      check(resp?.status() === 200, `${tag}: loads (HTTP ${resp?.status()})`);

      if (route === 'analyser/') {
        await page.waitForSelector('input[type=file]', { state: 'attached', timeout: 20000 });
        check(/Half Hourly Insights/.test(await page.title()), `${tag}: analyser title`);
        check(await page.locator('input[type=file]').count() > 0, `${tag}: upload control present`);
      } else {
        const imgs = await imageReport(page);
        check(imgs.broken.length === 0, `${tag}: all ${imgs.total} images load${imgs.broken.length ? ' (broken: ' + imgs.broken.join(', ') + ')' : ''}`);
        check(imgs.noAlt.length === 0, `${tag}: every image has alt text`);
        check(await page.locator('h1').count() === 1, `${tag}: exactly one h1`);
        check(await page.locator('a.skip[href="#main"]').count() === 1 && await page.locator('#main').count() === 1, `${tag}: skip link to main content`);
        check(await page.locator('nav[aria-label="Main"] a[href="analyser/"]').count() > 0, `${tag}: main navigation links to the analyser`);
      }
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      check(overflow <= 1, `${tag}: no sideways scrolling (overflow ${overflow}px)`);
      check(pageErrors.length === 0, `${tag}: no script errors${pageErrors.length ? ': ' + pageErrors.join(' | ') : ''}`);
      check(external.length === 0, `${tag}: no requests to other sites${external.length ? ': ' + external.join(', ') : ''}`);

      if (route === '') {
        check(/business/i.test(await page.locator('h1').innerText()), `${tag}: headline names the business audience`);
        check(await page.locator('.hero-audience').isVisible(), `${tag}: audience label visible`);
        check(await page.locator('a[href="sample-report"]').count() > 0, `${tag}: links to the sample report`);
        if (view.mobile) {
          const toggle = page.locator('#navToggle');
          await toggle.click();
          check(await toggle.getAttribute('aria-expanded') === 'true' && await page.locator('#navLinks a[href="guides"]').isVisible(), `${tag}: mobile menu opens`);
          await toggle.click();
        }
      }
      if (route === 'sample-report') {
        const text = await page.locator('main').innerText();
        check(/Made-up example/.test(text), `${tag}: labelled as made-up`);
        check(/not a promised saving/.test(text) && /Already included in the £2,776/.test(text), `${tag}: separates cost from saving and avoids double counting`);
      }
      if (route === 'contact') {
        check(await page.locator('form#enquiry[action^="https://formspree.io/f/"]').count() === 1, `${tag}: enquiry form posts to Formspree`);
        check(await page.locator('form#enquiry a[href^="mailto:"]').count() > 0, `${tag}: email fallback beside the form`);
        for (const id of ['name', 'email', 'message']) check(await page.locator(`label[for="${id}"]`).count() === 1, `${tag}: #${id} has a label`);
      }

      const shot = `${out}/${view.label}-${route === 'analyser/' ? 'analyser' : route || 'index'}.png`;
      await page.screenshot({ path: shot });
    }

    // Enquiries record which page on this site the visitor came from.
    {
      const p = await context.newPage();
      await p.goto(base + 'base-load');
      await p.goto(base + 'contact', { referer: base + 'base-load' });
      check(await p.locator('#fromPage').inputValue() === '/base-load', `${view.label} contact: records the page the visitor came from`);
      await p.close();
    }
    // The contact form must only show success when the service accepts the enquiry.
    // Formspree is stubbed here, so no real enquiry is sent.
    for (const [status, body, expectSuccess] of [[200, { ok: true }, true], [422, { errors: [{ message: 'Please enter a valid email.' }] }, false], [0, null, false]]) {
      const p = await context.newPage();
      await p.route('https://formspree.io/**', (r) => (status ? r.fulfill({ status, contentType: 'application/json', body: JSON.stringify(body) }) : r.abort()));
      await p.goto(base + 'contact');
      await p.fill('#name', 'Smoke test'); await p.fill('#email', 'test@example.com'); await p.fill('#message', 'Automated check');
      await p.check('input[name=consent]');
      await p.click('form#enquiry button[type=submit]');
      await p.waitForTimeout(1200);
      const onThanks = p.url().endsWith('thanks.html');
      const errText = onThanks ? '' : await p.locator('.form-error').innerText();
      const label = status ? `HTTP ${status}` : 'network failure';
      if (expectSuccess) check(onThanks, `${view.label} contact: ${label} goes to the thank-you page`);
      else check(!onThanks && errText.length > 0, `${view.label} contact: ${label} shows an error, not success ("${errText}")`);
      await p.close();
    }
    await context.close();
  }
} catch (e) {
  errors.push(`test run failed: ${e.message}`);
} finally {
  await browser?.close();
  server.kill('SIGTERM');
}

console.log(JSON.stringify({ passed: passed.length, failed: errors.length, errors, screenshots: out }, null, 2));
process.exit(errors.length ? 1 : 0);
