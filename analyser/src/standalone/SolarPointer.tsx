import { useState } from 'react';
import type { SiteTab } from '../local/findings';
import { inputCls } from './format';

/** Up to this many sites get a button each; more get a drop-down list. */
const MAX_BUTTONS = 6;

/**
 * The "Thinking about solar?" line on the All sites page. Every site has a
 * Solar tab, so this offers each of them: one button per site for a small
 * estate, a list to choose from for a large one.
 */
export default function SolarPointer({ sites, openSite }: {
  sites: { id: string; settings: { name: string } }[];
  openSite: (id: string, tab?: SiteTab) => void;
}) {
  const [chosen, setChosen] = useState(sites[0]?.id ?? '');
  if (!sites.length) return null;
  const link = 'text-sm font-semibold text-[var(--brand)] hover:underline whitespace-nowrap';
  return (
    <div className="rounded-xl border border-slate-300 border-l-4 border-l-amber-400 bg-white px-5 py-3 space-y-2">
      <p className="text-sm text-slate-700">
        <strong className="text-slate-900">Thinking about solar?</strong> Each site has a Solar tab showing how much of a system's
        output it would use, with a button to size it in the UK Solar Calculator.
      </p>
      {sites.length === 1 && (
        <button onClick={() => openSite(sites[0].id, 'solar')} className={link}>Open the Solar tab →</button>
      )}
      {sites.length > 1 && sites.length <= MAX_BUTTONS && (
        <div className="flex flex-wrap gap-x-5 gap-y-1" role="group" aria-label="Open a site's Solar tab">
          {sites.map((s) => (
            <button key={s.id} onClick={() => openSite(s.id, 'solar')} className={link}>Solar for {s.settings.name} →</button>
          ))}
        </div>
      )}
      {sites.length > MAX_BUTTONS && (
        <div className="flex flex-wrap items-center gap-3">
          <label className="text-sm text-slate-700" htmlFor="solar-site">Site</label>
          <select id="solar-site" className={`${inputCls} w-auto max-w-xs`} value={chosen} onChange={(e) => setChosen(e.target.value)}>
            {sites.map((s) => <option key={s.id} value={s.id}>{s.settings.name}</option>)}
          </select>
          <button onClick={() => openSite(chosen, 'solar')} className={link}>Open its Solar tab →</button>
        </div>
      )}
    </div>
  );
}
