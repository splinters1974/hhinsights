import { useMemo, useState } from 'react';
import type { SiteSummary } from '../local/localClient';
import { SOLAR_REGIONS, solarCalculatorLink, solarFit, type SolarRegion } from '../local/solarFit';
import { Card, Field } from './ui';
import { btnPrimary, inputCls, kwh, num, pct } from './format';

/**
 * How much of a solar system's output this site would use itself, from its
 * own half-hourly readings, and a hand-off to the UK Solar Calculator.
 */
export default function SolarPanel({ site }: { site: SiteSummary }) {
  const [region, setRegion] = useState<SolarRegion>('national');
  const specificYield = SOLAR_REGIONS.find((r) => r.key === region)!.yield;
  const fit = useMemo(() => solarFit(site.frame, specificYield), [site.frame, specificYield]);
  if (!fit) {
    return (
      <Card title="Solar: how much would you use?">
        <p className="text-sm text-slate-600">This needs at least four weeks of valid readings.</p>
      </Card>
    );
  }
  const scale = 365 / fit.days;
  // Show a few sizes: generation equal to about 20%, 50% and 100% of the site's use.
  const shown = [fit.points[3], fit.points[6], fit.points[9]];
  return (
    <Card title="Solar: how much would you use?"
      subtitle="Estimated from this site's half-hourly readings and a typical UK solar day. Solar output you use yourself saves the full unit rate; the rest is exported for much less.">
      <div className="grid gap-4 md:grid-cols-3 mb-4">
        <Field label="Region" hint="Sets the annual output per kWp, as the UK Solar Calculator does.">
          <select className={inputCls} value={region} onChange={(e) => setRegion(e.target.value as SolarRegion)}>
            {SOLAR_REGIONS.map((r) => <option key={r.key} value={r.key}>{r.label} ({r.yield} kWh/kWp)</option>)}
          </select>
        </Field>
      </div>
      <table className="w-full text-sm">
        <thead><tr className="text-left text-xs text-slate-500">
          <th className="py-1 font-medium">System size</th>
          <th className="text-right font-medium">Output a year</th>
          <th className="text-right font-medium">Used on site</th>
          <th className="text-right font-medium">Share of the site's electricity</th>
        </tr></thead>
        <tbody>
          {shown.map((p) => (
            <tr key={p.kwp} className="border-t border-slate-100">
              <td className="py-1.5">{num(p.kwp, 1)} kWp</td>
              <td className="text-right tabular-nums">{kwh(p.generated * scale)}</td>
              <td className="text-right tabular-nums">{pct(p.selfConsumption)}</td>
              <td className="text-right tabular-nums">{pct(p.coverage)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="text-xs text-slate-500 mt-2">
        Larger systems export more of their output, especially at weekends and on long summer evenings. A typical solar day is
        used, scaled to the region's annual output and to the UK's actual seasonal pattern, so real days will vary with the weather.
      </p>
      <div className="mt-4 flex flex-wrap items-center gap-3">
        <a className={btnPrimary} href={solarCalculatorLink(fit)} target="_blank" rel="noopener">
          Size solar for this site in the UK Solar Calculator
        </a>
        <span className="text-xs text-slate-500 max-w-xl">
          Opens our sister site in a new tab with the figures above already filled in. Only this site's annual use and the share used
          on site at each size are passed, after the # in the web address, which browsers don't send to any server. The readings stay here.
        </span>
      </div>
    </Card>
  );
}
