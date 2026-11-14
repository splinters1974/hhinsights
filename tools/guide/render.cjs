// Renders guide-built.html to a PDF. node render.mjs <built html> <output pdf> <footer text>
// Each h2 and what follows it, up to the next heading, is kept on one page.
const { chromium } = require('playwright');
const [input, output, footer] = process.argv.slice(2);
(async () => {
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(`file://${input}`, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.evaluate(() => {
  const style = document.createElement('style');
  style.textContent = '.keep { break-inside: avoid; }';
  document.head.appendChild(style);
  for (const h of [...document.querySelectorAll('h2')]) {
    const wrap = document.createElement('div');
    wrap.className = 'keep';
    h.before(wrap);
    let n = h;
    while (n && !(n !== h && /^H[12]$/.test(n.tagName ?? '')) && !n.matches?.('section')) {
      const next = n.nextSibling;
      wrap.appendChild(n);
      n = next;
    }
  }
});
await page.pdf({
  path: output, format: 'A4', printBackground: true, preferCSSPageSize: true,
  displayHeaderFooter: true, headerTemplate: '<span></span>',
  footerTemplate: `<div style="width:100%;font-family:'Schibsted Grotesk','Liberation Sans',sans-serif;font-size:7.5pt;color:#58595B;padding:0 17mm;display:flex;justify-content:space-between">
    <span>${footer}</span><span><span class="pageNumber"></span></span></div>`,
});
await browser.close();
})();
