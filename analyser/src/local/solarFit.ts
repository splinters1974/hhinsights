/**
 * How much of a solar system's output this site would use itself
 * ("self-consumption"), from its own half-hourly readings.
 *
 * Generation is estimated in the browser, with no network request: a
 * clear-sky sun-position model for central Great Britain (latitude 53°N)
 * gives the shape through each day and the year, and it is scaled so a
 * kWp produces the regional annual output (kWh/kWp) that the UK Solar
 * Calculator uses (SAP 10.3 based), with each quarter's share of the year
 * matched to actual UK solar output. Real days vary with the weather, so
 * treat the result as an estimate.
 *
 * Each half hour, the site uses min(generation, demand); the rest is
 * exported. Self-consumption = used / generated, over the valid readings.
 * This is the same comparison the Solardataprofile sizing service makes
 * against PVGIS hourly data.
 */
import type { Frame } from './frame';

export const SOLAR_CALCULATOR_URL = 'https://uksolarcalculator.co.uk/calculator.html';

/** Annual output per kWp by region, as the UK Solar Calculator's regional fallback. */
export const SOLAR_REGIONS = [
  { key: 'national', label: 'UK average', yield: 905 },
  { key: 'southeast', label: 'South East and East Anglia', yield: 1010 },
  { key: 'southwest', label: 'South West', yield: 1025 },
  { key: 'midlands', label: 'Midlands and Wales', yield: 950 },
  { key: 'north', label: 'North of England', yield: 900 },
  { key: 'scotland', label: 'Scotland', yield: 845 },
] as const;
export type SolarRegion = (typeof SOLAR_REGIONS)[number]['key'];

const LAT = (53 * Math.PI) / 180;
const LON_DEG = -1.5;

/** Last Sunday of a month, as YYYY-MM-DD (UTC arithmetic). */
function lastSunday(year: number, month: number): string {
  const d = new Date(Date.UTC(year, month + 1, 0));
  d.setUTCDate(d.getUTCDate() - d.getUTCDay());
  return d.toISOString().slice(0, 10);
}

/** True if UK clocks are on summer time (BST) for the whole of this date. */
function isBst(date: string): boolean {
  const y = +date.slice(0, 4);
  return date > lastSunday(y, 2) && date < lastSunday(y, 9);
}

function dayOfYear(date: string): number {
  const t = Date.UTC(+date.slice(0, 4), +date.slice(5, 7) - 1, +date.slice(8, 10));
  return Math.floor((t - Date.UTC(+date.slice(0, 4), 0, 1)) / 86_400_000) + 1;
}

/** Relative clear-sky output of a near-flat array, for one half hour (slot 0 = 00:00 to 00:30, clock time). */
function clearSky(doy: number, slot: number, bst: boolean): number {
  const decl = ((23.44 * Math.PI) / 180) * Math.sin((2 * Math.PI * (284 + doy)) / 365);
  const utcHour = slot * 0.5 + 0.25 - (bst ? 1 : 0);
  const hourAngle = ((15 * (utcHour - 12) + LON_DEG) * Math.PI) / 180;
  const sinEl = Math.sin(LAT) * Math.sin(decl) + Math.cos(LAT) * Math.cos(decl) * Math.cos(hourAngle);
  if (sinEl <= 0.01) return 0;
  // Meinel clear-sky attenuation: low sun passes through more atmosphere.
  return sinEl * Math.pow(0.7, Math.pow(1 / sinEl, 0.678));
}

/**
 * Share of a year's UK solar output in each quarter, from actual generation:
 * DESNZ Energy Trends table ET 6.1, average of 2024 and 2025. Clear skies
 * alone put too much in summer and too little in winter; this corrects it.
 */
const QUARTER_SHARE = [0.1275, 0.401, 0.357, 0.114];
const quarterOf = (date: string) => Math.floor((+date.slice(5, 7) - 1) / 3);

/** Per-quarter factors so a reference year's clear-sky output, summed, gives 1 and matches QUARTER_SHARE. */
const QUARTER_SCALE = (() => {
  const q = [0, 0, 0, 0];
  for (let doy = 1; doy <= 365; doy++) {
    const date = new Date(Date.UTC(2025, 0, doy)).toISOString().slice(0, 10);
    for (let s = 0; s < 48; s++) q[quarterOf(date)] += clearSky(doy, s, isBst(date));
  }
  return q.map((v, i) => QUARTER_SHARE[i] / v);
})();

export interface SolarPoint {
  /** System size, kWp. */
  kwp: number;
  /** Estimated generation over the valid readings, kWh. */
  generated: number;
  /** Of which used on site, kWh. */
  used: number;
  /** used / generated. */
  selfConsumption: number;
  /** used / site consumption: the share of the site's electricity solar would supply. */
  coverage: number;
}

export interface SolarFit {
  specificYield: number;
  /** Site consumption over the valid readings, kWh. */
  consumption: number;
  /** Days with at least one valid reading. */
  days: number;
  points: SolarPoint[];
}

/** Sizes as a share of annual use: from a small array to one generating 150% of the site's use. */
const SIZE_RATIOS = [0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1, 1.2, 1.5];

export function solarFit(frame: Frame, specificYield: number): SolarFit | null {
  const perKwp: number[][] = [];
  let consumption = 0, genPerKwp = 0, days = 0;
  frame.dates.forEach((date, i) => {
    const doy = dayOfYear(date), bst = isBst(date), flags = frame.flags?.[i];
    const row: number[] = [];
    let any = false;
    for (let s = 0; s < 48; s++) {
      if (flags && flags[s] !== 0) { row.push(NaN); continue; }
      const g = clearSky(doy, s, bst) * QUARTER_SCALE[quarterOf(date)] * specificYield;
      row.push(g);
      genPerKwp += g;
      consumption += frame.rows[i][s];
      any = true;
    }
    if (any) days++;
    perKwp.push(row);
  });
  if (days < 28 || consumption <= 0 || genPerKwp <= 0) return null;
  // Scale sizes by the period covered, so "100%" means generation equal to the site's use.
  const kwpForAll = consumption / genPerKwp;
  const points = SIZE_RATIOS.map((r) => {
    const kwp = Math.max(1, Math.round(kwpForAll * r * 10) / 10);
    let generated = 0, used = 0;
    perKwp.forEach((row, i) => row.forEach((g, s) => {
      if (Number.isNaN(g)) return;
      const gen = g * kwp;
      generated += gen;
      used += Math.min(gen, frame.rows[i][s]);
    }));
    return { kwp, generated, used, selfConsumption: generated > 0 ? used / generated : 0, coverage: used / consumption };
  });
  return { specificYield, consumption, days, points };
}

/** Share used on site at a given size, interpolated between the computed points. */
export function selfConsumptionAt(fit: SolarFit, kwp: number): number {
  const p = fit.points;
  if (kwp <= p[0].kwp) return p[0].selfConsumption;
  for (let i = 1; i < p.length; i++) {
    if (kwp <= p[i].kwp) {
      const t = (kwp - p[i - 1].kwp) / (p[i].kwp - p[i - 1].kwp);
      return p[i - 1].selfConsumption + t * (p[i].selfConsumption - p[i - 1].selfConsumption);
    }
  }
  return p[p.length - 1].selfConsumption;
}

/**
 * Link that opens the UK Solar Calculator with this site's curve. The data
 * goes after "#", which browsers never send to a server; it holds only the
 * annual use and the share used on site at each size, not the readings.
 * Format: #hhi=1&y=<kWh/kWp>&use=<kWh a year>&sc=<kWp>:<percent>,...
 */
export function solarCalculatorLink(fit: SolarFit): string {
  const annualUse = Math.round((fit.consumption * 365) / fit.days);
  const sc = fit.points.map((p) => `${p.kwp}:${Math.round(p.selfConsumption * 100)}`).join(',');
  return `${SOLAR_CALCULATOR_URL}#hhi=1&y=${fit.specificYield}&use=${annualUse}&sc=${sc}`;
}
