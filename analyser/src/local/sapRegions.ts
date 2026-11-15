/**
 * Postcode to solar yield, as the UK Solar Calculator does it, so both sites
 * give the same figure for the same postcode. Copied from the calculator
 * (calculator.html, SAP_REGIONS and SAP_POSTCODES): SAP 10.3 Appendix U,
 * Table U6 maps postcode districts to 21 sunshine regions; each yield is net
 * kWh per kWp a year for an east-west array at 10 degrees. If the calculator's
 * table changes, copy it again.
 */
export interface SapRegion { name: string; yield: number; broad: string }

export const SAP_REGIONS: SapRegion[] = [
  { name: "UK average", yield: 905, broad: 'national' },
  { name: "Thames", yield: 969, broad: 'southeast' },
  { name: "South East England", yield: 1029, broad: 'southeast' },
  { name: "Southern England", yield: 1053, broad: 'southeast' },
  { name: "South West England", yield: 1043, broad: 'southwest' },
  { name: "Severn", yield: 1003, broad: 'southwest' },
  { name: "Midlands", yield: 931, broad: 'midlands' },
  { name: "West Pennines", yield: 895, broad: 'north' },
  { name: "NW England & SW Scotland", yield: 908, broad: 'north' },
  { name: "Borders", yield: 887, broad: 'north' },
  { name: "North East England", yield: 902, broad: 'north' },
  { name: "East Pennines", yield: 905, broad: 'north' },
  { name: "East Anglia", yield: 990, broad: 'southeast' },
  { name: "Wales", yield: 968, broad: 'midlands' },
  { name: "West Scotland", yield: 851, broad: 'scotland' },
  { name: "East Scotland", yield: 857, broad: 'scotland' },
  { name: "North East Scotland", yield: 832, broad: 'scotland' },
  { name: "Highland", yield: 806, broad: 'scotland' },
  { name: "Western Isles", yield: 856, broad: 'scotland' },
  { name: "Orkney", yield: 828, broad: 'scotland' },
  { name: "Shetland", yield: 780, broad: 'scotland' },
  { name: "Northern Ireland", yield: 888, broad: 'north' },
];

const SAP_POSTCODES: Record<string, number> = {"AB": 16, "G": 14, "N": 1, "SL": 1, "AL": 1, "GL": 5, "NE": 9, "SM": 1, "B": 6, "GU": 1, "NG": 11, "SN": 5, "BA": 5, "GU11-12": 3, "NN": 6, "SN7": 1, "BB": 7, "GU14": 3, "NP": 5, "SO": 3, "BD": 11, "GU28-29": 2, "NP8": 13, "SP": 5, "BD23-24": 10, "GU30-35": 3, "NR": 12, "SP6-11": 3, "BH": 3, "GU46": 3, "NW": 1, "SR": 9, "BL": 7, "GU51-52": 3, "OL": 7, "SR7-8": 10, "BN": 2, "HA": 1, "OX": 1, "SS": 12, "BR": 2, "HD": 11, "PA": 14, "ST": 6, "BS": 5, "HG": 10, "PE": 12, "SW": 1, "BT": 21, "HP": 1, "PE9-12": 11, "SY": 6, "CA": 8, "HR": 6, "PE20-25": 11, "SY14": 7, "CB": 12, "HS": 18, "PH": 15, "SY15-25": 13, "CF": 5, "HU": 11, "PH19-25": 17, "TA": 5, "CH": 7, "HX": 11, "PH26": 16, "TD": 9, "CH5-8": 7, "IG": 12, "PH30-44": 17, "TD12": 9, "CM": 12, "IP": 12, "PH49": 14, "TD15": 9, "CM21-23": 1, "IV": 17, "PH50": 14, "TF": 6, "CO": 12, "IV30-32": 16, "PL": 4, "TN": 2, "CR": 1, "IV36": 16, "PO": 3, "TQ": 4, "CT": 2, "KA": 14, "PO18-22": 2, "TR": 4, "CV": 6, "KT": 1, "PR": 7, "TS": 10, "CW": 7, "KW": 17, "RG": 1, "TW": 1, "DA": 2, "KW15-17": 19, "RG21-29": 3, "UB": 1, "DD": 15, "KY": 15, "RH": 1, "W": 1, "DE": 6, "L": 7, "RH10-20": 2, "WA": 7, "DG": 8, "LA": 7, "RM": 12, "WC": 1, "DH": 10, "LA7-23": 8, "S": 11, "WD": 1, "DH4-5": 9, "LD": 13, "S18": 6, "WF": 11, "DL": 10, "LE": 6, "S32-33": 6, "WN": 7, "DN": 11, "LL": 7, "S40-45": 6, "WR": 6, "DT": 3, "LL23-27": 13, "SA": 5, "WS": 6, "DY": 6, "LL30-78": 13, "SA14-20": 13, "WV": 6, "E": 1, "LN": 11, "SA31-48": 13, "YO": 10, "EC": 1, "LS": 11, "SA61-73": 13, "YO15-16": 11, "EH": 15, "LS24": 10, "SE": 1, "YO25": 11, "EH43-46": 9, "LU": 1, "SG": 1, "ZE": 20, "EN": 1, "M": 7, "SK": 7, "EN9": 12, "ME": 2, "SK13": 6, "EX": 4, "MK": 1, "SK17": 6, "FK": 14, "ML": 14, "SK22-23": 6, "FY": 7};

/** Normalised postcode (upper case, single space), or '' if it doesn't look like one. */
export function cleanPostcode(raw: string): string {
  const pc = String(raw || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
  const m = pc.match(/^([A-Z]{1,2}\d[A-Z\d]?)(\d[A-Z]{2})$/);
  if (m) return `${m[1]} ${m[2]}`;
  return /^[A-Z]{1,2}\d[A-Z\d]?$/.test(pc) ? pc : '';
}

/** The SAP sunshine region for a full or outward postcode, or null if not recognised. */
export function sapRegionFromPostcode(raw: string): SapRegion | null {
  const parts = String(raw || '').trim().toUpperCase().split(/\s+/);
  const pc = parts.join('').replace(/[^A-Z0-9]/g, '');
  if (pc.length < 2) return null;
  const outward = parts.length > 1 ? parts[0].replace(/[^A-Z0-9]/g, '')
    : (/\d[A-Z]{2}$/.test(pc) && pc.length >= 5 ? pc.slice(0, -3) : pc);
  const m = outward.match(/^([A-Z]{1,2})(\d{1,2})[A-Z]?$/);
  if (!m) return null;
  const area = m[1], dist = parseInt(m[2], 10);
  let hit: number | null = null;
  for (const key of Object.keys(SAP_POSTCODES)) {
    const km = key.match(/^([A-Z]+)(\d+)(?:-(\d+))?$/);
    if (km && km[1] === area) {
      const lo = parseInt(km[2], 10), hi = km[3] ? parseInt(km[3], 10) : lo;
      if (dist >= lo && dist <= hi) hit = SAP_POSTCODES[key];
    }
  }
  if (hit === null && SAP_POSTCODES[area] !== undefined) hit = SAP_POSTCODES[area];
  return hit === null ? null : SAP_REGIONS[hit];
}
