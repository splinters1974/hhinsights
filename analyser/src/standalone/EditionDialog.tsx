import { useState } from 'react';
import { defaultPassword } from '../local/customerEdition';
import { downloadCustomerEdition, friendlyError } from '../local/localClient';
import { IS_HHI } from '../local/brand';
import { sendEditionLead, validEmail } from '../local/editionLead';

const input = 'w-full border border-slate-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-[var(--brand)]';

/**
 * Make a locked, password-protected copy of this app holding the sites
 * loaded now, for one customer to explore and download their own reports.
 */
export default function EditionDialog({ initialCustomer, siteCount, onClose }: {
  initialCustomer: string;
  siteCount: number;
  onClose: () => void;
}) {
  const [customer, setCustomer] = useState(initialCustomer);
  const [year, setYear] = useState(new Date().getFullYear());
  const [custom, setCustom] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [done, setDone] = useState(false);
  const [includeNotes, setIncludeNotes] = useState(false);
  // Who is making it (public build only): name, organisation, email, optional marketing consent.
  const [me, setMe] = useState({ name: '', organisation: '', email: '', marketing: false });
  const detailsOk = !IS_HHI || (me.name.trim() && me.organisation.trim() && validEmail(me.email));
  const password = custom ?? defaultPassword(customer, year);

  async function create() {
    setBusy(true);
    setError(null);
    try {
      if (IS_HHI) {
        try {
          await sendEditionLead({ ...me, siteCount });
        } catch {
          throw new Error('Your details could not be sent, so the file was not created. Check your internet connection and try again.');
        }
      }
      await downloadCustomerEdition(customer, password, { includeNotes });
      setDone(true);
    } catch (e) {
      setError(friendlyError(e, 'Could not create the file.'));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/40 flex items-center justify-center px-4" role="dialog" aria-modal="true">
      <div className="w-full max-w-lg max-h-[90vh] overflow-y-auto bg-white rounded-xl shadow-md border border-slate-300 p-6 space-y-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-800">Create customer edition</h2>
          <p className="text-sm text-slate-500 mt-0.5">
            A locked copy of this dashboard holding the {siteCount} site{siteCount === 1 ? '' : 's'} loaded now,
            with their current settings, logo, findings, action statuses and savings scenarios. The customer can explore every chart,
            change opening hours and closures, rates, carbon factor, supply capacity, excluded readings and savings scenarios, save
            their changes as a new copy with the same password, and download PDFs and a summary spreadsheet. They cannot add or
            remove sites, change action tracking or the analysis method, or get the half-hourly data out as a spreadsheet.
          </p>
        </div>

        <div className="grid grid-cols-3 gap-3">
          <div className="col-span-2">
            <label className="block text-xs font-medium text-slate-600 mb-1">Customer name</label>
            <input className={input} value={customer} onChange={(e) => setCustomer(e.target.value)} placeholder="e.g. Compleat Foods" />
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-600 mb-1">Year</label>
            <input className={input} type="number" value={year} onChange={(e) => setYear(Number(e.target.value) || year)} />
          </div>
        </div>

        <div>
          <label className="block text-xs font-medium text-slate-600 mb-1">Password</label>
          <div className="flex gap-2">
            <input className={`${input} font-mono`} value={password} onChange={(e) => setCustom(e.target.value)} />
            {custom !== null && (
              <button onClick={() => setCustom(null)} className="text-xs text-slate-500 hover:text-slate-800 whitespace-nowrap">
                Use standard
              </button>
            )}
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Standard is the customer name in lower case plus the year. Send the password separately from the
            file (by phone or a separate message), never in the same email.
          </p>
        </div>

        <label className="flex items-start gap-2 text-sm text-slate-700">
          <input type="checkbox" className="mt-0.5" checked={includeNotes} onChange={(e) => setIncludeNotes(e.target.checked)} />
          <span>Include action owners, target dates and internal notes<br />
            <span className="text-xs text-slate-500">Off by default: the customer sees each finding's status only.</span></span>
        </label>

        {IS_HHI && (
          <fieldset className="border-t border-slate-200 pt-3 space-y-2">
            <legend className="text-sm font-semibold text-slate-800 pr-2">About you</legend>
            <p className="text-xs text-slate-500">
              Customer editions are for handing dashboards to others. Using them to produce work for clients needs a licence
              (see the <a className="underline" href="../terms" target="_blank" rel="noopener">terms of use</a>). We ask who you are before the
              file is made. Only these details are sent to us, never the meter data or anything in the file.{' '}
              <a className="underline" href="../privacy" target="_blank" rel="noopener">Privacy notice</a>.
            </p>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1" htmlFor="ed-name">Your name</label>
                <input id="ed-name" className={input} autoComplete="name" value={me.name} onChange={(e) => setMe({ ...me, name: e.target.value })} />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1" htmlFor="ed-org">Your organisation</label>
                <input id="ed-org" className={input} autoComplete="organization" value={me.organisation} onChange={(e) => setMe({ ...me, organisation: e.target.value })} />
              </div>
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1" htmlFor="ed-email">Work email</label>
              <input id="ed-email" type="email" className={input} autoComplete="email" value={me.email} onChange={(e) => setMe({ ...me, email: e.target.value })} />
            </div>
            <label className="flex items-start gap-2 text-sm text-slate-700">
              <input type="checkbox" className="mt-0.5" checked={me.marketing} onChange={(e) => setMe({ ...me, marketing: e.target.checked })} />
              <span>Tell me about licences and updates to Half Hourly Insights (optional)</span>
            </label>
          </fieldset>
        )}

        {error && <p className="text-sm text-[#b42c2c]">{error}</p>}
        {done && (
          <p className="text-sm text-[#08780a] bg-green-50 border border-green-200 rounded-lg px-3 py-2">
            Created. Check your downloads for the file, then open it yourself with the password before sending it.
          </p>
        )}

        <div className="flex justify-end gap-2 pt-1">
          <button onClick={onClose} className="text-sm font-medium text-slate-600 px-4 py-2 rounded-lg hover:bg-slate-100">
            {done ? 'Close' : 'Cancel'}
          </button>
          <button
            onClick={create}
            disabled={busy || !customer.trim() || !detailsOk}
            className="text-sm font-semibold bg-[var(--brand)] hover:bg-[var(--brand-dark)] disabled:opacity-50 text-white px-4 py-2 rounded-lg"
          >
            {busy ? 'Encrypting…' : 'Create file'}
          </button>
        </div>
      </div>
    </div>
  );
}
