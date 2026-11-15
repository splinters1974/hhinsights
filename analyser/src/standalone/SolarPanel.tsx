import { useMemo, useState } from 'react';
import type { SiteSummary } from '../local/localClient';
import type { SiteSettings } from '../local/site';
import { SOLAR_REGIONS, solarCalculatorLink, solarFit, type SolarRegion } from '../local/solarFit';
import { cleanPostcode, sapRegionFromPostcode } from '../local/sapRegions';
import { Card, Field } from './ui';
import { btnPrimary, inputCls, kwh, num, pct } from './format';

/**
 * How much of a solar system's output this site would use itself, from its
 * own half-hourly readings, and a hand-off to the UK Solar Calculator.
 */
export default function SolarPanel({ site, onChange }: { site: SiteSummary; onChange?: (s: SiteSettings) => void }) {
  const [region, setRegion] = useState<SolarRegion>('national');
  // The postcode is typed here and saved with the site when the box loses focus.
  const [postcode, setPostcode] = useState(site.settings.postcode ?? '');
  const sap = sapRegionFromPostcode(postcode);
  const specificYield = sap ? sap.yield : SOLAR_REGIONS.find((r) => r.key === region)!.yield;
  const savePostcode = () => {
    const clean = cleanPostcode(postcode) || postcode.trim().toUpperCase();
    if (clean !== postcode) setPostcode(clean);
    if (onChange && clean !== (site.settings.postcode ?? '')) onChange({ ...site.settings, postcode: clean });
  };
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
      <div className="flex flex-wrap items-end gap-4 mb-4">
        <div className="w-full sm:w-48">
          <Field label="Site postcode (optional)"
            hint={sap ? 'Recognised.' : postcode.trim() && /\d/.test(postcode) ? 'Not recognised, so the region is used' : 'Sets the sunshine and finds the site on the calculator\'s map.'}>
            <input className={inputCls} value={postcode} maxLength={8} autoComplete="postal-code" placeholder="e.g. EX1 1AA"
              aria-label="Site postcode"
              onChange={(e) => setPostcode(e.target.value.toUpperCase())} onBlur={savePostcode}
              onKeyDown={(e) => { if (e.key === 'Enter') (e.target as HTMLInputElement).blur(); }} />
          </Field>
        </div>
        <div className="w-full sm:w-80">
          <Field label="Region" hint={sap ? 'Set from the postcode.' : 'Sets the annual output per kWp, as the UK Solar Calculator does.'}>
            {sap ? (
              <select className={inputCls} disabled value="postcode" aria-label="Region, set from the postcode">
                <option value="postcode">{sap.name} ({sap.yield} kWh/kWp)</option>
              </select>
            ) : (
              <select className={inputCls} value={region} onChange={(e) => setRegion(e.target.value as SolarRegion)}>
                {SOLAR_REGIONS.map((r) => <option key={r.key} value={r.key}>{r.label} ({r.yield} kWh/kWp)</option>)}
              </select>
            )}
          </Field>
        </div>
        <div className="pb-5 w-full sm:w-auto">
          <a className={`${btnPrimary} flex w-full sm:inline-flex sm:w-auto justify-center text-center`} href={solarCalculatorLink(fit, postcode)} target="_blank" rel="noopener">
            Size solar for this site in the UK Solar Calculator
          </a>
        </div>
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
      <p className="text-xs text-slate-500 mt-3 max-w-3xl">
        The button opens our sister site, the UK Solar Calculator, in a new tab with these figures filled in, so it can work out what fits
        on your roof, the cost and the payback. Only this site's annual use, the share used on site at each size and the postcode, if you
        entered one, are passed, after the # in the web address, which browsers don't send to any server. The readings stay here.{' '}
        <a className="underline" href="../solar" target="_blank" rel="noopener">How to use these figures</a>.
      </p>
    </Card>
  );
}
