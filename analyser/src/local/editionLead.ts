/**
 * Who is creating a customer edition. Before the file is built, the person
 * gives their name, organisation and email; these (and nothing else: no meter
 * data, no site names, no figures) are emailed to the Half Hourly Insights
 * team through EmailJS, the same service the UK Solar Calculator uses. See the
 * privacy notice ("If you create a customer edition"), which says what is
 * collected, why, and that it is kept for 24 months from last contact.
 */
const EMAILJS_URL = 'https://api.emailjs.com/api/v1.0/email/send';
const SERVICE_ID = 'default_service';
const TEMPLATE_ID = 'template_qvzha1q';
const PUBLIC_KEY = 'W-UuC4rxMLukeKUJJ';
const RECIPIENT = { email: 'martynsheridan@gmail.com', name: 'Martyn' };

export interface EditionLead {
  name: string;
  organisation: string;
  email: string;
  /** Ticked to hear about licences and updates; unticked by default. */
  marketing: boolean;
  /** How many sites the edition holds: a size signal, not the site names. */
  siteCount: number;
}

export const validEmail = (s: string) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(s.trim());

export function leadMessage(l: EditionLead, when = new Date()): string {
  return [
    'CUSTOMER EDITION CREATED ON HALF HOURLY INSIGHTS',
    '',
    `Name: ${l.name.trim()}`,
    `Organisation: ${l.organisation.trim()}`,
    `Email: ${l.email.trim()}`,
    `Sites in the edition: ${l.siteCount}`,
    `Happy to hear about licences and updates: ${l.marketing ? 'yes' : 'no'}`,
    `When: ${when.toLocaleString('en-GB')}`,
    '',
    'Customer editions are the feature consultants use to hand dashboards to clients. Under the terms of use, producing work for clients needs a licence.',
  ].join('\n');
}

/** Send the details. Throws if they could not be sent, so the caller can ask the person to try again. */
export async function sendEditionLead(l: EditionLead): Promise<void> {
  const res = await fetch(EMAILJS_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      service_id: SERVICE_ID,
      template_id: TEMPLATE_ID,
      user_id: PUBLIC_KEY,
      template_params: {
        to_email: RECIPIENT.email,
        to_name: RECIPIENT.name,
        reply_to: l.email.trim(),
        report_date: new Date().toLocaleDateString('en-GB'),
        system_size: 'n/a',
        region: 'n/a',
        message: leadMessage(l),
      },
    }),
  });
  if (!res.ok) throw new Error(`Details not sent (${res.status})`);
}
