/**
 * Solar self-consumption from half-hourly data, and the hand-off link to the
 * UK Solar Calculator.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { parseHHFile } from '../src/local/parser';
import { selfConsumptionAt, solarCalculatorLink, solarFit } from '../src/local/solarFit';

const year = Array.from({ length: 365 }, (_, d) => new Date(Date.UTC(2025, 0, 1 + d)).toISOString().slice(0, 10));
const flat = (kwh: number) => ({ dates: year, rows: year.map(() => new Array(48).fill(kwh)) });

test('1 kWp produces the regional annual output over a full year', () => {
  const f = solarFit(flat(1e6), 905)!;
  const p = f.points[0];
  assert.ok(Math.abs(p.generated / p.kwp - 905) < 1);
});

test('seasonal split follows actual UK output: most in spring and summer, little in winter', () => {
  const share = (months: number[]) => {
    const ds = year.filter((d) => months.includes(+d.slice(5, 7)));
    const f = solarFit({ dates: ds, rows: ds.map(() => new Array(48).fill(1e6)) }, 905)!;
    return f.points[0].generated / f.points[0].kwp / 905;
  };
  assert.ok(Math.abs(share([4, 5, 6]) - 0.401) < 0.002);
  assert.ok(Math.abs(share([10, 11, 12]) - 0.114) < 0.002);
});

test('no generation at night, so a night-only site uses none of it', () => {
  const night = { dates: year, rows: year.map(() => Array.from({ length: 48 }, (_, s) => (s < 8 || s >= 44 ? 5 : 0))) };
  const f = solarFit(night, 905)!;
  assert.ok(f.points.every((p) => p.selfConsumption < 0.01));
});

test('a site with steady demand far above output uses it all; bigger systems export more', () => {
  const f = solarFit(flat(1000), 905)!;
  assert.ok(f.points[0].selfConsumption > 0.999);
  const office = solarFit(parseHHFile(new Uint8Array(fs.readFileSync(new URL('../../site/samples/example-office.csv', import.meta.url))), 'o.csv').frame, 905)!;
  for (let i = 1; i < office.points.length; i++) assert.ok(office.points[i].selfConsumption <= office.points[i - 1].selfConsumption + 1e-9);
  assert.ok(office.points.at(-1)!.selfConsumption < 0.5, 'an office shut at weekends exports a lot from a large array');
});

test('interpolates between sizes and clamps at the ends', () => {
  const f = solarFit(flat(1), 905)!;
  const [a, b] = f.points;
  const mid = selfConsumptionAt(f, (a.kwp + b.kwp) / 2);
  assert.ok(mid <= Math.max(a.selfConsumption, b.selfConsumption) + 1e-9 && mid >= Math.min(a.selfConsumption, b.selfConsumption) - 1e-9);
  assert.equal(selfConsumptionAt(f, 0.1), a.selfConsumption);
  assert.equal(selfConsumptionAt(f, 1e9), f.points.at(-1)!.selfConsumption);
});

test('the hand-off link carries only a summary, after the #', () => {
  const office = solarFit(parseHHFile(new Uint8Array(fs.readFileSync(new URL('../../site/samples/example-office.csv', import.meta.url))), 'o.csv').frame, 905)!;
  const link = solarCalculatorLink(office);
  const [base, frag] = link.split('#');
  assert.equal(base, 'https://uksolarcalculator.co.uk/calculator.html');
  assert.match(frag, /^hhi=1&y=905&use=\d+&sc=(\d+(\.\d)?:\d+,){11}\d+(\.\d)?:\d+$/);
  assert.ok(link.length < 300, 'short summary, not the readings');
});

test('too little data gives no estimate', () => {
  const short = { dates: year.slice(0, 20), rows: year.slice(0, 20).map(() => new Array(48).fill(1)) };
  assert.equal(solarFit(short, 905), null);
});

test('postcodes map to the same sunshine regions as the UK Solar Calculator', async () => {
  const { sapRegionFromPostcode, cleanPostcode } = await import('../src/local/sapRegions');
  assert.equal(sapRegionFromPostcode('EX1 1AA')?.name, 'South West England');
  assert.equal(sapRegionFromPostcode('EX1 1AA')?.yield, 1043);
  assert.equal(sapRegionFromPostcode('AB10 1XG')?.name, 'North East Scotland');
  assert.equal(sapRegionFromPostcode('ZZ99 9ZZ'), null);
  assert.equal(cleanPostcode('ex11aa'), 'EX1 1AA');
  assert.equal(cleanPostcode('not a postcode'), '');
});

test('the hand-off link carries the postcode only when one is entered', () => {
  const office = solarFit(parseHHFile(new Uint8Array(fs.readFileSync(new URL('../../site/samples/example-office.csv', import.meta.url))), 'o.csv').frame, 1043)!;
  assert.ok(!solarCalculatorLink(office).includes('pc='));
  assert.ok(solarCalculatorLink(office, 'ex1 1aa').endsWith('&pc=EX1%201AA'));
  assert.ok(!solarCalculatorLink(office, 'rubbish').includes('pc='));
});
