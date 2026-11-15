"""
Solar tab: why solar suits many businesses, why the share used on site
matters most, what half-hourly data tells you before you size a system, and
how to take the figures to the UK Solar Calculator.

Worked-example figures come from the analyser's own solar estimate
(analyser/src/local/solarFit.ts) run on site/samples/example-office.csv at the
UK average output (905 kWh/kWp). If that model or the sample file changes,
re-run it and update EXAMPLE below. Values are first-year, at the UK Solar
Calculator's default unit price (25p/kWh) and export rate (5p/kWh).

REVIEW EACH APRIL with the price pages: the Ofgem SEG scope, the capital
allowance and business rates references, and the calculator's assumptions.
"""
from kit import (NAV_PARENT, Page, SOLAR_URL, guide, page_hero, faq_section, sources,
                 toc, updated_line)
from pages_guides import HOME

FILE = 'solar.html'
CALC = f'{SOLAR_URL}calculator.html'
SOLAR_CONTACT = f'{SOLAR_URL}contact.html?src=hhi'
CRUMBS = [HOME, ('Solar', FILE)]
NAV_PARENT[FILE] = FILE


def ref(*n):
    return f'<sup><a href="#sources">{",".join(str(x) for x in n)}</a></sup>'


SRC = [
    ('UK Solar Calculator: How the calculator works (method and assumptions)', f'{SOLAR_URL}how-it-works.html'),
    ('Ofgem: Smart Export Guarantee (SEG)', 'https://www.ofgem.gov.uk/environmental-and-social-schemes/smart-export-guarantee-seg'),
    ('UK Solar Calculator: Planning, grid connection and other hurdles', f'{SOLAR_URL}planning-and-grid.html'),
    ('Explanatory Memorandum to SI 2022/405, business rates exemption for renewable plant',
     'https://www.legislation.gov.uk/uksi/2022/405/pdfs/uksiem_20220405_en.pdf'),
    ('GOV.UK: Permanent full expensing for companies investing in plant and machinery',
     'https://www.gov.uk/government/publications/capital-allowances-permanent-full-expensing/capital-allowances-permanent-full-expensing-for-companies-investing-in-plant-and-machinery'),
    ('UK Solar Calculator: How long does commercial solar take to pay back?', f'{SOLAR_URL}commercial-solar-payback.html'),
    ('GOV.UK: Standard Assessment Procedure (SAP 10.3)', 'https://www.gov.uk/guidance/standard-assessment-procedure'),
    ('Department for Energy Security and Net Zero: Energy Trends section 6, renewables (table ET 6.1, solar generation by quarter)',
     'https://www.gov.uk/government/statistics/energy-trends-section-6-renewables'),
]

# Example office, UK average output. (kWp, generated, used on site, share used, share of the site's electricity)
EXAMPLE = [
    (26.3, 23728, 20886, 88, 26),
    (52.6, 47457, 34214, 72, 43),
    (105.3, 95003, 43613, 46, 55),
]
USE = 79137


def gbp(x):
    return f'£{round(x):,}'


def value(gen, used, unit=0.25, export=0.05):
    return used * unit + (gen - used) * export


def example_rows():
    out = []
    for kwp, gen, used, sc, cov in EXAMPLE:
        out.append(f'<tr><td style="white-space:nowrap">{kwp:g} kWp</td><td class="num">{gen:,} kWh</td><td class="num">{sc}%</td>'
                   f'<td class="num">{cov}%</td><td class="num">{gbp(value(gen, used))}</td>'
                   f'<td class="num">{gbp(value(gen, gen * 0.8))}</td></tr>')
    return ''.join(out)


big = EXAMPLE[2]
OVERSTATE = value(big[1], big[1] * 0.8) - value(big[1], big[2])
OVERSTATE_PCT = round(OVERSTATE / value(big[1], big[2]) * 100)

FAQS = [
    ('Can half-hourly data tell me what size of solar system to fit?',
     "It tells you the most important half of the answer: how much of a system's output you would use yourself at each size. "
     "Your roof, budget and grid connection set the other half. The analyser estimates the first; the UK Solar Calculator "
     "works out what fits on your roof and what it would cost and save."),
    ('Why not just fit as many panels as the roof will take?',
     "Because solar you can't use is exported for a few pence. Past a certain size, each extra panel mostly adds export. "
     "In our example office, doubling the system from about 53 to 105 kWp raises the share of the site's electricity "
     "supplied by solar from 43% to 55%, while the share of the output it uses falls from 72% to 46%. A full roof can "
     "still make sense, but only if the numbers work at the lower share used on site."),
    ('Does solar reduce standing charges or capacity charges?',
     "No. Standing charges are per day and capacity charges are per kVA of agreed supply capacity, so they stay the same. "
     "Solar reduces the units you buy, and with them the charges priced per kWh. It also does little for charges linked to "
     "winter evening peaks, because it's dark by about 4pm in midwinter. See "
     '<a href="non-energy-charges.html">non-energy charges explained</a>.'),
    ('Will my half-hourly data look different once solar is fitted?',
     "Yes. Your main meter records what you import from the grid, so solar you use on site disappears from the data and "
     "daytime demand looks lower. Size a system from data recorded before solar was fitted. Afterwards, use the analyser to "
     "check the fall in imports against what you expected, as in <a href=\"proving-savings.html\">proving a saving worked</a>."),
    ('Is my meter data sent to the UK Solar Calculator?',
     "No. The button on the analyser's Capacity tab passes only the site's annual use and the estimated share used on site "
     "at a dozen system sizes. They go in the part of the web address after the #, which browsers don't send to any server. "
     "Your readings stay on your computer."),
    ('Should I add a battery?',
     "Only if the numbers work. A battery stores solar you would otherwise export and uses it later, usually in the evening. "
     "Your half-hourly data shows how much you use after sunset on sunny days, which is the most a battery could shift. "
     "The UK Solar Calculator lets you model the system with and without one."),
]

TOC = [('why', 'Why businesses fit solar'), ('share', 'The figure that matters most'), ('data', 'What your data tells you'),
       ('example', 'A worked example'), ('how', 'From your data to a solar estimate'), ('calculator', 'What the calculator does'),
       ('limits', 'What this can and cannot tell you'), ('questions', 'Questions people ask'), ('sources', 'Sources')]

MAIN = f'''{updated_line()}
<p class="answer">Solar saves the most when you use its output yourself, because every unit you use saves your full unit price and every unit you export earns a few pence. Your half-hourly data shows how much daytime electricity your site really uses, so you can see how much of a system's output you would use at each size. Our sister site, the <a href="{SOLAR_URL}">UK Solar Calculator</a>, then works out what fits on your roof, what it costs and how soon it pays back.</p>

<h2 id="why">Why businesses fit solar</h2>
<ul>
<li><strong>It cuts the units you buy.</strong> Solar you use on site replaces electricity you would otherwise buy at your full unit price.{ref(1)} With business prices well above where they were ten years ago (see <a href="electricity-prices-ten-years.html">ten years of business electricity prices</a>), each kWh you don't buy is worth more than it was.</li>
<li><strong>Most workplaces use electricity in daylight.</strong> Offices, schools, shops, workshops and many public buildings are busiest in the middle of the day, when solar generates most.</li>
<li><strong>You can be paid for what you export.</strong> Under the Smart Export Guarantee, installations of up to 5 MW in Great Britain can be paid by a supplier for electricity they export. Suppliers set their own rates.{ref(2)}</li>
<li><strong>Rooftop solar rarely needs planning permission in England.</strong> Since December 2023, rooftop solar on non-domestic buildings has been permitted development with no capacity limit, with exceptions such as listed buildings. Most systems still need approval from the local network operator under G99.{ref(3)}</li>
<li><strong>There is tax and rates help.</strong> Plant used to generate renewable power on site has been exempt from business rates in England since April 2022,{ref(4)} and companies can claim full expensing on qualifying plant and machinery.{ref(5)} Check how they apply to you with your adviser.</li>
<li><strong>You don't have to buy it.</strong> Under a Power Purchase Agreement, a funder pays for and owns the system and you buy its electricity at an agreed rate.{ref(1)}</li>
</ul>
<p>Most UK commercial rooftop systems pay back in roughly four to eight years on the UK Solar Calculator's own worked figures.{ref(6)} Where yours falls depends mostly on one number.</p>

<h2 id="share">The figure that matters most: how much you use yourself</h2>
<p>At a 25p unit price, a kWh of solar you use saves 25p. A kWh you export earns about 5p, the rate the UK Solar Calculator assumes.{ref(1)} That five-fold gap means the share of output you use on site moves the savings more than almost any other input.</p>
<p>Without data, people guess. The calculator starts at 80%, which suits sites busy through the working week.{ref(1)} But the right figure depends on the size of the system as much as the site. A small system on a busy building may use all of its output. A large one on the same building may export half, especially at weekends and on long summer evenings. Your half-hourly data replaces the guess with a measured estimate at each size.</p>

<h2 id="data">What your half-hourly data tells you before you size a system</h2>
<div class="table-wrap"><table><thead><tr><th>What the data shows</th><th>Why it matters for solar</th><th>Where to look</th></tr></thead><tbody>
<tr><td>Daytime demand, weekday and weekend</td><td>Sets how much output you can use at each size. Quiet weekends mean more export from a large system.</td><td>Heatmap; Capacity tab</td></tr>
<tr><td>Base load</td><td>What runs even when the building is closed. On a sunny Sunday this is all the solar you can use.</td><td><a href="base-load.html#solar">Base load and solar</a></td></tr>
<tr><td>Summer and winter pattern</td><td>About three quarters of a year's solar output comes from April to September.{ref(8)} Summer daytime demand matters more than winter's.</td><td>Heatmap; monthly chart</td></tr>
<tr><td>Peak demand and supply capacity</td><td>How much headroom your connection has, and what the network operator will ask about in a G99 application.</td><td><a href="supply-capacity.html#solar">Solar and your connection</a></td></tr>
<tr><td>Evening use on sunny days</td><td>The most a battery could shift from midday to evening.</td><td>Day profile</td></tr>
<tr><td>Out-of-hours waste</td><td>Fix it first. Cutting waste lowers the demand solar has to match, so size the system on the building you'll have afterwards.</td><td><a href="out-of-hours-electricity.html">Out-of-hours use</a></td></tr>
</tbody></table></div>

<h2 id="example">A worked example: the sample office</h2>
<p>Our <a href="example-office-analysis.html">example office</a> uses about {USE:,} kWh a year and is quiet on Sundays and busy only on some Saturdays. Here is what the analyser estimates at three system sizes, at UK average output (905 kWh per kWp). Values are for the first year at 25p/kWh for solar used on site and 5p/kWh for export, before price rises and panel ageing. "Covers" is the share of the site's electricity solar would supply. "Value" uses the measured share used on site; "At 80%" is the same system if you had guessed 80%.</p>
<div class="table-wrap" tabindex="0" role="region" aria-label="Worked example by system size"><table><thead><tr><th>Size</th><th class="num">Output a year</th><th class="num">Used on site</th><th class="num">Covers</th><th class="num">Value</th><th class="num">At 80%</th></tr></thead><tbody>
{example_rows()}
</tbody></table></div>
<p>At about 53 kWp, assuming 80% instead of the measured 72% overstates the first-year value by about {gbp(value(EXAMPLE[1][1], EXAMPLE[1][1] * 0.8) - value(EXAMPLE[1][1], EXAMPLE[1][2]))}. At 105 kWp, the measured share is 46%, and assuming 80% overstates it by about {gbp(OVERSTATE)} a year ({OVERSTATE_PCT}%). Over a 25-year system life that difference decides whether the larger system is worth it. That's the mistake half-hourly data stops you making.</p>
<p class="note">The UK Solar Calculator models systems of 50 kWp and above, so a site this small sits at the bottom of its range. Larger sites follow the same pattern at a bigger scale.{ref(1)}</p>

<h2 id="how">From your data to a solar estimate, in three steps</h2>
<ol>
<li><strong>Load a year of half-hourly data</strong> into the <a href="analyser/">analyser</a>. It runs in your browser and nothing is uploaded. Need the data? See <a href="get-your-data.html">how to get your half-hourly data</a>.</li>
<li><strong>Open the site and choose the Capacity tab.</strong> "Solar: how much would you use?" shows the output, the share used on site and the share of your electricity solar would supply at three sizes. Pick your region to match your location.</li>
<li><strong>Choose "Size solar for this site".</strong> The UK Solar Calculator opens with your figures. Draw your roof on the map or enter its size, and the calculator sets the share used on site for the system that fits, then works out cost, savings and payback.</li>
</ol>
<p>Only the site's annual use and the share used on site at a dozen sizes are passed, in the part of the web address after the #, which browsers don't send to any server. See the <a href="privacy.html">privacy notice</a>.</p>

<h2 id="calculator">What the UK Solar Calculator does</h2>
<ul>
<li><strong>Measures your roof</strong> from satellite imagery or the dimensions you enter, for pitched and flat roofs, ground mounts and carports.{ref(1)}</li>
<li><strong>Estimates generation at your postcode</strong> from the government's SAP 10.3 sunshine data for 21 UK regions.{ref(1,7)}</li>
<li><strong>Prices the system</strong> from UK market benchmarks per kWp, including an inverter replacement in year 13.{ref(1)}</li>
<li><strong>Compares buying outright with a PPA</strong>, with payback, return and net benefit over 25 years.{ref(1)}</li>
<li><strong>Models a battery</strong> if you want one, and produces a 25-year PDF report you can share.{ref(1)}</li>
</ul>
<p>It's free and run by the same team, <a href="about.html">Kinetic Energy Consulting</a>. If you want help turning an estimate into a project, <a href="{SOLAR_CONTACT}">ask the solar team</a>.</p>

<h2 id="limits">What this can and cannot tell you</h2>
<p>The analyser's estimate uses a typical UK solar day, scaled to your region's annual output and to the UK's actual seasonal pattern. It doesn't know about cloudy weeks, shading, the direction your roof faces or what you'll change in future, so treat it as a planning figure, not a guarantee. The calculator's results are estimates, not a quotation. A site survey, a structural check and a network operator's offer come before any firm price.{ref(1,3)}</p>
{faq_section(FAQS)}
{sources(SRC)}'''

SIDE = f'''{toc(TOC)}
    <div class="side-cta"><strong>Size solar for your roof</strong><p>Postcode, roof and energy price. Results in seconds, with a 25-year report.</p><a href="{CALC}" class="btn">Open the UK Solar Calculator</a></div>'''

END = f'''<section class="cta-strip">
  <div class="cta-strip-inner">
    <h2 class="cta-strip-title">Measure it, then size it</h2>
    <div class="cta-strip-btns">
      <a href="analyser/" class="btn btn-gold btn-lg">Open the analyser</a>
      <a href="{CALC}" class="btn btn-outline-white btn-lg">Open the UK Solar Calculator</a>
    </div>
    <p class="cta-strip-lead">Both are free, with no sign-up. Want to talk it through? <a href="{SOLAR_CONTACT}" style="color:inherit;text-decoration:underline">Contact the solar team</a>.</p>
  </div>
</section>'''

PAGES = [Page(
    FILE, 'Solar sizing from half-hourly data | Half Hourly Insights',
    'Use your half-hourly electricity data to see how much solar your site would use, then size the system and payback in the UK Solar Calculator.',
    page_hero('Solar', 'Size solar from how your site really uses electricity',
              "Your half-hourly data shows how much of a solar system's output you'd use yourself. That's the number that decides whether solar pays.",
              crumbs=CRUMBS, image='solar')
    + guide(MAIN, SIDE).replace('<div class="side-cta"><strong>Try it on your own data</strong>', '<div class="side-cta"><strong>Measure it from your data</strong>', 1)
    + END,
    crumbs=CRUMBS, faqs=FAQS, article=True, section='Core pages',
    summary='How half-hourly data shows how much solar a site would use, and how to take that to the UK Solar Calculator to size the system.')]
