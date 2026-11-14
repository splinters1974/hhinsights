"""
Guides and sector pages. Each guide opens with a direct answer (what search
and AI answer engines quote), carries a few questions marked up as FAQPage,
and ends with links to related guides.

Figures in the worked example come from the analyser run on
site/samples/example-office.csv (made-up data). Re-check them if that file
or the engine changes.
"""
from kit import (NAV_PARENT, SOLAR_URL, Page, cta, faq_section, guide, page_hero, related, sources, strip_tags, toc,
                 updated_line)

HOME = ('Home', 'index.html')
GUIDES = ('Guides', 'guides.html')
SECTORS = ('Sectors', 'sectors.html')
SOLAR = f'<a href="{SOLAR_URL}">UK Solar Calculator</a>'


def guide_page(file, title, h1, lead, description, main, toc_items, faqs, next_links, summary, crumbs=None):
    crumbs = crumbs or [HOME, GUIDES, (h1, file)]
    NAV_PARENT[file] = crumbs[1][1]
    body = (page_hero(crumbs[1][0] if crumbs[1] != GUIDES else 'Guide', h1, lead, crumbs=crumbs)
            + guide(updated_line() + main + faq_section(faqs) + related(next_links), toc(toc_items + [('questions', 'Questions people ask')]))
            + cta('Try it on your own data', 'Free, no sign-up, and your file stays on your computer.'))
    return Page(file, title, description, body, crumbs=crumbs, faqs=faqs, article=True, summary=summary,
                section='Guides' if crumbs[1] == GUIDES else 'Sectors')


PAGES = []

# ── WORKED EXAMPLE ──────────────────────────────────────────────────────
PAGES.append(guide_page(
  'example-office-analysis.html',
  'Worked example: a year of half-hourly data for one office',
  'Worked example: one office, one year',
  'A year of half-hourly data from a small office, run through the analyser. The office and its data are made up, but every figure below is what the analyser reports for it.',
  'One office, one year of half-hourly data: out-of-hours use, base load, peaks against supply capacity, and what to do next.',
  f'''
<p class="answer">A third of this office's electricity (33%) was used while the building was shut. After allowing for what never switches off, that is about £2,800 a year at 25p/kWh, and almost half of it happens on Saturdays.</p>

<div class="note"><strong>Made-up data.</strong> The office is invented so you can see the method without anyone's real data. <a href="samples/example-office.csv" download>Download the file</a> and load it into the <a href="analyser/">analyser</a> to follow along.</div>

<h2 id="headline">The headline figures</h2>
<div class="table-wrap"><table><thead><tr><th>Measure</th><th class="num">Value</th><th>What it means</th></tr></thead><tbody>
<tr><td>Electricity a year</td><td class="num">79,191 kWh</td><td>Scaled from 363 days of valid readings (99.5% coverage)</td></tr>
<tr><td>Energy cost a year</td><td class="num">£19,798</td><td>At a flat 25p/kWh, before standing and capacity charges</td></tr>
<tr><td>Base load</td><td class="num">2.6 kW</td><td>The level demand rarely drops below</td></tr>
<tr><td>Highest half hour</td><td class="num">25.5 kW</td><td>28 January 2025, midday</td></tr>
<tr><td>Use while shut</td><td class="num">33%</td><td>With the default office hours, 07:00 to 19:00 on weekdays</td></tr>
<tr><td>Out-of-hours excess</td><td class="num">£2,776</td><td>Energy used while shut, above the base load, priced at 25p/kWh</td></tr>
</tbody></table></div>

<h2 id="split">Where the energy goes</h2>
<p>The analyser splits every half hour at the base load. The three parts add up to the total:</p>
<ul><li><strong>Base load, 29%</strong> (22,606 kWh): what runs around the clock.</li><li><strong>Open hours above base load, 57%</strong> (45,062 kWh): the building doing its job.</li><li><strong>Closed-hours excess, 14%</strong> (11,035 kWh): use above base load while the building should be shut. This is where to look first.</li></ul>

<h2 id="findings">What the analyser found</h2>
<h3>1. Out-of-hours use: £2,776 a year (high impact)</h3>
<p>The breakdown by day type is the useful part:</p>
<div class="table-wrap"><table><thead><tr><th>When</th><th class="num">Above base load</th></tr></thead><tbody>
<tr><td>Saturdays</td><td class="num">5,155 kWh</td></tr><tr><td>Weekday evenings and nights</td><td class="num">3,750 kWh</td></tr>
<tr><td>Bank holidays</td><td class="num">1,408 kWh</td></tr><tr><td>Sundays</td><td class="num">722 kWh</td></tr></tbody></table></div>
<p>Saturdays account for almost half. Sundays are quiet, so this isn't plant running all weekend: the building is being used on some Saturdays. Either that's planned (then the calendar should say so, and the figure falls) or a Saturday booking is running the whole building.</p>

<h3>2. Seven bank holidays look like working days (medium impact)</h3>
<p>Seven bank holidays used at least 80% of a normal weekday, including Christmas Day and Boxing Day. If the office was shut, heating and ventilation schedules probably don't know about bank holidays. If it was open, the calendar should be changed.</p>

<h3>3. Early starts and late finishes: £629 a year (low impact)</h3>
<p>Demand rises before opening and stays up after closing: about 1,250 kWh a year above base load in the two hours before opening, and the same in the two hours after closing. Optimum-start and time-clock settings are the usual cause.</p>

<h2 id="capacity">Supply capacity</h2>
<p>Assuming an agreed supply capacity of 40 kVA and a power factor of 0.95, the highest half hour reaches 27 kVA, 67% of capacity. Keeping a 10% safety margin, the site could take about 9 kW of constant new load. That's enough for modest EV charging, not a heat pump for the whole building. See <a href="supply-capacity.html">supply capacity and kVA</a>.</p>

<h2 id="next-steps">What we'd do next</h2>
<ol><li><strong>Confirm the opening hours</strong>, including Saturdays. Every out-of-hours figure depends on them.</li><li><strong>Check the heating and ventilation schedules</strong> for bank holidays and start times.</li><li><strong>Walk the building on a Saturday</strong> to see what's on and who is using it.</li><li><strong>Look at the base load</strong>: 2.6 kW running all year is about 22,800 kWh, roughly £5,700 at 25p/kWh. See <a href="base-load.html">how to bring it down</a>.</li></ol>
<p>57% of this office's electricity is used while it's open, during the working day, which is when on-site solar generates. The {SOLAR} estimates what a roof system would save.</p>
''',
  [('headline', 'The headline figures'), ('split', 'Where the energy goes'), ('findings', 'What the analyser found'), ('capacity', 'Supply capacity'), ('next-steps', "What we'd do next")],
  [('Is this real data?', 'No. The office and its readings are made up, so the method can be shown without anyone\'s real data. Every figure is what the analyser reports for the example file.'),
   ('How long does an analysis like this take?', 'Loading a year of data takes about a minute. Confirming the opening hours and reading the findings takes longer, and matters more.'),
   ('Are these figures savings?', 'No. They are what each pattern costs now at 25p/kWh. A saving depends on what you change.')],
  [('out-of-hours-electricity.html', 'Out-of-hours use', 'How to find and cut use while the building is shut.'),
   ('base-load.html', 'Base load', 'What never switches off, and why it adds up.'),
   ('get-your-data.html', 'Get your own data', 'What to ask your supplier for.')],
  'A small office run through the analyser: 33% of use while shut, £2,776 a year above base load, almost half on Saturdays; base load 2.6 kW; 67% of a 40 kVA supply.',
  crumbs=[HOME, GUIDES, ('Worked example', 'example-office-analysis.html')]))

# ── OUT-OF-HOURS ────────────────────────────────────────────────────────
PAGES.append(guide_page(
  'out-of-hours-electricity.html',
  'Out-of-hours electricity use: how to find and cut it',
  'Out-of-hours electricity use',
  'Electricity used when a building should be shut is often the cheapest consumption to cut. Here is how to find it in half-hourly data, and what usually causes it.',
  'How to find out-of-hours electricity use in half-hourly data, what causes it, and how to cut it with controls and schedules, not new equipment.',
  '''
<p class="answer">Out-of-hours use is electricity used while a building should be shut. Compare each half hour against the opening hours and subtract what never switches off (the base load); what's left is the out-of-hours excess. It's usually the cheapest use to cut, because the fix is a setting, not new equipment.</p>

<h2 id="what">What counts as out-of-hours</h2>
<p>Any half hour outside the building's opening hours: evenings, nights, weekends, bank holidays and closure periods. Not all of it is waste. Some load has to run all the time, such as servers, fridges, security and emergency lighting. That's the <a href="base-load.html">base load</a>.</p>
<p>The useful figure is the <strong>excess</strong>: use while shut, above the base load. In the analyser it's called the closed-hours excess, and it's the figure sites are ranked by.</p>

<h2 id="find">How to find it</h2>
<ol><li><strong>Set the opening hours properly.</strong> Everything depends on them. Include bank holidays, closure weeks and regular evening or weekend use.</li><li><strong>Look at the heatmap.</strong> Every half hour of the year in one picture: open hours show as a bright band, and anything bright outside it is out-of-hours use.</li><li><strong>Split it by day type.</strong> Weeknights, Saturdays, Sundays and bank holidays usually have different causes.</li><li><strong>Check the edges of the day.</strong> Demand that rises an hour or two before opening, or stays up after closing, points to time clocks and optimum-start settings.</li></ol>

<h2 id="causes">What usually causes it</h2>
<ul><li>Heating, ventilation and cooling running to the wrong schedule, or not knowing about bank holidays</li><li>Lighting left on, or on timers that no longer match the building's use</li><li>A small evening or weekend booking running the whole building</li><li>Plant left in hand (manual override) after maintenance</li><li>IT, catering and hot water equipment left on rather than on timers</li></ul>

<h2 id="cut">How to cut it</h2>
<p>Most of the fixes are settings: building management system schedules, time clocks, holiday calendars and switch-off routines. Start with the biggest block, often weekends or a recurring evening, and check the half-hourly data a month later to see whether it worked. The analyser's before-and-after comparison is built for exactly this.</p>
''',
  [('what', 'What counts as out-of-hours'), ('find', 'How to find it'), ('causes', 'What usually causes it'), ('cut', 'How to cut it')],
  [('Is all out-of-hours use waste?', 'No. Some load must run all the time. The out-of-hours excess, use while shut above the base load, is the part worth investigating.'),
   ('Why do opening hours matter so much?', 'They decide which half hours count as closed. If a building is genuinely used on Saturdays and the calendar says it is shut, Saturday use shows as out-of-hours. Confirm the hours before acting on the figures.'),
   ('How quickly can I see whether a change worked?', 'With half-hourly data, within weeks. Compare the same days before and after the change; the analyser has a before-and-after view for this.')],
  [('base-load.html', 'Base load', 'The other half of the picture: what never switches off.'),
   ('example-office-analysis.html', 'Worked example', 'Out-of-hours use in one office, with figures.'),
   ('sectors.html', 'By sector', 'What normal looks like in schools, offices, leisure and more.')],
  'What out-of-hours electricity use is, how to find it in half-hourly data (opening hours, heatmap, day types, edges of the day), common causes, and fixes.'))

# ── BASE LOAD ───────────────────────────────────────────────────────────
PAGES.append(guide_page(
  'base-load.html',
  'Base load electricity: what it is and how to cut it',
  'Base load: what never switches off',
  'Every building has a level of demand it never drops below. Because it runs every hour of the year, small reductions add up.',
  'What base load electricity is, how to measure it from half-hourly data, what makes it up, and how to reduce it. Each kilowatt running all year is 8,760 kWh.',
  '''
<p class="answer">Base load is the electricity demand a building never drops below, overnight and at weekends as well as during the day. Each kilowatt of it runs for 8,760 hours a year: 8,760 kWh, about £2,190 at 25p/kWh. Measure it from half-hourly data, find out what makes it up, and switch off what doesn't need to run.</p>

<h2 id="measure">How to measure it</h2>
<p>Take every valid half-hourly reading, convert to kW (kWh divided by half an hour), and find the level demand is above 95% of the time: the 5th percentile. That's the analyser's base load reference.</p>
<p>Why not the lowest reading? One meter dropout or a power cut would set it, and the true floor would look lower than it is. The analyser shows the lowest half hour alongside, so you can see the difference.</p>

<h2 id="what">What makes it up</h2>
<ul><li>IT: servers, network switches, phone systems</li><li>Refrigeration: kitchen fridges, freezers, vending machines, water coolers</li><li>Pumps and fans that run continuously</li><li>Hot water heaters and boilers kept on standby</li><li>Security, fire systems and emergency lighting</li><li>Equipment on standby, and plant left running by mistake</li></ul>

<h2 id="reduce">How to reduce it</h2>
<ol><li><strong>Walk the building at night or at a weekend</strong> and note everything that's on.</li><li><strong>Sort it</strong>: must run, could run less, shouldn't be on.</li><li><strong>Fix the easy ones</strong>: timers on water heaters and vending machines, switch-off routines, consolidating servers.</li><li><strong>Watch the base load month by month.</strong> A step up usually means something new was installed or left on; the analyser flags lasting changes like this.</li></ol>

<h2 id="worth">Is it worth it?</h2>
<p>At 25p/kWh, every 1 kW cut from the base load is worth about £2,190 a year. A 0.5 kW cut from a heater left on, at the same rate, is about £1,100. The arithmetic is simple because base load runs every hour of the year.</p>
''',
  [('measure', 'How to measure it'), ('what', 'What makes it up'), ('reduce', 'How to reduce it'), ('worth', 'Is it worth it?')],
  [('What is a typical base load?', 'It depends on the building: a data-heavy office or a site with refrigeration will have a much higher floor than a school. Compare a site against itself over time, and against similar buildings in your estate.'),
   ('Why is my base load higher at weekends than overnight on weekdays?', 'It shouldn\'t be. If it is, something is switching on at weekends (heating frost protection, a scheduled process or a booking). Check the heatmap for the weekend pattern.'),
   ('How much does 1 kW of base load cost?', 'It runs 8,760 hours a year, so 8,760 kWh. At 25p/kWh that is about £2,190 a year; multiply by your own rate.')],
  [('out-of-hours-electricity.html', 'Out-of-hours use', 'Use above the base load while the building is shut.'),
   ('supply-capacity.html', 'Supply capacity', 'The other end of the scale: your peaks.'),
   ('example-office-analysis.html', 'Worked example', 'Base load in one office, with figures.')],
  'What base load is, how to measure it from half-hourly data (5th percentile, not the minimum), what makes it up, how to reduce it; 1 kW all year is 8,760 kWh.'))

# ── SUPPLY CAPACITY ─────────────────────────────────────────────────────
PAGES.append(guide_page(
  'supply-capacity.html',
  'Supply capacity and kVA: room for heat pumps and EVs',
  'Supply capacity and kVA',
  'Before adding heat pumps, EV chargers or new plant, check how close your highest half hours already come to your agreed supply capacity.',
  'Agreed supply capacity explained: kW to kVA, comparing half-hourly peaks with capacity, and headroom for heat pumps and EV charging.',
  '''
<p class="answer">Your agreed supply capacity is the maximum demand, in kVA, your connection is set up for. Convert your half-hourly peaks from kW to kVA (divide by the power factor), compare them with the agreed capacity, and the gap is your headroom for new load such as heat pumps and EV chargers.</p>

<h2 id="what">What agreed supply capacity is</h2>
<p>Larger supplies have an agreed capacity, sometimes called authorised or available capacity, set in the connection agreement and usually shown on the bill in kVA. You typically pay a charge for it every day whether you use it or not. Going over it can bring extra charges, and the network operator may ask you to increase it.</p>

<h2 id="kva">kW and kVA</h2>
<p>Meters measure energy (kWh); half-hourly data gives average power in each half hour (kW). Capacity is set in kVA, which also counts reactive power. The link is the power factor:</p>
<div class="note"><strong>kVA = kW ÷ power factor.</strong> At a power factor of 0.95, a 95 kW peak is 100 kVA. If your bill shows reactive power charges, your power factor is probably lower than 0.95.</div>

<h2 id="headroom">Working out headroom</h2>
<ol><li><strong>Find your highest half hours</strong> over at least a year, so winter peaks are included.</li><li><strong>Convert them to kVA</strong> with your power factor.</li><li><strong>Keep a safety margin</strong>, for example 10%, below the agreed capacity.</li><li><strong>The headroom</strong> is the largest constant load you could add without going over the margin in any half hour.</li></ol>
<p>Half-hourly averages smooth out very short spikes, so this is a screen, not confirmation from your network operator.</p>

<h2 id="new-load">Heat pumps and EV charging</h2>
<p>A heat pump's electrical input is much lower than its heat output: at a coefficient of performance of 3, a 150 kW heat output draws about 50 kW. It runs hardest in winter, when building peaks are usually highest. EV charging overnight lands where the site is quietest. The analyser lets you test a new load at a chosen time of day and season against your actual half-hourly peaks.</p>
''',
  [('what', 'What agreed supply capacity is'), ('kva', 'kW and kVA'), ('headroom', 'Working out headroom'), ('new-load', 'Heat pumps and EV charging')],
  [('Where do I find my agreed supply capacity?', 'On your electricity bill or connection agreement, in kVA. Your supplier can confirm it.'),
   ('What power factor should I use?', 'If you do not know it, 0.95 is a reasonable starting assumption. A lower value is likely if your bill shows reactive power charges.'),
   ('Is half-hourly data enough to plan a new connection?', 'It is a good first screen, but half-hour averages hide very short peaks. For a significant new load, talk to your network operator before committing.')],
  [('base-load.html', 'Base load', 'The demand that never goes away.'),
   ('example-office-analysis.html', 'Worked example', 'Peaks against capacity in one office.'),
   ('how-it-works.html', 'How the analyser works', 'Including how headroom is worked out.')],
  'Agreed supply capacity in kVA, kW to kVA via power factor, headroom from half-hourly peaks with a safety margin, and screening heat pumps and EV charging.'))

# ── WORKED EXAMPLE: SCHOOL ──────────────────────────────────────────────
PAGES.append(guide_page(
  'example-school-analysis.html',
  'Worked example: a primary school\'s half-hourly data',
  'Worked example: one primary school',
  'A year of half-hourly data from a primary school, set up with its term dates and run through the analyser. The school is made up; every figure is what the analyser reports.',
  'A primary school\'s year of half-hourly data: heating left on through half term, evening lettings, and what the analyser found once term dates were entered.',
  '''
<p class="answer">Once its term dates were entered, this school used 31% of its electricity while shut: about £1,260 a year above what never switches off, at 25p/kWh. The biggest single problem was October half term, when demand was more than double what it should have been for an empty building.</p>

<div class="note"><strong>Made-up data.</strong> <a href="samples/example-school.csv" download>Download the file</a> and load it into the <a href="analyser/">analyser</a> to follow along. Set the building type to School and add the term dates below as closures.</div>

<h2 id="setup">Setting it up</h2>
<p>School holidays are never assumed: the analyser asks you to enter them. For this school:</p>
<ul><li>Building type: School (open 07:00 to 17:30 on weekdays)</li><li>Six closures: Easter, May half term, summer, October half term, Christmas and February half term</li><li>Hours ticked as confirmed</li></ul>
<p>Without the term dates, holiday weeks would count as normal school days, and a heating fault in a holiday would hide as normal use.</p>

<h2 id="headline">The headline figures</h2>
<div class="table-wrap"><table><thead><tr><th>Measure</th><th class="num">Value</th></tr></thead><tbody>
<tr><td>Electricity a year</td><td class="num">57,753 kWh</td></tr><tr><td>Energy cost a year (25p/kWh)</td><td class="num">£14,438</td></tr>
<tr><td>Base load</td><td class="num">1.9 kW</td></tr><tr><td>Highest half hour</td><td class="num">30.1 kW</td></tr>
<tr><td>Use while shut</td><td class="num">31%</td></tr><tr><td>Out-of-hours excess</td><td class="num">£1,261 a year</td></tr></tbody></table></div>

<h2 id="heatmap">The year at a glance</h2>
<figure class="figure"><img src="images/heatmap-school.png" width="2464" height="896" alt="Heatmap of a school year: dark blocks in term time, blank holidays, a pale block across October half term and thin stripes on Tuesday and Thursday evenings" loading="lazy"><figcaption>One column per day, one row per half hour. Term weeks are dark; holidays should be blank. October half term isn't.</figcaption></figure>
<p>Two things stand out: a pale block across the whole of October half term, and thin stripes after 18:00 on two evenings a week in term. <a href="reading-a-heatmap.html">How to read a heatmap</a>.</p>

<h2 id="findings">What the analyser found</h2>
<h3>1. Heating plant on through October half term</h3>
<p>The three largest out-of-hours days of the year were all in half term, about 100 kWh each above base load. The analyser flagged a lasting change: demand from 25 October was at least 15% above its expected level on five of nine days, on average more than double. The pattern (07:00 to 17:00 on weekdays, nobody in) points to plant running to its term-time schedule.</p>
<h3>2. Evening lettings</h3>
<p>Weekday evenings account for the largest share of the out-of-hours excess: 2,765 kWh above base load. The stripes on Tuesday and Thursday evenings are a regular hall letting. Lettings are fine, but they should be in the calendar as open hours, and it's worth checking whether a hall booking is lighting and heating more of the building than it needs.</p>
<h3>3. Holidays and weekends</h3>
<p>The holidays themselves added 1,157 kWh above base load, most of it in October. Saturdays and Sundays were close to base load (556 kWh and 526 kWh above it across the year), which is what you'd hope for.</p>

<h2 id="next-steps">What we'd do next</h2>
<ol><li><strong>Add the holiday calendar to the building management system</strong>, so heating and ventilation switch off for half terms as well as the long holidays.</li><li><strong>Add the lettings to the analyser's calendar</strong>, then look at what the hall booking switches on.</li><li><strong>Check the next half term</strong> with the analyser's before-and-after comparison to see whether the fix worked.</li></ol>
''',
  [('setup', 'Setting it up'), ('headline', 'The headline figures'), ('heatmap', 'The year at a glance'), ('findings', 'What the analyser found'), ('next-steps', "What we'd do next")],
  [('Do I have to enter term dates?', 'Yes. The analyser never assumes them, because they vary by school and by year. Paste them in as closures; without them, holiday weeks count as normal school days.'),
   ('Should a school use nothing in the holidays?', 'No. The base load continues (IT, fridges, security). Holiday use above the base load is what to look at.'),
   ('Is this real data?', 'No. The school and its readings are made up, so the method can be shown without anyone\'s real data.')],
  [('reading-a-heatmap.html', 'Reading a heatmap', 'How to spot patterns like half term at a glance.'),
   ('schools-electricity.html', 'Schools and colleges', 'What to check first in education buildings.'),
   ('proving-savings.html', 'Proving a saving', 'Checking whether the half-term fix worked.')],
  'A primary school with term dates entered: 31% of use while shut, £1,261 a year above base load; heating plant on through October half term (demand more than double); evening lettings.',
  crumbs=[HOME, GUIDES, ('Worked example: school', 'example-school-analysis.html')]))

# ── READING A HEATMAP ───────────────────────────────────────────────────
PAGES.append(guide_page(
  'reading-a-heatmap.html',
  'How to read a half-hourly electricity heatmap',
  'How to read a half-hourly heatmap',
  'A heatmap shows every half hour of a year in one picture. Once you know what to look for, the problems jump out.',
  'How to read a half-hourly electricity heatmap: what the axes and colours mean, what normal looks like, and the patterns that point to waste.',
  '''
<p class="answer">A half-hourly heatmap has one column per day and one row per half hour, with darker colour for higher demand. Normal use shows as a dark band during opening hours; anything dark outside that band, such as nights, weekends and holidays, is use worth checking.</p>

<h2 id="axes">What you're looking at</h2>
<ul><li><strong>Across:</strong> days, from the start of the period to the end.</li><li><strong>Down:</strong> time of day, from midnight at the top to midnight at the bottom.</li><li><strong>Colour:</strong> demand in that half hour, from pale (low) to dark (high).</li></ul>
<p>A year is about 17,500 half hours. A table of that many numbers is unreadable; the heatmap shows all of them at once.</p>

<figure class="figure"><img src="images/heatmap-office.png" width="2464" height="896" alt="Heatmap of an office year: a dark weekday band, pale nights, and weekends that are sometimes busy" loading="lazy"><figcaption>An office (made-up data). The weekday band is clear, and some Saturdays are as busy as weekdays.</figcaption></figure>

<h2 id="normal">What normal looks like</h2>
<p>For a building used on weekdays: a dark horizontal band during working hours, regular pale gaps for weekends, and pale nights. Winter is often a little darker than summer. The edges of the band show when the building really starts and stops.</p>

<h2 id="patterns">Patterns worth checking</h2>
<div class="table-wrap"><table><thead><tr><th>What you see</th><th>What it usually means</th></tr></thead><tbody>
<tr><td>A pale block where it should be blank (a holiday week)</td><td>Plant running to its normal schedule with nobody in</td></tr>
<tr><td>Thin stripes in the evening on the same weekdays</td><td>Regular evening use, such as lettings, classes or cleaning</td></tr>
<tr><td>Dark band starting well before opening</td><td>Heating or ventilation start times set too early</td></tr>
<tr><td>Nights that get darker from a certain date</td><td>New equipment, or something left on: base load has risen</td></tr>
<tr><td>A single dark column</td><td>One unusual day: an event, a fault, or a reading error</td></tr>
<tr><td>Grey or striped gaps</td><td>Missing data, not zero use</td></tr></tbody></table></div>

<figure class="figure"><img src="images/heatmap-school.png" width="2464" height="896" alt="Heatmap of a school year showing term blocks, holidays, a pale half-term block and evening stripes" loading="lazy"><figcaption>A primary school (made-up data). The pale block in late October is heating left on through half term; the stripes after 18:00 are evening lettings. See the <a href="example-school-analysis.html">worked example</a>.</figcaption></figure>

<h2 id="next">From picture to figure</h2>
<p>The heatmap shows where to look; the figures say how much it matters. In the analyser, click any day to see its half hours against a typical day, then use the out-of-hours and unusual-day findings to put a cost on what you've spotted.</p>
''',
  [('axes', "What you're looking at"), ('normal', 'What normal looks like'), ('patterns', 'Patterns worth checking'), ('next', 'From picture to figure')],
  [('What is a carpet plot?', 'Another name for the same chart: one column per day, one row per half hour, coloured by demand.'),
   ('Why are some days grey?', 'No valid readings. Missing data is shown as missing, not as zero, so gaps don\'t look like the building was switched off.'),
   ('Can I see one day in detail?', 'Yes. In the analyser, click any day on the heatmap to see its half hours against a typical day of the same kind.')],
  [('example-school-analysis.html', 'Worked example: school', 'The school heatmap, explained finding by finding.'),
   ('out-of-hours-electricity.html', 'Out-of-hours use', 'Putting a cost on what the heatmap shows.'),
   ('glossary.html', 'Glossary', 'The terms used in these guides.')],
  'How to read a half-hourly heatmap (days across, time of day down, colour for demand) and the patterns that point to waste.'))

# ── PROVING A SAVING ────────────────────────────────────────────────────
PAGES.append(guide_page(
  'proving-savings.html',
  'How to prove an energy saving worked, with half-hourly data',
  'Proving a saving worked',
  'You changed a setting or replaced some equipment. Half-hourly data can show whether it made a difference, if you compare like with like.',
  'How to use half-hourly data to show whether a change saved energy: matched before-and-after periods, the right measure, and what can mislead.',
  '''
<p class="answer">Compare matched periods before and after the change: the same days of the week, the same kind of day (open, closed, holiday), and enough weeks to smooth out noise. Look at the part of demand the change should affect, such as base load or out-of-hours use, rather than the total bill.</p>

<h2 id="match">Compare like with like</h2>
<ul><li><strong>Same kind of day.</strong> Compare weekdays with weekdays and holidays with holidays. A before period full of bank holidays will flatter the after period, or the reverse.</li><li><strong>Long enough.</strong> Four to eight weeks either side is usually enough to see a real change in half-hourly data. A single week can be swayed by one unusual day.</li><li><strong>Close in time.</strong> The nearer the two periods, the less the weather and the seasons get in the way.</li><li><strong>Leave out the change itself.</strong> Skip the days when the work was being done.</li></ul>

<h2 id="measure">Measure the right thing</h2>
<p>Pick the measure the change should move:</p>
<div class="table-wrap"><table><thead><tr><th>Change</th><th>Look at</th></tr></thead><tbody>
<tr><td>Heating or ventilation schedules</td><td>Out-of-hours use, and demand around opening and closing</td></tr>
<tr><td>Switching off equipment overnight</td><td>Base load</td></tr>
<tr><td>LED lighting</td><td>Open-hours demand</td></tr>
<tr><td>Holiday settings in the building controls</td><td>Use during closures</td></tr></tbody></table></div>
<p>Total consumption mixes the change with everything else that happened, such as occupancy, weather and new equipment, so a real saving can disappear in it.</p>

<h2 id="weather">Weather and seasons</h2>
<p>Electric heating and cooling follow the weather. If the before period was colder than the after period, some of the drop is weather, not the change. For heating-related changes, compare the same weeks a year apart as a cross-check, or normalise with degree days if you have them.</p>

<h2 id="analyser">In the analyser</h2>
<ul><li><strong>Did a change make a difference?</strong> on the Base load tab compares matched weeks either side of a date you choose.</li><li><strong>Compare periods</strong> on the Heatmap tab compares any two periods side by side.</li><li><strong>Persistent changes</strong> on the Unusual days tab flags lasting shifts on its own, so you can check whether a change shows up when you'd expect.</li></ul>
<p>For formal measurement and verification of savings, the International Performance Measurement and Verification Protocol (IPMVP) sets out recognised methods.</p>
''',
  [('match', 'Compare like with like'), ('measure', 'Measure the right thing'), ('weather', 'Weather and seasons'), ('analyser', 'In the analyser')],
  [('How long should I wait before checking?', 'Four to eight weeks of data after the change, compared with the same length of time before it, is usually enough to see a real change.'),
   ('Why has our bill not gone down?', 'A saving in one place can be hidden by changes elsewhere: occupancy, weather, prices or new equipment. Compare the specific measure the change should affect.'),
   ('Can this replace a formal M&amp;V report?', 'It is a good check, but formal measurement and verification (for example under IPMVP) sets a baseline, adjustments and reporting up front.')],
  [('base-load.html', 'Base load', 'The measure most switch-off changes move.'),
   ('out-of-hours-electricity.html', 'Out-of-hours use', 'The measure schedule changes move.'),
   ('example-school-analysis.html', 'Worked example: school', 'A half-term fix worth checking.')],
  'Proving a saving with half-hourly data: matched before-and-after periods, the right measure for the change, weather effects, and the analyser tools.'))

# ── MHHS ────────────────────────────────────────────────────────────────
PAGES.append(guide_page(
  'half-hourly-settlement.html',
  'Market-wide half-hourly settlement (MHHS) explained',
  'Market-wide half-hourly settlement explained',
  'Britain is moving every electricity meter onto half-hourly settlement. Here is what that means for businesses and public bodies, and why it makes half-hourly data more useful.',
  'What market-wide half-hourly settlement (MHHS) is, the timetable to 2027, who runs it, and what it means for business and public sector electricity customers.',
  '''
<p class="answer">Market-wide half-hourly settlement (MHHS) means suppliers will be charged for the electricity their customers use in each half hour, rather than from estimated profiles. Migration began in October 2025 and is due to be complete in May 2027. For organisations with smart or advanced meters, it means half-hourly readings are part of how electricity is settled, so it's worth asking your supplier for them.</p>

<h2 id="what">What it is</h2>
<p>Large sites have been settled half-hourly for years. Smaller sites have mostly been settled using standard profiles: estimates of when a typical customer uses electricity. MHHS replaces those estimates with actual half-hourly readings wherever a meter can provide them.<sup><a href="#sources">1</a></sup></p>
<p>The programme's stated objective is "to maximise the opportunities provided by smart metering by developing and implementing an enduring process for MHHS, that delivers benefits for consumers and enables a smart, flexible energy system."<sup><a href="#sources">2</a></sup></p>

<h2 id="who">Who runs it</h2>
<p>Ofgem decided to proceed with MHHS on 20 April 2021.<sup><a href="#sources">1</a></sup> Ofgem is the programme sponsor and appointed Elexon as Senior Responsible Owner and Implementation Manager; delivery is led by the industry.<sup><a href="#sources">2</a></sup></p>

<h2 id="timeline">The timetable</h2>
<div class="table-wrap"><table><thead><tr><th>Date</th><th>Milestone</th></tr></thead><tbody>
<tr><td>20 April 2021</td><td>Ofgem decision to introduce MHHS (originally planned to complete in October 2025)</td></tr>
<tr><td>21 October 2025</td><td>Migration to the new arrangements began, for all meter types</td></tr>
<tr><td>7 May 2027</td><td>Migration due to be complete, with all energy settled under the new arrangements</td></tr>
<tr><td>2 July 2027</td><td>Settlement moves from a 14-month to a four-month timetable</td></tr></tbody></table></div>
<p>Dates as published by Ofgem and the MHHS programme in November 2026; check the programme's milestone page for the latest.<sup><a href="#sources">1, 3</a></sup></p>

<h2 id="you">What it means for your organisation</h2>
<ul><li><strong>You don't have to do anything to be migrated:</strong> your supplier handles it.</li><li><strong>Microbusinesses can't opt out.</strong> Ofgem's decision says half-hourly data will be processed for settlement for domestic customers unless they opt out, and that microbusiness customers will not be able to opt out.<sup><a href="#sources">1</a></sup></li><li><strong>Tariffs may change.</strong> Ofgem expects MHHS to encourage suppliers to offer tariffs that reward using electricity at cheaper times, such as time-of-use tariffs.<sup><a href="#sources">1</a></sup></li><li><strong>Half-hourly data becomes the norm.</strong> If your meter records half-hourly readings, your supplier uses them; ask for them, and you can see exactly when your sites use electricity.</li></ul>
<p>When electricity is used will matter more under half-hourly settlement and time-of-use tariffs. Knowing your half-hourly pattern now, including what runs overnight and at weekends, puts you in a better position to choose a tariff and cut costs.</p>
''' + sources([
    ('Ofgem: Electricity Retail Market-wide Half-hourly Settlement: Decision and Full Business Case (20 April 2021)', 'https://www.ofgem.gov.uk/decision/electricity-retail-market-wide-half-hourly-settlement-decision-and-full-business-case'),
    ('MHHS Programme: Programme overview', 'https://www.mhhsprogramme.co.uk/programme-information/programme-overview'),
    ('MHHS Programme: Key programme milestones', 'https://www.mhhsprogramme.co.uk/programme-information/key-programme-milestones')]),
  [('what', 'What it is'), ('who', 'Who runs it'), ('timeline', 'The timetable'), ('you', 'What it means for your organisation')],
  [('When does market-wide half-hourly settlement finish?', 'Migration is due to be complete on 7 May 2027, with the move to a four-month settlement timetable on 2 July 2027, according to the MHHS programme\'s published milestones.'),
   ('Do I need to do anything?', 'No. Your supplier migrates your meters. It is worth asking them for your half-hourly data, so you can see when your sites use electricity.'),
   ('Can a business opt out of half-hourly data collection?', 'Ofgem\'s 2021 decision says microbusiness customers will not be able to opt out of their half-hourly data being processed for settlement. Domestic customers can opt out.')],
  [('get-your-data.html', 'Getting your data', 'What to ask your supplier for.'),
   ('glossary.html', 'Glossary', 'Settlement, MPAN, kVA and other terms.'),
   ('out-of-hours-electricity.html', 'Out-of-hours use', 'The first thing to look at in your data.')],
  'Market-wide half-hourly settlement: Ofgem decision 20 April 2021; migration began 21 October 2025, due complete 7 May 2027; four-month settlement timetable from 2 July 2027; microbusinesses cannot opt out.'))

# ── GLOSSARY ────────────────────────────────────────────────────────────
GLOSSARY = [
  ('Agreed supply capacity', 'The maximum demand, in kVA, a connection is set up for, shown on larger electricity bills. Also called authorised or available capacity. <a href="supply-capacity.html">More</a>.'),
  ('Annualised figure', 'A yearly figure scaled up from the valid readings available, used when the data covers less than a full year or has gaps.'),
  ('Base load', 'The level of demand a building rarely drops below, measured as the 5th percentile of half-hourly demand. It is what never switches off. <a href="base-load.html">More</a>.'),
  ('Closed-hours excess', 'Electricity used while a building should be shut, above its base load. The analyser ranks sites by it. <a href="out-of-hours-electricity.html">More</a>.'),
  ('Coverage', 'The share of expected half-hourly readings that are present and valid.'),
  ('Degree days', 'A measure of how cold (heating degree days) or warm (cooling degree days) a period was, used to compare energy use across different weather.'),
  ('DNO', 'Distribution network operator: the company that runs the local electricity network and the connection to your site.'),
  ('Half-hourly (HH) data', 'Electricity consumption recorded for every half hour: 48 readings a day.'),
  ('Heatmap', 'A chart of every half hour in a period: one column per day, one row per half hour, coloured by demand. Also called a carpet plot. <a href="reading-a-heatmap.html">More</a>.'),
  ('kVA', 'Kilovolt-ampere: apparent power, the unit supply capacity is set in. kVA = kW ÷ power factor.'),
  ('kW', 'Kilowatt: power, the rate of use at a moment. A half-hourly reading in kWh divided by 0.5 hours gives the average kW for that half hour.'),
  ('kWh', 'Kilowatt-hour: energy, what you are billed for. 1 kW for one hour is 1 kWh.'),
  ('Load factor', 'Average demand divided by peak demand. A low load factor means short, high peaks.'),
  ('Market-wide half-hourly settlement (MHHS)', 'The move to settle every electricity meter in Great Britain using half-hourly data. <a href="half-hourly-settlement.html">More</a>.'),
  ('MPAN', 'Meter point administration number: the 13-digit supply number on an electricity bill that identifies a meter point.'),
  ('Peak demand', 'The highest half-hourly average demand in a period, usually in kW or kVA.'),
  ('Power factor', 'The ratio of real power (kW) to apparent power (kVA), between 0 and 1. Equipment such as motors lowers it.'),
  ('Settlement', 'The process that works out how much electricity each supplier\'s customers used, and when, so suppliers pay the right amount for it.'),
  ('Time-of-use tariff', 'A tariff with different unit rates at different times of day, such as day and night rates.'),
]
NAV_PARENT['glossary.html'] = 'guides.html'
PAGES.append(Page(
  'glossary.html', 'Glossary of half-hourly electricity terms',
  'Plain-English definitions of half-hourly electricity terms: base load, kW, kWh, kVA, power factor, MPAN, agreed supply capacity, settlement and more.',
  page_hero('Guide', 'Glossary', 'Plain-English definitions of the terms used in half-hourly electricity data and on this site.',
            crumbs=[HOME, GUIDES, ('Glossary', 'glossary.html')])
  + guide(updated_line() + '<dl class="glossary">' + ''.join(
      f'<div id="{t.lower().split(" (")[0].replace(" ", "-")}"><dt>{t}</dt><dd>{d}</dd></div>' for t, d in GLOSSARY) + '</dl>')
  + cta('See the terms in your own data', 'Free, no sign-up, and nothing is uploaded.'),
  crumbs=[HOME, GUIDES, ('Glossary', 'glossary.html')], article=True, section='Guides',
  summary='Definitions: base load, closed-hours excess, kW, kWh, kVA, power factor, MPAN, agreed supply capacity, settlement, MHHS, heatmap, load factor and more.',
  schema=[{'@type': 'DefinedTermSet', 'name': 'Half-hourly electricity glossary', 'hasDefinedTerm': [
      {'@type': 'DefinedTerm', 'name': t, 'description': strip_tags(d).replace(' More.', '')} for t, d in GLOSSARY]}]))

# ── SECTORS ─────────────────────────────────────────────────────────────
SECTOR_DATA = [
  ('schools-electricity.html', 'Schools and colleges', 'Electricity use in schools and colleges',
   'Schools are closed for around 13 weeks a year, so holidays and weekends should look almost flat. When they don\'t, there\'s usually a schedule to fix.',
   'Holiday weeks, weekends and evenings should be close to the base load. The big difference between a school and an office is the length of the holidays, so set term dates in the calendar first.',
   ['Heating and ventilation running through holidays, especially half terms', 'IT suites, servers and interactive screens left on overnight', 'Kitchen equipment and water heaters on through the holidays', 'Evening lettings that run the whole building for one hall or pitch', 'Pool or sports hall plant on the same schedule as the main building'],
   'Add each term\'s dates as closures, and any regular evening lettings as open hours, so out-of-hours figures reflect what the school really controls.',
   [('Should holiday use be zero?', 'No. Base load continues (IT, fridges, security). Holiday use above the base load is what to look at.'),
    ('How do I handle evening lettings?', 'Add them to the calendar as open hours, so they are not counted as out-of-hours use, then check whether the letting needs the whole building heated and lit.')]),
  ('offices-council-buildings.html', 'Offices and council buildings', 'Electricity use in offices and council buildings',
   'Office demand should fall sharply when people go home. The interesting part is everything that doesn\'t.',
   'A clear weekday shape, with demand dropping to the base load in the evening and at weekends. Hybrid working has made many offices quieter on Mondays and Fridays, but plant often still runs as if every desk were full.',
   ['Air handling and cooling running all night or all weekend', 'Early starts well before staff arrive (optimum start set too early)', 'Whole floors lit for a cleaner or one late worker', 'Server rooms and comms cupboards with their own cooling', 'Council buildings used for evening meetings or elections, which need their own calendar entries'],
   'Set hours by day of the week if Monday and Friday occupancy is low, and add bank holidays, which many building schedules miss.',
   [('Why does our office use so much at weekends?', 'Usually heating, ventilation or cooling on the wrong schedule, or a weekend activity using the whole building. The day-type breakdown shows which.'),
    ('Has hybrid working changed what to look for?', 'Yes. Compare quiet weekdays with busy ones: if demand barely changes, plant is running to a full-occupancy schedule.')]),
  ('leisure-centres.html', 'Leisure centres and pools', 'Electricity use in leisure centres and pools',
   'Long opening hours and pools that run around the clock make leisure centres high users. The question is what the overnight floor is made of.',
   'High base load from pool plant, ventilation and dehumidification, with opening hours from early morning to late evening, seven days a week.',
   ['Pool hall ventilation and dehumidification at daytime rates overnight', 'Filtration pumps that could run slower outside opening hours', 'Sports hall and studio lighting left on between bookings', 'Saunas, steam rooms and hot water heaters on before they are needed', 'Plant that kept running through a closure for maintenance'],
   'Opening hours vary by day and change in holidays; enter them carefully, because a centre open 14 hours a day leaves a short closed window where small settings make a big difference.',
   [('Is a high base load normal for a pool?', 'Yes: pool plant has to run continuously. The question is whether it runs harder than needed outside opening hours, for example ventilation at full speed overnight.'),
    ('What should I look at first?', 'The overnight floor and how fast demand falls after closing. Pool covers and slower overnight ventilation and filtration settings are common starting points.')]),
  ('healthcare-electricity.html', 'Healthcare', 'Electricity use in healthcare buildings',
   'Hospitals and many care settings run 24/7, so out-of-hours use isn\'t the right question. Day against night, and peaks against capacity, are.',
   'Continuous operation with a daytime rise. Clinics, surgeries and administrative buildings on the same estate keep office-style hours and should be treated like offices.',
   ['Night demand that is close to daytime demand in non-clinical areas', 'Weekend use in outpatient and administrative buildings', 'Peaks close to supply capacity before electric heating or EV charging is added', 'Steps in base load after new equipment or a refurbishment', 'Sub-meters for different buildings or wings, where available'],
   'Set 24/7 buildings as always open, so the analysis focuses on base load, peaks and changes over time, and give clinics and offices their real hours.',
   [('Can out-of-hours analysis work for a hospital?', 'For the main 24/7 building, compare day against night and track base load instead. For clinics and offices on the estate, out-of-hours analysis works as for any office.'),
    ('Why does supply capacity matter so much in healthcare?', 'Replacing gas heating with heat pumps adds a large winter load. Check how close current winter peaks already come to the agreed capacity first.')]),
  ('industrial-warehouses.html', 'Industrial and warehouses', 'Electricity use in industrial sites and warehouses',
   'Shift patterns make the calendar the most important setting. Get it right and shutdowns, compressed air and refrigeration show up clearly.',
   'Demand follows shifts: a clear step up when a shift starts and down when it ends. Planned shutdowns should drop close to the base load.',
   ['Compressed air left on overnight and at weekends; leaks show as a steady load when production stops', 'Refrigeration and chillers running harder than needed', 'Shutdown weeks that never get close to the base load', 'Lighting in high-bay warehouses outside shift times', 'Peaks against capacity before adding EV charging for vans or forklifts'],
   'Enter shift times, including overnight shifts, and planned shutdowns, so the analysis separates production from everything else.',
   [('How do I spot compressed air leaks?', 'Look at demand when production has stopped. If the compressors keep cycling with nothing using air, the steady load is often leaks.'),
    ('Can the analyser handle night shifts?', 'Yes. Opening hours can run past midnight, and each day of the week can have its own hours.')]),
  ('retail-hospitality.html', 'Retail and hospitality', 'Electricity use in retail and hospitality',
   'Fixed trading hours make out-of-hours use easy to see. Refrigeration, signage and kitchen equipment are the usual suspects.',
   'Demand follows trading hours, with preparation before opening and cleaning after closing. Refrigeration sets a high base load in food retail and hospitality.',
   ['Refrigeration and display cases without night blinds or covers', 'Signage and display lighting on timers that run all night', 'Kitchen extraction and equipment switched on long before service', 'Heating and cooling running to an old schedule after trading hours changed', 'Seasonal hours that never made it into the building controls'],
   'Include preparation and cleaning time in the opening hours, so the out-of-hours figure shows what is genuinely avoidable.',
   [('Why is our base load so high?', 'In food retail and hospitality it is mostly refrigeration. Night blinds, door seals and set points are worth checking before anything else.'),
    ('How do I compare several shops or venues?', 'Load one file per meter. The analyser ranks sites by out-of-hours excess and has an estate comparison by building type.')]),
]

for file, short, h1, lead, normal, checks, calendar_tip, faqs in SECTOR_DATA:
    PAGES.append(guide_page(
      file, f'{short}: what half-hourly data shows', h1, lead,
      f'Half-hourly electricity data in {short.lower()}: what normal looks like, what to check first and how to set opening hours.',
      f'''
<p class="answer">{normal}</p>

<h2 id="check">What to check first</h2>
<ul>{''.join(f'<li>{c}</li>' for c in checks)}</ul>

<h2 id="calendar">Setting the opening hours</h2>
<p>{calendar_tip}</p>
<p>These are starting points, not rules. Every site is compared with its own calendar, so the hours matter more than the sector.</p>
''',
      [('check', 'What to check first'), ('calendar', 'Setting the opening hours')],
      faqs,
      [('out-of-hours-electricity.html', 'Out-of-hours use', 'How to find and cut use while shut.'),
       ('base-load.html', 'Base load', 'What never switches off.'),
       ('sectors.html', 'Other sectors', 'Schools, offices, leisure, healthcare, industrial and retail.')],
      f'{short}: what normal half-hourly demand looks like and what to check first.',
      crumbs=[HOME, SECTORS, (short, file)]))

PAGES.append(Page(
  'sectors.html', 'What to look for by sector | Half Hourly Insights',
  'What half-hourly electricity data shows in schools, offices and council buildings, leisure centres, healthcare, industrial sites and retail.',
  page_hero('Sectors', 'What to look for in your sector', 'Every building type has its own normal. Choose yours for the patterns worth checking first.',
            crumbs=[HOME, SECTORS]) +
  '<section class="section"><div class="section-inner"><div class="link-grid">' +
  ''.join(f'<a class="link-card" href="{f}"><h3>{s}</h3><p>{lead}</p><span class="more">Read more</span></a>'
          for f, s, _, lead, *_ in SECTOR_DATA) +
  '</div></div></section>' + cta('Check your own sites', 'Load several meters at once and the analyser ranks them, so you know where to start.'),
  crumbs=[HOME, SECTORS], section='Sectors', summary='Index of sector pages.'))

GUIDE_LIST = [
    ('get-your-data.html', 'Getting your half-hourly data', 'Who has it, what to ask for, a letter template, and the formats the analyser reads.'),
    ('example-office-analysis.html', 'Worked example: one office, one year', 'What the analyser found in a year of data from a small office.'),
    ('example-school-analysis.html', 'Worked example: a primary school', 'Heating left on through half term, evening lettings, and term dates.'),
    ('reading-a-heatmap.html', 'How to read a heatmap', 'Every half hour of a year in one picture, and the patterns to spot.'),
    ('out-of-hours-electricity.html', 'Out-of-hours electricity use', 'How to find use while the building is shut, and cut it.'),
    ('base-load.html', 'Base load', 'What never switches off, how to measure it and how to reduce it.'),
    ('supply-capacity.html', 'Supply capacity and kVA', 'Headroom for heat pumps, EV charging and new plant.'),
    ('proving-savings.html', 'Proving a saving worked', 'Before-and-after comparisons that stand up.'),
    ('half-hourly-settlement.html', 'Half-hourly settlement (MHHS) explained', 'What the move to half-hourly settlement means, and the timetable to 2027.'),
    ('glossary.html', 'Glossary', 'kW, kWh, kVA, base load, MPAN and other terms.'),
    ('how-it-works.html', 'How the analyser works', 'Every step, from reading the file to the report.'),
]
NAV_PARENT['get-your-data.html'] = 'guides.html'
PAGES.append(Page(
  'guides.html', 'Guides to half-hourly electricity data | Half Hourly Insights',
  'Plain-English guides to half-hourly electricity data: getting it, out-of-hours use, base load, supply capacity and a worked example.',
  page_hero('Guides', 'Guides to half-hourly data', 'Plain-English answers to the questions that come up when you first look at half-hourly electricity data.',
            crumbs=[HOME, GUIDES]) +
  '<section class="section"><div class="section-inner"><div class="link-grid">' +
  ''.join(f'<a class="link-card" href="{f}"><h3>{t}</h3><p>{d}</p><span class="more">Read the guide</span></a>' for f, t, d in GUIDE_LIST) +
  '</div><p class="note" style="margin-top:32px">Looking for your sector? See <a href="sectors.html" style="color:var(--blue);text-decoration:underline">what to look for by sector</a>.</p></div></section>'
  + cta('Ready to look at your own data?', 'Free, no sign-up, and nothing is uploaded.'),
  crumbs=[HOME, GUIDES], section='Guides', summary='Index of guides.'))
