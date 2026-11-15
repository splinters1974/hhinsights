"""
Energy price section: what's in a business electricity price, the non-energy
charges one by one, ten years of prices, and where non-energy costs are heading.

Every figure comes from a published source, cited on the page, with its date.
Rates change every April (levies, network charges, CCL), every six months
(BSUoS) and every quarter (CfD and nuclear RAB levies).

REVIEW EACH APRIL, and when NESO publishes final BSUoS tariffs each December:
  RATES below (RO level and buy-out price, CfD and RAB interim levy rates,
  Capacity Market total and peak demand, BSUoS, TNUoS band charges, CCL),
  PRICES (DESNZ Quarterly Energy Prices table 3.4.2, updated quarterly),
  the OUTLOOK table, and the CHECKED date.
"""
from kit import sources
from pages_guides import GUIDES, HOME, guide_page

CHECKED = '14 November 2026'


def ref(*n):
    return f'<sup><a href="#sources">{",".join(str(x) for x in n)}</a></sup>'


# ── Sources ──────────────────────────────────────────────────────────────
S = {
    'qep': ('Department for Energy Security and Net Zero: Gas and electricity prices in the non-domestic sector, QEP tables 3.4.1 and 3.4.2 (29 September 2026)',
            'https://www.gov.uk/government/statistical-data-sets/gas-and-electricity-prices-in-the-non-domestic-sector'),
    'wmi': ('Ofgem: Wholesale market indicators, day-ahead baseload contracts', 'https://www.ofgem.gov.uk/news-and-insight/data/data-portal/wholesale-market-indicators'),
    'ro': ('Department for Energy Security and Net Zero: Calculating the level of the Renewables Obligation for 2026 to 2027 (29 September 2025)',
           'https://www.gov.uk/government/publications/renewables-obligation-level-calculations-2026-to-2027/calculating-the-level-of-the-renewables-obligation-for-2026-to-2027'),
    'ro_buyout': ('Ofgem: Renewables Obligation buy-out price and mutualisation threshold and ceilings 2026 to 2027 (31 March 2026)',
                  'https://www.ofgem.gov.uk/data/renewables-obligation-buy-out-price-and-mutualisation-threshold-and-ceilings-2026-2027'),
    'ro2728': ('Department for Energy Security and Net Zero: Calculating the level of the Renewables Obligation for 2027 to 2028 (25 September 2026)',
               'https://www.gov.uk/government/publications/renewables-obligation-level-calculations-2027-to-2028/calculating-the-level-of-the-renewables-obligation-for-2027-to-2028'),
    'emrs': ('EMR Settlement: Key figures for payments 2026/27 (CfD and nuclear RAB levy rates, Capacity Market payments)',
             'https://www.emrsettlement.co.uk/document/settlement-data/key-figures-for-payment-2026-27-excel/'),
    'cm': ('EMR Settlement: G15 Capacity Market supplier payments guidance', 'https://www.emrsettlement.co.uk/document/guidance/g15-cm-supplier-payments/'),
    'cfd': ('EMR Settlement: Contracts for Difference explained', 'https://www.emrsettlement.co.uk/about-emr/contracts-for-difference/'),
    'rab': ('EMR Settlement: Nuclear RAB', 'https://www.emrsettlement.co.uk/schemes/nuclearrab/'),
    'bsuos': ('NESO: BSUoS final tariffs for 2026/27 (December 2025)', 'https://www.neso.energy/document/375861/download'),
    'bsuos28': ('NESO: BSUoS draft tariffs for 2027/28 (October 2026)', 'https://www.neso.energy/document/388126/download'),
    'bsuos_nov': ('NESO: BSUoS forecast for November 2026', 'https://www.neso.energy/document/388856/download'),
    'tnuos': ('NESO: Final TNUoS tariffs for 2026/27 (January 2026) and tables', 'https://www.neso.energy/document/376336/download'),
    'cmp440': ('NESO: CMP440 workgroup report, re-introduction of demand TNUoS (April 2026)', 'https://www.neso.energy/document/377086/download'),
    'tcr': ('Ofgem: Targeted Charging Review decision (December 2019)', 'https://www.ofgem.gov.uk/sites/default/files/docs/2019/12/full_decision_doc_updated.pdf'),
    'duos': ('Ofgem: Distribution use of system charging, managing the effects of surplus residual charges, call for input (July 2024)',
             'https://www.ofgem.gov.uk/sites/default/files/2024-07/Call_for_input_Distribution_Use_of_System_Charging_Managing_the_effects_of_surplus_residual_charges1721755290818.pdf'),
    'ed3': ('Ofgem: Ofgem sets rules for 2028 to 2033 grid investment to meet growing electricity demand (21 May 2026)',
            'https://www.ofgem.gov.uk/press-release/ofgem-sets-rules-2028-2033-grid-investment-meet-growing-electricity-demand'),
    'ccl': ('HM Revenue and Customs: Climate Change Levy rates (updated 27 November 2025)', 'https://www.gov.uk/guidance/climate-change-levy-rates'),
    'ccl28': ('HM Revenue and Customs: Climate Change Levy rates from 1 April 2028 (28 October 2026)',
              'https://www.gov.uk/government/publications/climate-change-levy-rates-from-1-april-2028'),
    'vat': ('HM Revenue and Customs: VAT on fuel and power (VAT Notice 701/19, updated 28 October 2026)', 'https://www.gov.uk/guidance/vat-on-fuel-and-power-notice-70119'),
    'fit': ('Ofgem: Feed-in Tariffs (FIT)', 'https://www.ofgem.gov.uk/environmental-and-social-schemes/feed-tariffs-fit'),
    'bics': ('Department for Business and Trade: British Industrial Competitiveness Scheme (updated 1 October 2026)',
             'https://www.gov.uk/government/collections/british-industrial-competitiveness-scheme'),
}


def src(*keys):
    """Numbered sources for a page, in order, plus a ref() lookup by key."""
    return [S[k] for k in keys], {k: i + 1 for i, k in enumerate(keys)}


# ── 2026/27 rates (see module notes) ─────────────────────────────────────
RO_LEVEL, RO_BUYOUT = 0.472, 69.34                       # ROCs/MWh (GB); £/ROC
RO = RO_LEVEL * RO_BUYOUT                                # £/MWh
CM_TOTAL, CM_PEAK_MWH = 3_474_489_734.79, 11_291_571.95   # £, MWh in Periods of High Demand, 2026/27
CM_RATE = CM_TOTAL / CM_PEAK_MWH                         # £ per MWh used in those periods
BSUOS = (13.74 + 12.49) / 2                              # Apr-Sep 2026, Oct 2026-Mar 2027
TNUOS_LV3 = 14.381374                                    # £/site/day, LV 150-250 kVA
CCL = 8.01                                               # £/MWh (0.801p/kWh)
# Interim levy rates, £/MWh, as (days in force, rate) through April 2026 to March 2027.
CFD_PERIODS = [(91, 10.260), (47, 10.559), (45, 2.068), (35, 5.529), (57, 0.0), (90, 2.979)]
RAB_PERIODS = [(91, 4.683), (92, 4.488), (66, 3.754), (26, 5.151), (90, 3.676)]
CFD = sum(d * r for d, r in CFD_PERIODS) / sum(d for d, _ in CFD_PERIODS)
RAB = sum(d * r for d, r in RAB_PERIODS) / sum(d for d, _ in RAB_PERIODS)

# The example site: 500 MWh a year at low voltage, 200 kVA agreed capacity,
# used like our example office (6.1% of its electricity falls 4pm-7pm on
# working days, November to February).
SITE_MWH, PEAK_SHARE = 500, 0.0609
EXAMPLE = [  # label, how it's charged, £/MWh averaged over the year
    ('Renewables Obligation', f'{RO_LEVEL} certificates per MWh at £{RO_BUYOUT:.2f} each', RO),
    ('Capacity Market', f'about £{CM_RATE:.0f} per MWh used 4pm to 7pm on winter working days; 6.1% of this site\'s use', CM_RATE * PEAK_SHARE),
    ('Balancing (BSUoS)', '£13.74/MWh to September 2026, then £12.49/MWh', BSUOS),
    ('Transmission (TNUoS)', f'£{TNUOS_LV3:.2f} a day for a low-voltage site with 150 to 250 kVA of capacity', TNUOS_LV3 * 365 / SITE_MWH),
    ('Climate Change Levy', '0.801p/kWh', CCL),
    ('Contracts for Difference', '£0 to £10.56/MWh, set each quarter and adjusted in between', CFD),
    ('Nuclear RAB (Sizewell C)', '£3.68 to £5.15/MWh, set each quarter', RAB),
]
EXAMPLE_TOTAL = sum(v for *_, v in EXAMPLE)               # £/MWh
QEP_SMALL_MEDIUM_Q2_2026 = 27.67                          # p/kWh incl CCL, 500-1,999 MWh band, April to June 2026

# DESNZ QEP table 3.4.2, annual, p/kWh including CCL, excluding VAT.
# Bands: very small 0-20 MWh, small 20-499, small/medium 500-1,999, medium 2,000-19,999, large 20,000-69,999 a year.
PRICES = {
    2015: (13.38, 12.22, 10.92, 10.04, 9.78), 2016: (12.75, 12.08, 10.86, 10.01, 9.83),
    2017: (14.00, 12.60, 11.00, 10.49, 10.44), 2018: (15.48, 13.72, 12.19, 11.53, 10.85),
    2019: (16.71, 14.89, 13.51, 12.56, 11.86), 2020: (17.17, 15.47, 14.39, 13.27, 13.11),
    2021: (17.99, 16.25, 15.75, 14.30, 14.08), 2022: (23.84, 20.09, 23.85, 20.21, 19.30),
    2023: (32.28, 32.76, 32.17, 29.04, 27.07), 2024: (32.33, 29.79, 28.88, 28.74, 26.77),
    2025: (34.93, 29.09, 28.25, 25.91, 24.40),
}
BANDS = ['Very small (up to 20 MWh)', 'Small (20 to 499 MWh)', 'Small/medium (500 to 1,999 MWh)', 'Medium (2,000 to 19,999 MWh)', 'Large (20,000 to 69,999 MWh)']


def money(v, dp=0):
    return f'£{v:,.{dp}f}'


# ── Charts (inline SVG, one series, labelled; a table carries the same data) ──
def hbar_chart(rows, label, unit_fmt):
    """Horizontal bars, largest first, as HTML so text stays readable on phones. rows: [(name, value)]."""
    rows = sorted(rows, key=lambda r: -r[1])
    vmax = max(v for _, v in rows)
    return (f'<figure class="hbars" role="img" aria-label="{label}">' + ''.join(
        f'<div class="hbar" title="{name}: {unit_fmt(v)}"><span class="hbar-label">{name}</span>'
        f'<span class="hbar-track"><span class="hbar-fill" style="width:{v / vmax * 100:.1f}%"></span>'
        f'<span class="hbar-value">{unit_fmt(v)}</span></span></div>' for name, v in rows) + '</figure>')


def column_chart(points, label, highlight=(), caption=''):
    """Columns over time, as HTML. points: [(year, value)]; values in pence."""
    vmax = 35
    cols = ''.join(
        f'<div class="col{" col-hi" if yr in highlight else ""}" title="{yr}: {v:.1f}p/kWh">'
        f'<span class="col-value">{v:.1f}</span><span class="col-bar" style="height:{v / vmax * 100:.1f}%"></span>'
        f'<span class="col-year">{str(yr)[2:] if len(points) > 8 else yr}</span></div>' for yr, v in points)
    cap = f'<figcaption>{caption}</figcaption>' if caption else ''
    return f'<figure class="cols" role="img" aria-label="{label}"><div class="cols-plot">{cols}</div>{cap}</figure>'


def wrap_table(html, label):
    return f'<div class="table-wrap" tabindex="0" role="region" aria-label="{label}">{html}</div>'


SECTION_NEXT = [
    ('business-electricity-price.html', "What's in a business electricity price", 'The five parts of the price, with a worked example.'),
    ('non-energy-charges.html', 'Non-energy charges explained', 'Network charges, policy levies and taxes, one by one.'),
    ('electricity-prices-ten-years.html', 'Ten years of business electricity prices', 'From 2015 to 2026, and what drove the changes.'),
    ('non-energy-costs-outlook.html', 'Where non-energy costs are heading', 'Published forecasts and decisions for 2027 and beyond.'),
]


def section_next(this):
    return [x for x in SECTION_NEXT if x[0] != this]


PAGES = []

# ── 1. WHAT'S IN A PRICE ─────────────────────────────────────────────────
_src, n = src('qep', 'ro', 'ro_buyout', 'emrs', 'cm', 'bsuos', 'tnuos', 'ccl', 'vat', 'tcr', 'cfd', 'rab', 'fit')
PAGES.append(guide_page(
  'business-electricity-price.html',
  "What's in a business electricity price?",
  "What's in a business electricity price",
  'A business electricity price is much more than the cost of the energy. Here are the five parts, what each pays for, and a worked example with 2026/27 rates.',
  'The components of a UK business electricity price: wholesale energy, network charges, policy costs, taxes and supplier costs, with a worked 2026/27 example.',
  f'''
<p class="answer">A business electricity price has five parts: the wholesale energy, network charges for moving it, policy costs that pay for low-carbon generation and a secure supply, taxes, and the supplier's own costs and margin. For a business using 500 MWh a year, the network and policy charges we can work out from published 2026/27 rates come to about {EXAMPLE_TOTAL / 10:.1f}p/kWh. That is about a third of the {QEP_SMALL_MEDIUM_Q2_2026}p/kWh that businesses of that size paid on average in April to June 2026.{ref(n['qep'])}</p>

<h2 id="parts">The five parts</h2>
<div class="price-parts">
<div class="price-part"><h3>Wholesale energy</h3><p>The electricity itself, bought on the wholesale market by your supplier. Often called the "commodity" cost.</p></div>
<div class="price-part"><h3>Network charges</h3><ul><li><strong>Transmission (TNUoS)</strong>: the high-voltage national grid</li><li><strong>Distribution (DUoS)</strong>: your local network</li><li><strong>Balancing (BSUoS)</strong>: keeping supply and demand matched</li></ul></div>
<div class="price-part"><h3>Policy costs</h3><ul><li>Renewables Obligation</li><li>Contracts for Difference</li><li>Capacity Market</li><li>Nuclear RAB (Sizewell C)</li><li>Feed-in Tariffs</li></ul></div>
<div class="price-part"><h3>Taxes</h3><ul><li><strong>Climate Change Levy</strong> on business energy</li><li><strong>VAT</strong>, usually at 20%</li></ul></div>
<div class="price-part"><h3>Supplier costs</h3><p>Metering and data services, the supplier's running costs, the cost of managing risk, and its margin.</p></div>
</div>
<p>The non-energy parts, everything except the wholesale energy, are explained one by one in <a href="non-energy-charges.html">non-energy charges explained</a>.</p>

<h2 id="example">A worked example: 500 MWh a year</h2>
<p>Take a business site using {SITE_MWH} MWh a year at low voltage, with 200 kVA of agreed supply capacity. It uses electricity the way our <a href="sample-report.html">example office</a> does, so 6.1% of its use falls between 4pm and 7pm on working days from November to February. That matters for the Capacity Market charge.</p>
<p>These are the charges we can calculate from the rates published for April 2026 to March 2027:</p>
''' + hbar_chart([(lbl, v) for lbl, _, v in EXAMPLE], 'Non-energy charges per MWh for the example site, 2026/27', lambda v: f'£{v:.2f}/MWh') + wrap_table(
  '<table><thead><tr><th>Charge</th><th>Published rate</th><th class="num">£/MWh</th><th class="num">£ a year</th></tr></thead><tbody>'
  + ''.join(f'<tr><td>{lbl}</td><td>{how}</td><td class="num">{v:.2f}</td><td class="num">{money(v * SITE_MWH)}</td></tr>' for lbl, how, v in EXAMPLE)
  + f'<tr><td><strong>Total</strong></td><td>{EXAMPLE_TOTAL / 10:.1f}p/kWh</td><td class="num"><strong>{EXAMPLE_TOTAL:.2f}</strong></td><td class="num"><strong>{money(EXAMPLE_TOTAL * SITE_MWH)}</strong></td></tr></tbody></table>',
  'Example site charges table') + f'''
<p>Sources for each rate: Renewables Obligation{ref(n['ro'], n['ro_buyout'])}, Capacity Market{ref(n['emrs'], n['cm'])}, balancing{ref(n['bsuos'])}, transmission{ref(n['tnuos'])}, Climate Change Levy{ref(n['ccl'])}, Contracts for Difference and nuclear RAB{ref(n['emrs'])}. The CfD and nuclear RAB figures are averages of the rates in force through the year, weighted by days; the Capacity Market figure is the year's total payments divided by the electricity used in the charging periods. Both are our calculations.</p>

<h2 id="missing">What the example leaves out</h2>
<ul><li><strong>Wholesale energy.</strong> It depends on when your supplier bought it and on your contract. See <a href="electricity-prices-ten-years.html">ten years of prices</a>.</li><li><strong>Distribution charges.</strong> They depend on your region, your connection and when you use electricity. Each network operator publishes its own rates.{ref(n['tcr'])}</li><li><strong>Supplier costs and margin</strong>, including metering.</li><li><strong>VAT.</strong> Most business electricity is charged at the standard rate of 20%. A lower rate applies to charities' non-business use and to sites using no more than 33 kWh a day on average. From 1 October 2026 to 30 June 2027 those qualifying supplies in Great Britain are zero-rated.{ref(n['vat'])}</li></ul>
<p>Suppliers handle non-energy charges differently. Some fix them for the length of the contract, others pass changes straight through, and some show them as separate lines on the bill. Your contract should say which.</p>

<h2 id="hh">Why half-hourly data matters here</h2>
<p>Two of these charges depend on <em>when</em> you use electricity. The Capacity Market charge is based entirely on use between 4pm and 7pm on working days from November to February.{ref(n['cm'])} Distribution charges usually have different unit rates for different times of day. Your <a href="analyser/">half-hourly data</a> shows exactly how much you use in those hours, and what could move.</p>
''' + sources(_src),
  [('parts', 'The five parts'), ('example', 'A worked example'), ('missing', 'What the example leaves out'), ('hh', 'Why half-hourly data matters')],
  [("What are non-energy costs on a business electricity bill?", "Everything except the wholesale energy: network charges (transmission, distribution and balancing), policy costs (the Renewables Obligation, Contracts for Difference, Capacity Market, nuclear RAB and Feed-in Tariffs) and the Climate Change Levy."),
   ("How much of a business electricity price is non-energy?", f"For our example 500 MWh-a-year site, the network and policy charges we can calculate from published 2026/27 rates come to about {EXAMPLE_TOTAL / 10:.1f}p/kWh, before distribution charges, supplier costs and VAT. That is about a third of the {QEP_SMALL_MEDIUM_Q2_2026}p/kWh average price for businesses of that size in April to June 2026."),
   ("What VAT rate do businesses pay on electricity?", "Usually the standard rate of 20%. Charities' non-business use and very small supplies (no more than 33 kWh a day on average) qualify for a lower rate, which is 0% in Great Britain from 1 October 2026 to 30 June 2027.")],
  section_next('business-electricity-price.html'),
  f'Components of a UK business electricity price; worked 2026/27 example for a 500 MWh site: published network and policy charges about {EXAMPLE_TOTAL / 10:.1f}p/kWh, about a third of the {QEP_SMALL_MEDIUM_Q2_2026}p/kWh average delivered price (DESNZ, Q2 2026).'))

# ── 2. NON-ENERGY CHARGES ────────────────────────────────────────────────
_src, n = src('tnuos', 'tcr', 'duos', 'bsuos', 'ro', 'ro_buyout', 'cfd', 'emrs', 'cm', 'rab', 'fit', 'ccl', 'vat', 'bics')
TNUOS_BANDS = [('LV1', 'up to 90 kVA', 5.797398), ('LV2', '90 to 150 kVA', 11.51184), ('LV3', '150 to 250 kVA', 14.381374), ('LV4', 'over 250 kVA', 38.180103)]
PAGES.append(guide_page(
  'non-energy-charges.html',
  'Non-energy charges on business electricity bills, explained',
  'Non-energy charges explained',
  'What each network charge, policy levy and tax on a business electricity bill pays for, how it is charged, and the 2026/27 rates.',
  'TNUoS, DUoS, BSUoS, Renewables Obligation, CfD, Capacity Market, nuclear RAB, Feed-in Tariffs and Climate Change Levy explained, with 2026/27 rates.',
  f'''
<p class="answer">Non-energy charges are everything on a business electricity bill apart from the wholesale energy: network charges (TNUoS, DUoS and BSUoS), policy costs (the Renewables Obligation, Contracts for Difference, Capacity Market, nuclear RAB and Feed-in Tariffs) and the Climate Change Levy. Some are charged per unit, some per day and some only at certain times, so when you use electricity can matter as much as how much.</p>
<div class="note"><strong>Rates checked {CHECKED}.</strong> Most change every April; balancing charges change every six months and the CfD and nuclear RAB levies every quarter. Follow the source links for the latest.</div>

<h2 id="networks">Network charges</h2>
<h3 id="tnuos">Transmission (TNUoS)</h3>
<p>Pays for the high-voltage national transmission network. For business sites, the main part is a fixed charge per site per day (the non-locational demand residual), set by charging band. For low-voltage sites with an agreed capacity, the band depends on that capacity.{ref(n['tnuos'])} The bands stay fixed for the current transmission price control.{ref(n['tnuos'])}</p>
''' + wrap_table('<table><thead><tr><th>Band</th><th>Agreed capacity</th><th class="num">£ per site per day, 2026/27</th><th class="num">£ a year</th></tr></thead><tbody>'
  + ''.join(f'<tr><td>{b}</td><td>{c}</td><td class="num">{v:.2f}</td><td class="num">{money(v * 365)}</td></tr>' for b, c, v in TNUOS_BANDS)
  + '</tbody></table>', 'Transmission charges for low-voltage business sites') + f'''
<p><strong>Half-hourly angle:</strong> a fixed daily charge doesn't change with when you use electricity, but your band depends on your agreed capacity. See <a href="supply-capacity.html">supply capacity</a>.</p>

<h3 id="duos">Distribution (DUoS)</h3>
<p>Pays for your local distribution network, run by the network operator for your region (the first two digits of your <a href="mpan-profile-class.html">MPAN</a> tell you which). Charges are a mix of unit rates, capacity charges and daily fixed charges, plus a fixed "residual" charge per site per day, banded for business sites since Ofgem's Targeted Charging Review.{ref(n['tcr'], n['duos'])} Unit rates vary by time band, often called red, amber and green, and each operator sets its own times and rates.{ref(n['duos'])}</p>
<p><strong>Half-hourly angle:</strong> moving use out of the most expensive time band, and keeping peak demand within your agreed capacity, both reduce distribution charges. Your half-hourly data shows how much falls in each band.</p>

<h3 id="bsuos">Balancing (BSUoS)</h3>
<p>Covers the National Energy System Operator's (NESO's) costs of balancing the electricity system. Since April 2023 it has been a fixed tariff per MWh, set in advance for six-month periods.{ref(n['bsuos'])} It is £13.74/MWh for April to September 2026 and £12.49/MWh for October 2026 to March 2027.{ref(n['bsuos'])}</p>

<h2 id="policy">Policy costs</h2>
<h3 id="ro">Renewables Obligation (RO)</h3>
<p>Suppliers must present Renewables Obligation Certificates for each MWh they supply, or pay a buy-out price instead. For 2026/27 the level is 0.472 certificates per MWh in Great Britain and the buy-out price is £69.34, which works out at about £{RO:.2f}/MWh.{ref(n['ro'], n['ro_buyout'])} Energy-intensive industries are fully exempt from these costs.{ref(n['ro'])}</p>

<h3 id="cfd">Contracts for Difference (CfD)</h3>
<p>CfDs give low-carbon generators a fixed price (the strike price). When the market price is below it, generators are paid the difference, funded by a levy on suppliers. When the market price is above it, generators pay the difference back.{ref(n['cfd'])} So the levy falls when wholesale prices rise. It was £10.26/MWh in April to June 2026, was cut in stages from August, and was £0/MWh from 5 November 2026. It is set at £2.98/MWh for January to March 2027.{ref(n['emrs'])}</p>

<h3 id="cm">Capacity Market (CM)</h3>
<p>Pays capacity providers to make sure enough reliable capacity is available, for example during periods of low wind and high demand.{ref(n['cm'])} Payments for October 2026 to September 2027 total £3.47 billion.{ref(n['emrs'])} Suppliers pay according to their customers' share of demand between 4pm and 7pm on working days from November to February.{ref(n['cm'])} Dividing the total by the demand forecast for those hours gives about £{CM_RATE:.0f} for each MWh used in them (our calculation).{ref(n['emrs'])}</p>
<p><strong>Half-hourly angle:</strong> this is the charge most affected by timing. Cutting use between 4pm and 7pm on winter working days cuts it directly.</p>
<p><strong>Solar won't do much here:</strong> in midwinter the sun sets around 4pm across most of the UK, so panels produce little or nothing in these hours. Solar cuts the charges you pay per unit instead. To see how much of a solar system's output your site would use, try the analyser's Solar tab or our sister site, the <a href="https://uksolarcalculator.co.uk/">UK Solar Calculator</a>.</p>

<h3 id="rab">Nuclear RAB</h3>
<p>Funds the construction of new nuclear power stations under the Regulated Asset Base model; the first is Sizewell C. It is collected from suppliers in the same way as the CfD levy.{ref(n['rab'])} The rate was £3.75/MWh from October 2026, rising to £5.15/MWh from 6 December 2026, and is £3.68/MWh for January to March 2027.{ref(n['emrs'])}</p>

<h3 id="fit">Feed-in Tariffs (FiT)</h3>
<p>The scheme that pays owners of small-scale renewable installations, such as rooftop solar, for the electricity they generate. It closed to new applicants on 1 April 2019, but payments to existing installations continue and are funded through suppliers.{ref(n['fit'])}</p>

<h2 id="tax">Taxes</h2>
<h3 id="ccl">Climate Change Levy (CCL)</h3>
<p>A tax on energy used by businesses. The electricity rate is 0.801p/kWh from 1 April 2026 and 0.827p/kWh from 1 April 2027. Holders of a climate change agreement get a 92% discount on electricity.{ref(n['ccl'])}</p>
<h3 id="vat">VAT</h3>
<p>Most business electricity carries VAT at the standard rate of 20%. Charities' non-business use and sites using no more than 33 kWh a day on average qualify for a reduced rate, which is 0% in Great Britain from 1 October 2026 to 30 June 2027.{ref(n['vat'])}</p>

<h2 id="relief">Reliefs for energy-intensive businesses</h2>
<p>Energy-intensive industries are exempt from the indirect costs of the Renewables Obligation.{ref(n['ro'])} From 2027, the British Industrial Competitiveness Scheme will also cut electricity costs by up to £40/MWh for eligible manufacturers, exempting them from the indirect costs of the Renewables Obligation, Capacity Market and Feed-in Tariffs.{ref(n['bics'])}</p>
''' + sources(_src),
  [('networks', 'Network charges'), ('policy', 'Policy costs'), ('tax', 'Taxes'), ('relief', 'Reliefs')],
  [('What is TNUoS on my electricity bill?', 'Transmission Network Use of System charges pay for the national high-voltage grid. For business sites the main part is a fixed charge per site per day, set by band; for low-voltage sites with an agreed capacity the band depends on that capacity.'),
   ('What is DUoS?', 'Distribution Use of System charges pay for your local network. They combine unit rates that vary by time of day, capacity charges and fixed daily charges, set by the network operator for your region.'),
   ('Why did the CfD levy fall to zero?', 'When wholesale prices are above a CfD generator\'s strike price, the generator pays the difference back, which reduces the levy. The CfD interim levy rate was £0/MWh from 5 November 2026.'),
   ('When is the Capacity Market charge calculated?', 'On electricity used between 4pm and 7pm on working days from November to February.')],
  section_next('non-energy-charges.html'),
  'Non-energy charges explained with 2026/27 rates: TNUoS bands (LV1-LV4 £5.80-£38.18/site/day), DUoS time bands, BSUoS £13.74/£12.49/MWh, RO £32.73/MWh, CfD £0-£10.56/MWh, Capacity Market (4-7pm winter working days), nuclear RAB, FiT, CCL 0.801p/kWh, VAT.'))

# ── 3. TEN YEARS OF PRICES ───────────────────────────────────────────────
_src, n = src('qep', 'wmi', 'bsuos_nov')
PAGES.append(guide_page(
  'electricity-prices-ten-years.html',
  'UK business electricity prices, 2015 to 2026',
  'Ten years of business electricity prices',
  'How much UK businesses have paid for electricity since 2015, what happened to wholesale prices in the energy crisis, and what drives prices now.',
  'UK business electricity prices from 2015 to 2026 by size of user (government statistics), wholesale price history and what drives it.',
  f'''
<p class="answer">For a business using 500 to 2,000 MWh a year, the average electricity price was 10.9p/kWh in 2015 and 15.8p/kWh in 2021. It then doubled to 32.2p/kWh in 2023 as wholesale prices spiked, and was 28.3p/kWh in 2025. These are government figures for the delivered price, including the Climate Change Levy but not VAT.{ref(n['qep'])}</p>

<h2 id="delivered">What businesses paid</h2>
<p>The government publishes the average price paid by non-domestic electricity users, by size. The figures are "fully delivered" prices: wholesale energy, network and policy costs and supplier costs all included, VAT excluded.{ref(n['qep'])} This chart shows businesses using 500 to 1,999 MWh a year.</p>
''' + column_chart([(y, PRICES[y][2]) for y in sorted(PRICES)], 'Average electricity price paid by businesses using 500 to 1,999 MWh a year, 2015 to 2025, pence per kWh', highlight=(2022, 2023), caption="Pence per kWh, including the Climate Change Levy, excluding VAT. Years shown as '15 to '25; the darker bars are 2022 and 2023, the years of the energy crisis.") + wrap_table(
  '<table><thead><tr><th>Annual use</th>' + ''.join(f'<th class="num">{y}</th>' for y in (2015, 2019, 2021, 2022, 2023, 2025)) + '</tr></thead><tbody>'
  + ''.join(f'<tr><td>{b}</td>' + ''.join(f'<td class="num">{PRICES[y][i]:.1f}</td>' for y in (2015, 2019, 2021, 2022, 2023, 2025)) + '</tr>' for i, b in enumerate(BANDS))
  + '</tbody></table>', 'Business electricity prices by size of user') + f'''
<p>Pence per kWh, including the Climate Change Levy, excluding VAT. Source: QEP table 3.4.2.{ref(n['qep'])} The latest quarter published, April to June 2026, was {QEP_SMALL_MEDIUM_Q2_2026}p/kWh for the 500 to 1,999 MWh band.{ref(n['qep'])}</p>

<h2 id="wholesale">What happened to wholesale prices</h2>
<p>Ofgem's chart of monthly average day-ahead wholesale prices in Great Britain shows the energy crisis clearly. Reading from that chart:{ref(n['wmi'])}</p>
<ul><li><strong>2015 to 2019:</strong> mostly between about £35 and £65/MWh.</li><li><strong>Spring 2020:</strong> a low of about £25/MWh.</li><li><strong>2021 to 2022:</strong> a steep rise from autumn 2021, peaking above £350/MWh in summer 2022.</li><li><strong>2023 to 2025:</strong> back down, mostly between about £60 and £125/MWh.</li><li><strong>2026:</strong> rising again through the summer and autumn.</li></ul>
<p>NESO's November 2026 forecast puts the average wholesale price for November at £152/MWh, 25% higher than its September forecast of £121/MWh.{ref(n['bsuos_nov'])}</p>

<h2 id="drivers">What drives wholesale prices</h2>
<p>Ofgem names three main factors:{ref(n['wmi'])}</p>
<ul><li><strong>Wind.</strong> Forecasts of higher wind generation usually mean lower day-ahead prices, because less expensive gas-fired generation is needed. Variable wind makes prices volatile.</li><li><strong>Gas and carbon prices.</strong> Gas-fired generators often set the market price, so gas and carbon prices have a strong influence on electricity prices.</li><li><strong>European prices.</strong> Great Britain trades electricity with Europe through interconnectors. When it relies on imports, British prices must be high enough to attract them.</li></ul>
<p>Many businesses don't pay day-ahead prices directly. Suppliers buy much of their energy in advance, so changes in the wholesale market reach contract prices gradually, depending on when your contract was priced.</p>
''' + sources(_src),
  [('delivered', 'What businesses paid'), ('wholesale', 'Wholesale prices'), ('drivers', 'What drives wholesale prices')],
  [('How much have business electricity prices risen since 2015?', 'For businesses using 500 to 1,999 MWh a year, the average delivered price rose from 10.9p/kWh in 2015 to 28.3p/kWh in 2025, according to government statistics (including the Climate Change Levy, excluding VAT).'),
   ('When did wholesale electricity prices peak?', "Ofgem's monthly day-ahead price chart peaks above £350/MWh in summer 2022."),
   ('What sets the wholesale electricity price in Great Britain?', 'Ofgem points to wind generation, gas and carbon prices (gas-fired plants often set the price) and European prices via interconnectors.')],
  section_next('electricity-prices-ten-years.html'),
  'UK business electricity prices 2015-2025 by size band (DESNZ QEP 3.4.2): 500-1,999 MWh band 10.9p (2015), 15.8p (2021), 32.2p (2023), 28.3p/kWh (2025); wholesale history from Ofgem; drivers: wind, gas and carbon, European prices.'))

# ── 4. OUTLOOK ───────────────────────────────────────────────────────────
_src, n = src('bsuos', 'bsuos28', 'ro', 'ro_buyout', 'ro2728', 'bics', 'ccl', 'ccl28', 'emrs', 'cmp440', 'ed3', 'vat', 'cm')
OUTLOOK = [  # charge, 2026/27, next published figure, status, source keys
    ('Balancing (BSUoS)', '£13.74/MWh (Apr to Sep 2026); £12.49/MWh (Oct 2026 to Mar 2027)', '£21.67/MWh (Apr to Sep 2027); £18.42/MWh (Oct 2027 to Mar 2028)', 'Draft; final tariffs due December 2026', ('bsuos', 'bsuos28')),
    ('Renewables Obligation', f'0.472 certificates per MWh (about £{RO:.2f}/MWh)', f'0.369 certificates per MWh from April 2027 (about £{0.369 * RO_BUYOUT:.2f}/MWh at this year\'s buy-out price), or 0.394 if the manufacturers\' relief is in place in time', 'Published; buy-out price for 2027/28 not yet set', ('ro', 'ro_buyout', 'ro2728')),
    ('Climate Change Levy', '0.801p/kWh', '0.827p/kWh from April 2027, then frozen at that level from April 2028', 'Confirmed', ('ccl', 'ccl28')),
    ('Contracts for Difference', '£0 to £10.56/MWh during the year', '£2.98/MWh for January to March 2027', 'Set quarterly; moves opposite to wholesale prices', ('emrs',)),
    ('Nuclear RAB', '£3.68 to £5.15/MWh during the year', '£3.68/MWh for January to March 2027', 'Set quarterly', ('emrs',)),
    ('Capacity Market', '£3.47 billion for October 2026 to September 2027', 'The next year\'s total is published the summer before it starts', 'Published annually', ('emrs', 'cm')),
    ('Transmission (TNUoS)', 'Fixed daily charges by band', 'A proposal (CMP440) to reintroduce demand transmission charges from April 2027', 'Proposal; awaiting decision', ('cmp440',)),
    ('Distribution (DUoS)', 'Set by each network operator', 'New price control for 2028 to 2033; Ofgem to approve the settlement by the end of 2027', 'In preparation', ('ed3',)),
]
PAGES.append(guide_page(
  'non-energy-costs-outlook.html',
  'Where non-energy electricity costs are heading from 2027',
  'Where non-energy costs are heading',
  'Published forecasts and decisions for each non-energy charge on business electricity bills: what is confirmed, what is draft, and what is still undecided.',
  'Published forecasts for UK non-energy electricity costs from 2027: balancing charges, levies, Climate Change Levy, network price controls and manufacturers\' relief.',
  f'''
<p class="answer">Published figures point to higher balancing charges from April 2027: NESO's draft tariff is £21.67/MWh for April to September 2027, up from £13.74/MWh, driven by constraint costs and wholesale prices. The Climate Change Levy rises to 0.827p/kWh and is then frozen, while the Renewables Obligation falls to 0.369 certificates per MWh. These are published forecasts and decisions from the bodies that set the charges, not our predictions.{ref(n['bsuos28'], n['ccl'], n['ro2728'])}</p>
<div class="note"><strong>Checked {CHECKED}.</strong> Draft figures change. Each line says whether it is confirmed, draft or a proposal, and links to the source.</div>

<h2 id="table">Charge by charge</h2>
''' + wrap_table('<table><thead><tr><th>Charge</th><th>2026/27</th><th>Next published figure</th><th>Status</th></tr></thead><tbody>'
  + ''.join(f'<tr><td>{c}</td><td>{now}</td><td>{nxt}{ref(*[n[k] for k in keys])}</td><td>{st}</td></tr>' for c, now, nxt, st, keys in OUTLOOK)
  + '</tbody></table>', 'Outlook for non-energy charges') + f'''

<h2 id="balancing">Balancing costs are forecast to rise</h2>
<p>NESO's draft tariffs for 2027/28 are £21.67/MWh for April to September 2027 and £18.42/MWh for October 2027 to March 2028. NESO attributes the rise to higher constraint costs (up 32% for the first period) and higher wholesale prices (up 33%).{ref(n['bsuos28'])} Final tariffs are published each December.{ref(n['bsuos'])}</p>

<h2 id="manufacturers">Relief for manufacturers moves costs to others</h2>
<p>From 2027 the British Industrial Competitiveness Scheme will cut electricity costs for eligible manufacturers by up to £40/MWh, by exempting them from the indirect costs of the Renewables Obligation, Capacity Market and Feed-in Tariffs.{ref(n['bics'])} Exempt electricity doesn't carry these costs, so they are spread over everyone else. The government's own calculation shows the 2027/28 Renewables Obligation level for other users rising from 0.369 to 0.394 certificates per MWh if the scheme is in place in time.{ref(n['ro2728'])}</p>

<h2 id="networks">Networks: a new price control from 2028</h2>
<p>Ofgem has set out how it will judge the distribution network operators' plans for 2028 to 2033, and will approve the final settlement by the end of 2027. It expects demand on distribution networks to rise, while promising tighter cost controls to stop unnecessary investment being recovered through bills.{ref(n['ed3'])} Separately, NESO's CMP440 proposal would reintroduce demand transmission charges from 1 April 2027.{ref(n['cmp440'])} Check for Ofgem's decision before relying on it.</p>

<h2 id="levies">Levies that track wholesale prices</h2>
<p>The CfD levy moves the opposite way to wholesale prices: it fell to £0/MWh from 5 November 2026 and is set at £2.98/MWh for January to March 2027.{ref(n['emrs'])} If wholesale prices stay high, it may stay low; if they fall, it will rise.</p>

<h2 id="vat">The temporary VAT zero rate ends in June 2027</h2>
<p>The 0% rate for qualifying supplies in Great Britain, including charities' non-business use and very small business supplies, runs from 1 October 2026 to 30 June 2027.{ref(n['vat'])} Most business electricity is unaffected and stays at 20%.</p>

<h2 id="you">What you can do</h2>
<ul><li><strong>Check your contract</strong> to see which non-energy charges are fixed and which are passed through when they change.</li><li><strong>Look at your use between 4pm and 7pm on winter working days.</strong> The Capacity Market charge is based on it.{ref(n['cm'])} Your <a href="analyser/">half-hourly data</a> shows exactly how much falls in that window.</li><li><strong>Check your agreed capacity.</strong> Transmission charges for low-voltage sites are banded by it. See <a href="supply-capacity.html">supply capacity</a>.</li><li><strong>Cut use while closed.</strong> Most charges are per unit, so every unit saved reduces them. Start with <a href="out-of-hours-electricity.html">out-of-hours use</a>.</li></ul>
''' + sources(_src),
  [('table', 'Charge by charge'), ('balancing', 'Balancing costs'), ('manufacturers', 'Relief for manufacturers'), ('networks', 'Networks from 2028'),
   ('levies', 'Levies that track wholesale'), ('vat', 'VAT zero rate'), ('you', 'What you can do')],
  [('Will non-energy electricity costs go up in 2027?', "Some will. NESO's draft balancing charge for April to September 2027 is £21.67/MWh, up from £13.74/MWh, and the Climate Change Levy rises to 0.827p/kWh. The Renewables Obligation level falls. Final balancing tariffs are published in December."),
   ('What is the British Industrial Competitiveness Scheme?', 'A scheme starting in 2027 that cuts electricity costs by up to £40/MWh for eligible manufacturers by exempting them from the indirect costs of the Renewables Obligation, Capacity Market and Feed-in Tariffs.'),
   ('Will the Climate Change Levy keep rising?', 'The electricity rate rises to 0.827p/kWh from April 2027 and is then frozen at that level from April 2028, according to HMRC.')],
  section_next('non-energy-costs-outlook.html'),
  'Outlook for UK non-energy electricity costs: BSUoS draft £21.67/MWh (Apr-Sep 2027) and £18.42/MWh (Oct 2027-Mar 2028); RO 0.369 ROC/MWh 2027/28 (0.394 with BICS); CCL 0.827p/kWh from April 2027 then frozen; CfD £2.98/MWh Q1 2027; ED3 network price control from 2028.'))
