/**
 * The website quotes figures for the example office file (site/samples/example-office.csv)
 * on the sample report and worked example pages. These tests run the same file through
 * the analyser so a change to either the file or the engine shows up as a failure,
 * instead of the pages silently going out of date.
 *
 * They also load the same readings in other layouts (long CSV, Excel, gaps, duplicates,
 * part year) and check the totals behave.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import * as XLSX from 'xlsx';
import { parseHHFile } from '../src/local/parser';
import { defaultSettings } from '../src/local/site';
import { analyse } from './helpers';

const csvText = fs.readFileSync(new URL('../../site/samples/example-office.csv', import.meta.url), 'utf8');
const enc = (s: string) => new TextEncoder().encode(s);
const wide = parseHHFile(enc(csvText), 'example-office.csv').frame;
const office = (f = wide) => analyse(f, defaultSettings('Office'), 25);
const sum = (rows: number[][]) => rows.flat().filter(Number.isFinite).reduce((a, b) => a + b, 0);
const r = Math.round;

test('sample report: headline figures match the analyser', () => {
  const m = office();
  assert.equal(r(m.annual!.kwh), 79191);
  assert.equal(r(m.annual!.cost), 19798);
  assert.equal(r(m.closed.share * 100), 33);
  assert.equal(m.baseAll.kw, 2.6);
  assert.equal(r(m.base.annual!.cost / 100) * 100, 5700);
});

test('sample report: closed-hours finding, its parts and its level', () => {
  const m = office();
  const by = Object.fromEntries(m.byClass.map((c) => [c.cls, r(c.excessAll)]));
  assert.deepEqual(by, { weekday: 3750, saturday: 5155, sunday: 722, holiday: 1408 });
  const ooh = m.findings.find((f) => f.key === 'ooh')!;
  assert.equal(ooh.level, 'high');
  assert.equal(r(ooh.cost!.annual!), 2776);
  assert.equal(r(ooh.kwh!.observed), 11035);
  // The parts add up to the whole: nothing counted twice or left out.
  assert.equal(by.weekday + by.saturday + by.sunday + by.holiday, 11035);
});

test('sample report: smaller findings sit inside the closed-hours figure, base load is separate', () => {
  const m = office();
  const f = Object.fromEntries(m.findings.map((x) => [x.key, x]));
  assert.equal(f.holidays.level, 'medium');
  assert.match(f.holidays.title, /^7 bank holidays/);
  assert.equal(f.shoulders.level, 'low');
  assert.equal(r(f.shoulders.cost!.annual!), 629);
  assert.ok(f.ooh.related.includes('holidays') && f.ooh.related.includes('shoulders'));
  assert.ok(f.shoulders.kwh!.observed < f.ooh.kwh!.observed);
  assert.equal(f.base.calendarDependent, false);
  assert.equal(f.base.level, 'info');
});

test('the analysed total is the file total less the two clock-change days held back', () => {
  const { frame, warnings } = parseHHFile(enc(csvText), 'example-office.csv');
  assert.equal(frame.dates.length, 365);
  assert.equal(warnings.filter((w) => /clock-change day/.test(w)).length, 2);
  const m = office(frame);
  assert.ok(m.observed.kwh < sum(frame.rows) && sum(frame.rows) - m.observed.kwh < 400);
});

// --- Same readings, other layouts ---------------------------------------------------

const header = csvText.split(/\r?\n/)[0].split(',');
const dataLines = csvText.trim().split(/\r?\n/).slice(1).map((l) => l.split(','));

function longCsv(lines = dataLines): string {
  const out = ['Timestamp,kWh'];
  for (const [d, ...vals] of lines) {
    vals.forEach((v, i) => {
      const start = new Date(Date.parse(`${d}T00:00:00Z`) + i * 1800_000).toISOString().slice(0, 16).replace('T', ' ');
      out.push(`${start},${v}`);
    });
  }
  return out.join('\n');
}

test('Excel copy of the file gives the same days and total', () => {
  const ws = XLSX.utils.aoa_to_sheet([header, ...dataLines.map(([d, ...v]) => [d, ...v.map(Number)])]);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'Data');
  const bytes = XLSX.write(wb, { type: 'array', bookType: 'xlsx' }) as ArrayBuffer;
  const x = parseHHFile(new Uint8Array(bytes), 'example-office.xlsx').frame;
  assert.deepEqual(x.dates, wide.dates);
  assert.equal(sum(x.rows).toFixed(2), sum(wide.rows).toFixed(2));
  assert.equal(r(office(x).annual!.kwh), 79191);
});

test('one-reading-per-row CSV gives the same days and total as the grid (winter, no clock change)', () => {
  const winter = dataLines.filter(([d]) => d >= '2024-11-01' && d <= '2025-02-28');
  const p = parseHHFile(enc(longCsv(winter)), 'long.csv');
  const grid = wide.dates.map((d, i) => [d, wide.rows[i]] as const).filter(([d]) => d >= '2024-11-01' && d <= '2025-02-28');
  assert.equal(p.info.convention, 'start');
  assert.deepEqual(p.frame.dates, grid.map(([d]) => d));
  assert.equal(sum(p.frame.rows).toFixed(2), sum(grid.map(([, row]) => row)).toFixed(2));
});

test('a timestamped file in GMT all year is spotted and moved to UK clock time', () => {
  const p = parseHHFile(enc(longCsv()), 'long-gmt.csv');
  assert.ok(p.warnings.some((w) => /GMT all year/.test(w)));
  // The one ambiguous day is held back for review rather than guessed.
  assert.ok(p.warnings.some((w) => /two different readings for the same time/.test(w)));
});

test('blank readings are gaps, not zeros, and are reported', () => {
  const holed = dataLines.map((l, i) => (i % 30 === 5 ? [l[0], ...l.slice(1).map((v, j) => (j < 12 ? '' : v))] : l));
  const p = parseHHFile(enc([header.join(','), ...holed.map((l) => l.join(','))].join('\n')), 'gaps.csv');
  const flagged = (p.frame.flags ?? []).reduce((n, f) => n + (f ? f.filter((x) => x !== 0).length : 0), 0);
  assert.ok(flagged >= 12 * 12, `blank slots flagged as invalid (${flagged})`);
  assert.ok(sum(p.frame.rows) < sum(wide.rows), 'blanks add nothing to the total');
  assert.equal(office(p.frame).baseAll.kw, 2.6, 'gaps do not drag base load to zero');
  assert.ok(p.warnings.some((w) => /blank half-hour/.test(w)));
});

test('a day repeated in the file is not counted twice', () => {
  const dup = [...dataLines.slice(0, 100), dataLines[50], ...dataLines.slice(100)];
  let total: number | null = null;
  try {
    const p = parseHHFile(enc([header.join(','), ...dup.map((l) => l.join(','))].join('\n')), 'dup.csv');
    total = sum(p.frame.rows);
    assert.equal(p.frame.dates.length, 365, 'one row per date');
  } catch (e) {
    // Refusing the file outright is also safe.
    assert.match(String(e), /duplicate|twice|repeated|conflict/i);
  }
  if (total !== null) assert.ok(Math.abs(total - sum(wide.rows)) < 1e-6, `total ${total} vs ${sum(wide.rows)}`);
});

test('a part year is analysed as it is, not scaled up to a year by default', () => {
  const part = dataLines.slice(0, 120);
  const p = parseHHFile(enc([header.join(','), ...part.map((l) => l.join(','))].join('\n')), 'part.csv');
  const m = office(p.frame);
  assert.equal(p.frame.dates.length, 120);
  assert.equal(m.annual, null);
  assert.ok(m.findings.every((f) => !f.cost || f.cost.annual == null), 'no annual £ on a 4-month file');
});
