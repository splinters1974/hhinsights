/**
 * Brand: Half Hourly Insights, the public build of the analyser for the
 * website. The logo is embedded as data so the page needs nothing beside it
 * and the PDFs carry it too.
 */
import { HHI_LOGO, HHI_LOGO_ASPECT } from './hhiLogo';

/** The public build: anyone can use it, so no company "prepares" anything. */
export const IS_HHI = true;

/** The name in running text. */
export const COMPANY = 'Half Hourly Insights';
/** The name as it signs off ("By …"). */
export const COMPANY_FULL = 'Half Hourly Insights';
/** How a customer edition credits its maker ("Energy dashboard …"). */
export const PREPARED = 'made with Half Hourly Insights';
/** Who set the locked parts of a customer edition. */
export const SET_BY = 'whoever made this dashboard';

/** Action blue and money green, as on the website. */
export const BRAND_ACCENT = '#0065a5';
export const BRAND_GREEN = '#008540';

/** The logo, and its width / height for placing it without distortion. */
export const LOGO = HHI_LOGO;
export const LOGO_ASPECT = HHI_LOGO_ASPECT;

/**
 * Attribution carried by every download in the public build: PDFs (every
 * page), Excel (top of every sheet and the file properties), chart images
 * and customer dashboards. Free use is for the user's own organisation;
 * producing work for clients needs a licence (see /terms on the website).
 */
export const SITE_URL_SHORT = 'hhinsights.co.uk';
export const ATTRIBUTION = 'Made with Half Hourly Insights · hhinsights.co.uk';
export const LICENCE_NOTE = 'Free to use for your own organisation. Producing work for clients needs a licence: hhinsights.co.uk/terms';
