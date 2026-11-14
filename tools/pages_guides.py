"""
Guides and sector pages. Each guide opens with a direct answer (what search
and AI answer engines quote), carries a few questions marked up as FAQPage,
and ends with links to related guides.

Written for a general business reader: plain words, terms explained on first
use, one idea per sentence. "Closed-hours excess" is the analyser's figure;
"out-of-hours use" is the general idea.

Figures in the worked examples come from the analyser run on
site/samples/example-office.csv and example-school.csv (made-up data).
Re-check them if those files or the engine change.
"""
from kit import (NAV_PARENT, SOLAR_URL, Page, cta, link_card, faq_section, guide, page_hero, photo, related, sources, strip_tags, toc,
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
            + cta('Try it on your own data', "It's free, there's no sign-up, and your file stays on your computer."))
    return Page(file, title, description, body, crumbs=crumbs, faqs=faqs, article=True, summary=summary,
                section='Guides' if crumbs[1] == GUIDES else 'Sectors')


PAGES = []

# ── WORKED EXAMPLE ──────────────────────────────────────────────────────
PAGES.append(guide_page(
  'example-office-analysis.html',
  'Worked example: a year of half-hourly data for one office',
  'Worked example: one office, one year',
  'A year of data from a small office, run through the analyser. The office is made up; every figure is what the analyser reports.',
  'One office, one year of half-hourly data: use while closed, base load, peaks against supply capacity, and what to do next.',
  f'''
<p class="answer">This office used a third of its electricity (33%) while closed. Above what always has to run, that costs about £2,800 a year at 25p/kWh, and almost half of it is on Saturdays.</p>

<div class="note"><strong>Made-up data.</strong> <a href="samples/example-office.csv" download>Download the file</a> and load it into the <a href="analyser/">analyser</a> to follow along.</div>

<h2 id="headline">The headline figures</h2>
<div class="table-wrap"><table><thead><tr><th>Measure</th><th class="num">Value</th><th>What it means</th></tr></thead><tbody>
<tr><td>Electricity a year</td><td class="num">79,191 kWh</td><td>From 363 days of readings (99.5% coverage)</td></tr>
<tr><td>Energy cost a year</td><td class="num">£19,798</td><td>At 25p/kWh, before standing charges</td></tr>
<tr><td>Base load</td><td class="num">2.6 kW</td><td>The level demand rarely drops below</td></tr>
<tr><td>Busiest half hour</td><td class="num">25.5 kW</td><td>28 January 2025, midday</td></tr>
<tr><td>Use while closed</td><td class="num">33%</td><td>Office hours, 07:00 to 19:00 weekdays</td></tr>
<tr><td>Closed-hours excess</td><td class="num">£2,776</td><td>Use while closed, above base load</td></tr>
</tbody></table></div>

<h2 id="split">Where the electricity goes</h2>
<p>The three parts add up to the total:</p>
<ul><li><strong>Base load, 29%</strong> (22,606 kWh): runs around the clock.</li><li><strong>Open, above base load, 57%</strong> (45,062 kWh): normal use.</li><li><strong>Closed-hours excess, 14%</strong> (11,035 kWh): use while closed, above base load.</li></ul>

<h2 id="findings">What the analyser found</h2>
<h3>1. Use while closed: £2,776 a year (high impact)</h3>
<div class="table-wrap"><table><thead><tr><th>When</th><th class="num">Above base load</th></tr></thead><tbody>
<tr><td>Saturdays</td><td class="num">5,155 kWh</td></tr><tr><td>Weekday evenings and nights</td><td class="num">3,750 kWh</td></tr>
<tr><td>Bank holidays</td><td class="num">1,408 kWh</td></tr><tr><td>Sundays</td><td class="num">722 kWh</td></tr></tbody></table></div>
<p>Saturdays account for almost half, but Sundays are quiet, so the building is being used on some Saturdays. If that's planned, add it to the calendar. If not, a Saturday booking may be running the whole building.</p>

<h3>2. Seven bank holidays look like working days (medium impact)</h3>
<p>On seven bank holidays, including Christmas Day, the office used at least 80% of a normal weekday's electricity. If it was closed, the heating schedules probably don't include bank holidays.</p>

<h3>3. Early starts and late finishes: £629 a year (low impact)</h3>
<p>About 1,250 kWh a year above base load in the two hours before opening, and the same after closing. Timers and heating start-up settings are the usual cause.</p>

<h2 id="capacity">Supply capacity</h2>
<p>With a 40 kVA supply and a power factor of 0.95, the busiest half hour reaches 27 kVA, 67% of capacity. Keeping a 10% margin leaves about 9 kW, enough for one 7 kW EV charger but not a heat pump for the building. See <a href="supply-capacity.html">supply capacity and kVA</a>.</p>

<h2 id="next-steps">What we'd do next</h2>
<ol><li><strong>Confirm the opening hours</strong>, including Saturdays.</li><li><strong>Check the heating schedules</strong> for bank holidays and start times.</li><li><strong>Walk round on a Saturday</strong> to see what's on.</li><li><strong>Look at the base load.</strong> 2.6 kW running all year is about 22,800 kWh, roughly £5,700 at 25p/kWh. See <a href="base-load.html">how to reduce it</a>.</li></ol>
<p>57% of its electricity is used in the working day, when solar panels generate. Our {SOLAR} estimates what a roof system would save.</p>
''',
  [('headline', 'The headline figures'), ('split', 'Where the electricity goes'), ('findings', 'What the analyser found'), ('capacity', 'Supply capacity'), ('next-steps', "What we'd do next")],
  [('Is this real data?', "No. It's made up so we can show the method without using anyone's real data."),
   ('How long does an analysis like this take?', 'Loading the data takes about a minute. Confirming the opening hours takes longer, and matters more.'),
   ('Are these figures savings?', "No. They're what each pattern costs now at 25p/kWh. Any saving depends on what you change.")],
  [('out-of-hours-electricity.html', 'Out-of-hours use', 'How to find and reduce use while the building is closed.'),
   ('base-load.html', 'Base load', 'What always runs, and why it adds up.'),
   ('get-your-data.html', 'Get your own data', 'What to ask your supplier for.')],
  'A small office run through the analyser: 33% of use while closed, £2,776 a year above base load, almost half on Saturdays; base load 2.6 kW; 67% of a 40 kVA supply.',
  crumbs=[HOME, GUIDES, ('Worked example', 'example-office-analysis.html')]))

# ── OUT-OF-HOURS ────────────────────────────────────────────────────────
PAGES.append(guide_page(
  'out-of-hours-electricity.html',
  'Out-of-hours electricity use: how to find and cut it',
  'Out-of-hours electricity use',
  "Electricity used while a building should be closed is often the cheapest kind to cut. Here's how to find it and what usually causes it.",
  'How to find out-of-hours electricity use in half-hourly data, what usually causes it, and how to reduce it by changing timers and controls.',
  '''
<p class="answer">Out-of-hours use is electricity used while a building should be closed. Compare each half hour with the opening hours and take away what always has to run (the base load). What's left is the closed-hours excess, and it can often be cut by changing a timer or control setting.</p>

<h2 id="what">What counts as out-of-hours</h2>
<p>Evenings, nights, weekends, bank holidays and closure periods all count. Some use is unavoidable: servers, fridges, security and emergency lighting make up the <a href="base-load.html">base load</a>. The part to focus on is the excess above it, which the analyser ranks sites by.</p>

<h2 id="find">How to find it</h2>
<ol><li><strong>Set the opening hours accurately</strong>, including bank holidays, closures and regular evening or weekend use.</li><li><strong>Look at the heatmap.</strong> Opening hours show as a dark band; anything dark outside it is out-of-hours use.</li><li><strong>Break it down by type of day.</strong> Weeknights, weekends and bank holidays usually have different causes.</li><li><strong>Check the start and end of the day.</strong> Use that starts early or finishes late points to timers or heating start-up settings.</li></ol>

<h2 id="causes">What usually causes it</h2>
<ul><li>Heating, ventilation and air conditioning on the wrong schedule, or not set up for bank holidays</li><li>Lights left on, or on out-of-date timers</li><li>A small booking that runs the whole building</li><li>Equipment left on manual override after maintenance</li><li>IT, catering and hot water equipment with no timer</li></ul>

<h2 id="cut">How to cut it</h2>
<p>Most fixes are changes to settings: building management schedules, timers, holiday calendars and switch-off routines. Start with the biggest block, often weekends or a regular evening, and use the analyser's before-and-after comparison a month later to check it worked.</p>
''',
  [('what', 'What counts as out-of-hours'), ('find', 'How to find it'), ('causes', 'What usually causes it'), ('cut', 'How to cut it')],
  [('Is all out-of-hours use waste?', 'No. Some equipment must run all the time. The excess above the base load is the part to investigate.'),
   ('Why do opening hours matter so much?', "They decide which half hours count as closed. If the building is used on Saturdays but the calendar says closed, that use shows as out-of-hours."),
   ('How quickly can I see whether a change worked?', 'Within a few weeks, using the before-and-after view in the analyser.')],
  [('base-load.html', 'Base load', 'The other half of the picture: what always runs.'),
   ('example-office-analysis.html', 'Worked example', 'Out-of-hours use in one office, with figures.'),
   ('sectors.html', 'By sector', 'What normal looks like in schools, offices, leisure centres and more.')],
  'What out-of-hours electricity use is, how to find it in half-hourly data (opening hours, heatmap, day types, start and end of the day), common causes, and fixes.'))

# ── BASE LOAD ───────────────────────────────────────────────────────────
PAGES.append(guide_page(
  'base-load.html',
  'Base load electricity: what it is and how to cut it',
  'Base load: what never switches off',
  'Every building has a level of use it never drops below. It runs every hour of the year, so small cuts add up.',
  'What base load electricity is, how to measure it from half-hourly data, what makes it up, and how to reduce it. Each kilowatt running all year is 8,760 kWh.',
  '''
<p class="answer">Base load is the minimum electricity a building uses at all times, day and night. Each kilowatt of it runs 8,760 hours a year: 8,760 kWh, or about £2,190 at 25p/kWh. Measure it, find out what makes it up, and switch off what doesn't need to run.</p>

<h2 id="measure">How to measure it</h2>
<p>The analyser finds the level demand stays above 95% of the time (the 5th percentile of all valid half-hourly readings, in kW). It doesn't use the single lowest reading, because one meter fault or power cut would set it too low. The lowest half hour is shown alongside for comparison.</p>

<h2 id="what">What makes it up</h2>
<ul><li>IT: servers, network equipment and phone systems</li><li>Refrigeration: kitchen fridges, freezers, vending machines and water coolers</li><li>Pumps and fans that run continuously</li><li>Water heaters and boilers kept on standby</li><li>Security systems, fire alarms and emergency lighting</li><li>Equipment left on standby, or left running by mistake</li></ul>

<h2 id="reduce">How to reduce it</h2>
<ol><li><strong>Walk round at night or at a weekend</strong> and note what's on.</li><li><strong>Sort it</strong> into must run, could run less, and shouldn't be on.</li><li><strong>Fix the easy ones</strong>: timers on water heaters and vending machines, switch-off routines, fewer servers. Turning off a 0.5 kW heater left on all year saves about £1,100.</li><li><strong>Check it monthly.</strong> A step up means something new is on. The analyser flags lasting changes.</li></ol>
''',
  [('measure', 'How to measure it'), ('what', 'What makes it up'), ('reduce', 'How to reduce it')],
  [('What is a typical base load?', 'It depends on the building. Sites with lots of IT or refrigeration run much higher than a school. Compare each site with its own history and with similar buildings.'),
   ('Why is my base load higher at weekends than overnight on weekdays?', "It shouldn't be. Something is switching on at weekends, such as heating frost protection or a booking. Check the heatmap."),
   ('How much does 1 kW of base load cost?', "About £2,190 a year at 25p/kWh. Multiply 8,760 by your own rate.")],
  [('out-of-hours-electricity.html', 'Out-of-hours use', 'Use above the base load while the building is closed.'),
   ('supply-capacity.html', 'Supply capacity', 'The other end of the scale: your busiest half hours.'),
   ('example-office-analysis.html', 'Worked example', 'Base load in one office, with figures.')],
  'What base load is, how to measure it from half-hourly data (5th percentile, not the minimum), what makes it up, how to reduce it; 1 kW all year is 8,760 kWh.'))

# ── SUPPLY CAPACITY ─────────────────────────────────────────────────────
PAGES.append(guide_page(
  'supply-capacity.html',
  'Supply capacity and kVA: room for heat pumps and EVs',
  'Supply capacity and kVA',
  'Before adding heat pumps or EV chargers, check how close your busiest half hours already come to your supply limit.',
  'Agreed supply capacity explained: kW to kVA, comparing half-hourly peaks with capacity, and room for heat pumps and EV charging.',
  '''
<p class="answer">Your agreed supply capacity is the maximum demand your connection is set up for, in kVA. Convert your busiest half hours from kW to kVA (divide by the power factor) and compare. The gap is your headroom for new equipment such as heat pumps and EV chargers.</p>

''' + photo('plant-outside', 'Two engineers with a tablet beside packaged plant, flues and pipework outside a large building', '') + '''
<h2 id="what">What agreed supply capacity is</h2>
<p>Larger supplies have an agreed (or authorised) capacity, set in the connection agreement and shown on the bill in kVA. You pay a daily charge for it whether you use it or not, and going over it can bring extra charges.</p>

<h2 id="kva">kW and kVA</h2>
<p>Half-hourly data gives average power in kW. Capacity is set in kVA, which also counts reactive power drawn by equipment such as motors. The power factor links them:</p>
<div class="note"><strong>kVA = kW ÷ power factor.</strong> At a power factor of 0.95, a 95 kW peak is 100 kVA. If your bill includes reactive power charges, your power factor is probably below 0.95.</div>

<h2 id="headroom">Working out headroom</h2>
<ol><li><strong>Find your busiest half hours</strong> over a full year, to include winter.</li><li><strong>Convert them to kVA.</strong></li><li><strong>Keep a margin</strong>, say 10%, below the agreed capacity.</li><li><strong>Headroom</strong> is the largest constant load you could add without breaching that margin.</li></ol>
<p>Half-hour averages hide very short spikes, so confirm with your network operator before relying on it.</p>

<h2 id="new-load">Heat pumps and EV charging</h2>
<p>A heat pump with a coefficient of performance (COP) of 3 draws about 50 kW of electricity to produce 150 kW of heat. It works hardest in winter, when peaks are usually highest. Overnight EV charging falls when sites are quietest. The analyser tests a new load at a chosen time and season against your actual peaks.</p>
''',
  [('what', 'What agreed supply capacity is'), ('kva', 'kW and kVA'), ('headroom', 'Working out headroom'), ('new-load', 'Heat pumps and EV charging')],
  [('Where do I find my agreed supply capacity?', 'On your electricity bill or connection agreement, in kVA. Your supplier can confirm it.'),
   ('What power factor should I use?', "Use 0.95 if you don't know it. It's probably lower if your bill shows reactive power charges."),
   ('Is half-hourly data enough to plan a new connection?', "It's a good first check. For a significant new load, speak to your network operator first.")],
  [('base-load.html', 'Base load', 'The demand that never goes away.'),
   ('example-office-analysis.html', 'Worked example', 'Peaks against capacity in one office.'),
   ('how-it-works.html', 'How the analyser works', 'Including how headroom is worked out.')],
  'Agreed supply capacity in kVA, kW to kVA via power factor, headroom from half-hourly peaks with a safety margin, and checking heat pumps and EV charging.'))

# ── WORKED EXAMPLE: SCHOOL ──────────────────────────────────────────────
PAGES.append(guide_page(
  'example-school-analysis.html',
  'Worked example: a primary school\'s half-hourly data',
  'Worked example: one primary school',
  'A year of data from a primary school, run through the analyser with its term dates entered. The school is made up; every figure is what the analyser reports.',
  'A primary school\'s year of half-hourly data: heating left on through half term, evening lettings, and what the analyser found once term dates were entered.',
  '''
<p class="answer">This school used 31% of its electricity while closed: about £1,260 a year above what always runs, at 25p/kWh. The biggest issue was October half term, when the empty building used more than twice what it should have.</p>

<div class="note"><strong>Made-up data.</strong> <a href="samples/example-school.csv" download>Download the file</a> and load it into the <a href="analyser/">analyser</a> to follow along. Set the building type to School and enter the term dates below as closures.</div>

<h2 id="setup">Setting it up</h2>
<p>The analyser never assumes school holidays. For this school we entered:</p>
<ul><li>Building type: School (open 07:00 to 17:30 on weekdays)</li><li>Six closures: Easter, May half term, summer, October half term, Christmas and February half term</li><li>Hours marked as confirmed</li></ul>

<h2 id="headline">The headline figures</h2>
<div class="table-wrap"><table><thead><tr><th>Measure</th><th class="num">Value</th></tr></thead><tbody>
<tr><td>Electricity a year</td><td class="num">57,753 kWh</td></tr><tr><td>Energy cost a year (25p/kWh)</td><td class="num">£14,438</td></tr>
<tr><td>Base load</td><td class="num">1.9 kW</td></tr><tr><td>Busiest half hour</td><td class="num">30.1 kW</td></tr>
<tr><td>Use while closed</td><td class="num">31%</td></tr><tr><td>Closed-hours excess</td><td class="num">£1,261 a year</td></tr></tbody></table></div>

<h2 id="heatmap">The year at a glance</h2>
<figure class="figure"><img src="images/heatmap-school.png" width="2464" height="896" alt="Heatmap of a school year: dark blocks in term time, blank holidays, a pale block across October half term and thin stripes on Tuesday and Thursday evenings" loading="lazy"><figcaption>One column per day and one row per half hour. Term weeks are dark and holidays should be blank, but October half term isn't.</figcaption></figure>
<p>Two things stand out: a block across October half term, and stripes after 18:00 on two evenings a week. See <a href="reading-a-heatmap.html">how to read a heatmap</a>.</p>

<h2 id="findings">What the analyser found</h2>
<h3>1. Heating left on through October half term</h3>
<p>The three worst days of the year were all in half term, each about 100 kWh above base load. From 25 October, demand was at least 15% above expected on five of nine days, and on average more than double. The 07:00 to 17:00 weekday pattern suggests heating and ventilation stayed on the term-time schedule.</p>
<h3>2. Evening lettings</h3>
<p>Weekday evenings are the largest share of the closed-hours excess: 2,765 kWh above base load. The Tuesday and Thursday stripes are a hall letting. Enter it as open hours, and check whether it lights and heats more of the building than it needs.</p>
<h3>3. Holidays and weekends</h3>
<p>Holidays added 1,157 kWh above base load, mostly in October. Weekends were close to base load (556 kWh on Saturdays and 526 kWh on Sundays over the year), as you'd expect.</p>

<h2 id="next-steps">What we'd do next</h2>
<ol><li><strong>Add half terms to the building management system</strong> as well as the long holidays.</li><li><strong>Enter the lettings in the calendar</strong> and check what the hall booking switches on.</li><li><strong>Check the next half term</strong> with the before-and-after comparison.</li></ol>
''',
  [('setup', 'Setting it up'), ('headline', 'The headline figures'), ('heatmap', 'The year at a glance'), ('findings', 'What the analyser found'), ('next-steps', "What we'd do next")],
  [('Do I have to enter term dates?', 'Yes. They vary between schools and years, so the analyser never assumes them. Without them, holidays count as school days.'),
   ('Should a school use nothing in the holidays?', 'No. The base load carries on (IT, fridges, security). Holiday use above the base load is what to look at.'),
   ('Is this real data?', "No. It's made up so we can show the method without using anyone's real data.")],
  [('reading-a-heatmap.html', 'Reading a heatmap', 'How to spot patterns like half term at a glance.'),
   ('schools-electricity.html', 'Schools and colleges', 'What to check first in education buildings.'),
   ('proving-savings.html', 'Proving a saving', 'Checking whether the half-term fix worked.')],
  'A primary school with term dates entered: 31% of use while closed, £1,261 a year above base load; heating left on through October half term (demand more than double); evening lettings.',
  crumbs=[HOME, GUIDES, ('Worked example: school', 'example-school-analysis.html')]))

# ── READING A HEATMAP ───────────────────────────────────────────────────
PAGES.append(guide_page(
  'reading-a-heatmap.html',
  'How to read a half-hourly electricity heatmap',
  'How to read a half-hourly heatmap',
  'A heatmap shows every half hour of a year on one chart. Once you know what to look for, problems are easy to spot.',
  'How to read a half-hourly electricity heatmap: what the axes and colours mean, what normal looks like, and the patterns that point to waste.',
  '''
<p class="answer">A half-hourly heatmap has one column per day and one row per half hour, darker for higher demand. Normal use is a dark band during opening hours. Anything dark outside it, at night, at weekends or in holidays, is worth checking.</p>

<h2 id="axes">What you're looking at</h2>
<ul><li><strong>Across:</strong> days.</li><li><strong>Down:</strong> time of day, midnight to midnight.</li><li><strong>Colour:</strong> demand, pale (low) to dark (high).</li></ul>

<figure class="figure"><img src="images/heatmap-office.png" width="2464" height="896" alt="Heatmap of an office year: a dark weekday band, pale nights, and weekends that are sometimes busy" loading="lazy"><figcaption>An office (made-up data). The weekday band is clear, and some Saturdays are as busy as weekdays.</figcaption></figure>

<h2 id="normal">What normal looks like</h2>
<p>A weekday building shows a dark band in working hours, pale weekends and pale nights. Winter is often a little darker. The edges of the band show when the building really starts and stops.</p>

<h2 id="patterns">Patterns worth checking</h2>
<div class="table-wrap"><table><thead><tr><th>What you see</th><th>What it usually means</th></tr></thead><tbody>
<tr><td>A block where a holiday should be blank</td><td>Heating running to the normal schedule with nobody in</td></tr>
<tr><td>Thin stripes in the evening on the same weekdays</td><td>Lettings, classes or cleaning</td></tr>
<tr><td>The band starting well before opening</td><td>Heating set to start too early</td></tr>
<tr><td>Nights that get darker from a certain date</td><td>Something new is running all the time</td></tr>
<tr><td>A single dark column</td><td>An event, a fault or a reading error</td></tr>
<tr><td>Grey or striped gaps</td><td>Missing data (not zero use)</td></tr></tbody></table></div>

<figure class="figure"><img src="images/heatmap-school.png" width="2464" height="896" alt="Heatmap of a school year showing term blocks, holidays, a pale half-term block and evening stripes" loading="lazy"><figcaption>A primary school (made-up data): heating left on through October half term, and evening lettings. See the <a href="example-school-analysis.html">worked example</a>.</figcaption></figure>

<h2 id="next">Putting a cost on what you see</h2>
<p>In the analyser, click any day to compare it with a typical day, then use the out-of-hours and unusual-day findings to put a cost on what you've spotted.</p>
''',
  [('axes', "What you're looking at"), ('normal', 'What normal looks like'), ('patterns', 'Patterns worth checking'), ('next', 'Putting a cost on what you see')],
  [('What is a carpet plot?', 'Another name for the same chart.'),
   ('Why are some days grey?', "They have no valid readings. Missing data is shown as missing, not as zero use."),
   ('Can I see one day in detail?', 'Yes. Click any day on the heatmap in the analyser.')],
  [('example-school-analysis.html', 'Worked example: school', 'The school heatmap, explained finding by finding.'),
   ('out-of-hours-electricity.html', 'Out-of-hours use', 'Putting a cost on what the heatmap shows.'),
   ('glossary.html', 'Glossary', 'The terms used in these guides.')],
  'How to read a half-hourly heatmap (days across, time of day down, colour for demand) and the patterns that point to waste.'))

# ── PROVING A SAVING ────────────────────────────────────────────────────
PAGES.append(guide_page(
  'proving-savings.html',
  'How to prove an energy saving worked, with half-hourly data',
  'Proving a saving worked',
  "You've changed a setting or replaced equipment. Half-hourly data shows whether it worked, if you compare like with like.",
  'How to use half-hourly data to show whether a change saved energy: matched before-and-after periods, the right measure, and what can mislead.',
  '''
<p class="answer">Compare matching periods before and after the change: the same days of the week, the same types of day, and enough weeks to even out variation. Look at the part of demand the change should affect, such as base load or out-of-hours use, rather than the total bill.</p>

''' + photo('board-review', 'A team reviewing charts and printed reports around a meeting table, with solar panels and battery units outside the window', 'A saving is easier to sign off when the before-and-after comparison is fair.') + '''
<h2 id="match">Compare like with like</h2>
<ul><li><strong>Same types of day.</strong> Weekdays with weekdays, holidays with holidays. Bank holidays in one period skew the result.</li><li><strong>Enough data.</strong> Four to eight weeks either side. One week can be thrown by a single odd day.</li><li><strong>Close together</strong>, so weather and seasons matter less.</li><li><strong>Leave out the days</strong> when the work was done.</li></ul>

<h2 id="measure">Measure the right thing</h2>
<p>Choose the measure the change should affect:</p>
<div class="table-wrap"><table><thead><tr><th>Change</th><th>Look at</th></tr></thead><tbody>
<tr><td>Heating or ventilation schedules</td><td>Out-of-hours use, and demand around opening and closing</td></tr>
<tr><td>Switching off equipment overnight</td><td>Base load</td></tr>
<tr><td>LED lighting</td><td>Demand during opening hours</td></tr>
<tr><td>Holiday settings in the building controls</td><td>Use during closures</td></tr></tbody></table></div>
<p>Total use mixes your change with everything else, such as occupancy, weather and new equipment, so a real saving can get lost.</p>

<h2 id="weather">Weather and seasons</h2>
<p>If the before period was colder, some of the drop is weather. For heating changes, cross-check against the same weeks a year earlier, or adjust using degree days.</p>

<h2 id="analyser">In the analyser</h2>
<ul><li><strong>Did a change make a difference?</strong> (Base load tab) compares matched weeks either side of a date.</li><li><strong>Compare periods</strong> (Heatmap tab) shows two periods side by side.</li><li><strong>Persistent changes</strong> (Unusual days tab) flags lasting shifts.</li></ul>
<p>For formal verification of savings, see the International Performance Measurement and Verification Protocol (IPMVP).</p>
''',
  [('match', 'Compare like with like'), ('measure', 'Measure the right thing'), ('weather', 'Weather and seasons'), ('analyser', 'In the analyser')],
  [('How long should I wait before checking?', 'Four to eight weeks after the change, compared with the same before.'),
   ('Why has our bill not gone down?', 'Other changes, such as occupancy, weather, prices or new equipment, can hide it. Compare the measure the change should affect.'),
   ('Can this replace a formal M&amp;V report?', "It's a good check, but formal measurement and verification (for example under IPMVP) agrees the baseline, adjustments and reporting up front.")],
  [('base-load.html', 'Base load', 'The measure most switch-off changes affect.'),
   ('out-of-hours-electricity.html', 'Out-of-hours use', 'The measure schedule changes affect.'),
   ('example-school-analysis.html', 'Worked example: school', 'A half-term fix worth checking.')],
  'Proving a saving with half-hourly data: matched before-and-after periods, the right measure for the change, weather effects, and the analyser tools.'))

# ── MHHS ────────────────────────────────────────────────────────────────
PAGES.append(guide_page(
  'half-hourly-settlement.html',
  'Market-wide half-hourly settlement (MHHS) explained',
  'Market-wide half-hourly settlement explained',
  "Britain is moving every electricity meter onto half-hourly settlement. Here's what that means for your organisation.",
  'What market-wide half-hourly settlement (MHHS) is, the timetable to 2027, who runs it, and what it means for business and public sector electricity customers.',
  '''
<p class="answer">Market-wide half-hourly settlement (MHHS) means suppliers are charged for what their customers actually use in each half hour, instead of an estimate from standard profiles. It began in October 2025 and is due to finish in May 2027. If you have a smart or advanced meter, your half-hourly readings are part of how you're settled, so ask your supplier for them.</p>

''' + photo('site-plans-substation', 'Four people in hard hats and high-visibility vests reviewing site plans next to a substation and solar panels') + '''
<h2 id="what">What it is</h2>
<p>Large sites have been settled half-hourly for years. Smaller sites mostly used standard profiles: estimates of when a typical customer uses electricity. MHHS replaces them with actual readings wherever a meter can provide them.<sup><a href="#sources">1</a></sup></p>
<p>The programme's stated objective is "to maximise the opportunities provided by smart metering by developing and implementing an enduring process for MHHS, that delivers benefits for consumers and enables a smart, flexible energy system."<sup><a href="#sources">2</a></sup></p>

<h2 id="who">Who runs it</h2>
<p>Ofgem decided to go ahead with MHHS on 20 April 2021.<sup><a href="#sources">1</a></sup> Ofgem is the programme sponsor and appointed Elexon as Senior Responsible Owner and Implementation Manager. Delivery is led by the energy industry.<sup><a href="#sources">2</a></sup></p>

<h2 id="timeline">The timetable</h2>
<div class="table-wrap"><table><thead><tr><th>Date</th><th>Milestone</th></tr></thead><tbody>
<tr><td>20 April 2021</td><td>Ofgem decision to introduce MHHS (originally planned to finish in October 2025)</td></tr>
<tr><td>21 October 2025</td><td>Migration to the new arrangements began, for all meter types</td></tr>
<tr><td>7 May 2027</td><td>Migration due to be complete, with all energy settled under the new arrangements</td></tr>
<tr><td>2 July 2027</td><td>Settlement moves from a 14-month to a four-month timetable</td></tr></tbody></table></div>
<p>Dates as published in November 2026; check the programme's milestone page for updates.<sup><a href="#sources">1, 3</a></sup></p>

<h2 id="you">What it means for your organisation</h2>
<ul><li><strong>You don't need to do anything to be moved across.</strong> Your supplier handles it.</li><li><strong>Microbusinesses can't opt out.</strong> Ofgem's decision says half-hourly data will be processed for settlement for domestic customers unless they opt out, and that microbusiness customers will not be able to opt out.<sup><a href="#sources">1</a></sup></li><li><strong>Tariffs may change.</strong> Ofgem expects more time-of-use tariffs that reward using electricity at cheaper times.<sup><a href="#sources">1</a></sup></li><li><strong>Half-hourly data becomes standard.</strong> Ask your supplier for a copy.</li></ul>
<p>As time-of-use tariffs spread, when you use electricity will matter more. Knowing your pattern now helps you choose a tariff and cut costs.</p>
''' + sources([
    ('Ofgem: Electricity Retail Market-wide Half-hourly Settlement: Decision and Full Business Case (20 April 2021)', 'https://www.ofgem.gov.uk/decision/electricity-retail-market-wide-half-hourly-settlement-decision-and-full-business-case'),
    ('MHHS Programme: Programme overview', 'https://www.mhhsprogramme.co.uk/programme-information/programme-overview'),
    ('MHHS Programme: Key programme milestones', 'https://www.mhhsprogramme.co.uk/programme-information/key-programme-milestones')]),
  [('what', 'What it is'), ('who', 'Who runs it'), ('timeline', 'The timetable'), ('you', 'What it means for your organisation')],
  [('When does market-wide half-hourly settlement finish?', "Migration is due to be complete on 7 May 2027, with the move to a four-month settlement timetable on 2 July 2027, according to the MHHS programme's published milestones."),
   ('Do I need to do anything?', 'No. Your supplier moves your meters across.'),
   ('Can a business opt out of half-hourly data collection?', "Ofgem's 2021 decision says microbusiness customers will not be able to opt out of their half-hourly data being processed for settlement. Domestic customers can opt out.")],
  [('get-your-data.html', 'Getting your data', 'What to ask your supplier for.'),
   ('glossary.html', 'Glossary', 'Settlement, MPAN, kVA and other terms.'),
   ('out-of-hours-electricity.html', 'Out-of-hours use', 'The first thing to look at in your data.')],
  'Market-wide half-hourly settlement: Ofgem decision 20 April 2021; migration began 21 October 2025, due complete 7 May 2027; four-month settlement timetable from 2 July 2027; microbusinesses cannot opt out.'))

# ── GLOSSARY ────────────────────────────────────────────────────────────
GLOSSARY = [
  ('Agreed supply capacity', 'The maximum demand, in kVA, a connection is set up for. <a href="supply-capacity.html">More</a>.'),
  ('Annualised figure', 'A yearly figure scaled up from less than a full year of readings.'),
  ('Base load', 'The level of demand a building rarely drops below (the 5th percentile). <a href="base-load.html">More</a>.'),
  ('Closed-hours excess', 'Electricity used while a building should be closed, above its base load. The analyser ranks sites by it. <a href="out-of-hours-electricity.html">More</a>.'),
  ('Coverage', 'The share of expected half-hourly readings that are present and valid.'),
  ('Degree days', 'A measure of how cold or warm a period was, used to compare energy use fairly.'),
  ('DNO', 'Distribution network operator: runs the local network and your connection.'),
  ('Half-hourly (HH) data', 'A record of the electricity used in every half hour: 48 readings a day.'),
  ('Heatmap', 'A chart of every half hour, one column per day, coloured by demand. <a href="reading-a-heatmap.html">More</a>.'),
  ('kVA', 'Kilovolt-ampere: the unit supply capacity is set in. kVA = kW ÷ power factor.'),
  ('kW', 'Kilowatt: the rate electricity is used at a moment. Half-hourly kWh ÷ 0.5 = average kW.'),
  ('kWh', 'Kilowatt-hour: energy, what you are billed for. 1 kW for one hour.'),
  ('Load factor', 'Average demand divided by peak demand. A low load factor means demand has short, high peaks.'),
  ('Market-wide half-hourly settlement (MHHS)', 'The move to settle every electricity meter in Great Britain using half-hourly data. <a href="half-hourly-settlement.html">More</a>.'),
  ('MPAN', 'Meter point administration number: the 13-digit supply number on your bill.'),
  ('Peak demand', 'The highest half-hourly average demand in a period, usually in kW or kVA.'),
  ('Power factor', 'The ratio of real power (kW) to apparent power (kVA), between 0 and 1. Equipment such as motors lowers it.'),
  ('Settlement', 'How the industry works out what each supplier\'s customers used, and when.'),
  ('Time-of-use tariff', 'A tariff with different rates at different times of day.'),
]
NAV_PARENT['glossary.html'] = 'guides.html'
PAGES.append(Page(
  'glossary.html', 'Glossary of half-hourly electricity terms',
  'Simple definitions of half-hourly electricity terms: base load, kW, kWh, kVA, power factor, MPAN, agreed supply capacity, settlement and more.',
  page_hero('Guide', 'Glossary', 'Simple definitions of the terms used in half-hourly electricity data and on this site.',
            crumbs=[HOME, GUIDES, ('Glossary', 'glossary.html')])
  + guide(updated_line() + '<dl class="glossary">' + ''.join(
      f'<div id="{t.lower().split(" (")[0].replace(" ", "-")}"><dt>{t}</dt><dd>{d}</dd></div>' for t, d in GLOSSARY) + '</dl>')
  + cta('See the terms in your own data', "It's free, there's no sign-up, and nothing is uploaded."),
  crumbs=[HOME, GUIDES, ('Glossary', 'glossary.html')], article=True, section='Guides',
  summary='Definitions: base load, closed-hours excess, kW, kWh, kVA, power factor, MPAN, agreed supply capacity, settlement, MHHS, heatmap, load factor and more.',
  schema=[{'@type': 'DefinedTermSet', 'name': 'Half-hourly electricity glossary', 'hasDefinedTerm': [
      {'@type': 'DefinedTerm', 'name': t, 'description': strip_tags(d).replace(' More.', '')} for t, d in GLOSSARY]}]))

# ── SECTORS ─────────────────────────────────────────────────────────────
SECTOR_DATA = [
  ('schools-electricity.html', 'Schools and colleges', 'Electricity use in schools and colleges',
   "Schools are closed for about 13 weeks a year, so holidays should show very little use. When they don't, a schedule needs fixing.",
   'In holidays, at weekends and in the evening, use should be close to the base load. Enter term dates in the calendar before anything else.',
   ['Heating running through holidays, especially half terms', 'IT suites and screens left on overnight', 'Kitchen equipment and water heaters on in holidays', 'Lettings that run the whole building for one hall', 'Pool or sports hall plant on the main building schedule'],
   'Enter each holiday as a closure and regular lettings as open hours, so the figures show what the school can control.',
   [('Should holiday use be zero?', 'No. Look at holiday use above the base load.'),
    ('How do I handle evening lettings?', "Enter them as open hours, then check whether the letting needs the whole building heated and lit.")]),
  ('offices-council-buildings.html', 'Offices and council buildings', 'Electricity use in offices and council buildings',
   "Office electricity use should drop sharply when people go home. Whatever carries on running is worth investigating.",
   'Expect a clear weekday pattern, falling to base load in the evening and at weekends. Hybrid working has made Mondays and Fridays quieter, but heating and lighting often run as if every desk were full.',
   ['Ventilation and cooling running all night or weekend', 'Heating starting well before staff arrive', 'Whole floors lit for one late worker', 'Server rooms with their own cooling', 'Evening council meetings and elections missing from the calendar'],
   'Set different hours by day if Mondays and Fridays are quieter, and add bank holidays, which many schedules miss.',
   [('Why does our office use so much at weekends?', 'Usually heating or cooling on the wrong schedule, or a weekend activity using the whole building.'),
    ('Has hybrid working changed what to look for?', 'Yes. If quiet days use as much as busy ones, plant runs to a full-occupancy schedule.')]),
  ('leisure-centres.html', 'Leisure centres and pools', 'Electricity use in leisure centres and pools',
   'Long opening hours and pools that run around the clock make leisure centres heavy electricity users. Start by understanding what makes up the overnight use.',
   'Expect a high base load from pool pumps, ventilation and dehumidification, with opening hours from early morning to late evening, seven days a week.',
   ['Pool hall ventilation at daytime levels overnight', 'Filtration pumps that could run slower at night', 'Sports hall lighting left on between bookings', 'Saunas and water heaters on earlier than needed', 'Plant running through maintenance closures'],
   'Hours vary by day and in school holidays, so enter them carefully. With a short closed period each night, small setting changes make a big difference.',
   [('Is a high base load normal for a pool?', 'Yes, pool equipment runs continuously. Check whether it runs harder than needed overnight.'),
    ('What should I look at first?', 'Overnight use. Pool covers and slower night ventilation are common first steps.')]),
  ('healthcare-electricity.html', 'Healthcare', 'Electricity use in healthcare buildings',
   'Hospitals and many care settings run 24 hours a day, so out-of-hours use is less relevant. Comparing day with night, and peaks with supply capacity, tells you more.',
   'Expect continuous use with a rise during the day. Clinics, surgeries and offices on the same estate keep office hours and should be treated like offices.',
   ['Night use close to daytime use in non-clinical areas', 'Weekend use in outpatient and admin buildings', 'Peaks near supply capacity before adding heat pumps or EV charging', 'Base load rising after new equipment or a refurbishment'],
   'Set 24-hour buildings as always open, and give clinics and offices their real hours.',
   [('Can out-of-hours analysis work for a hospital?', 'For 24-hour buildings, compare day with night and track the base load instead. Clinics and offices work like any office.'),
    ('Why does supply capacity matter so much in healthcare?', 'Heat pumps add a large winter load. Check your winter peaks against capacity first.')]),
  ('industrial-warehouses.html', 'Industrial and warehouses', 'Electricity use in industrial sites and warehouses',
   "With shift work, getting the calendar right matters more than anything. Once it's set, use during shutdowns, compressed air leaks and refrigeration are easy to see.",
   'Demand follows the shift pattern, stepping up when a shift starts and down when it ends. During planned shutdowns, use should fall close to the base load.',
   ['Compressed air left on overnight and at weekends', 'Refrigeration working harder than needed', 'Shutdown weeks that never get near the base load', 'Warehouse lighting on outside shift times', 'Peaks against capacity before adding EV charging'],
   'Enter shift times, including nights, and planned shutdowns.',
   [('How do I spot compressed air leaks?', 'If compressors keep running after production stops, the steady load is often leaks.'),
    ('Can the analyser handle night shifts?', 'Yes. Hours can run past midnight and differ by day.')]),
  ('retail-hospitality.html', 'Retail and hospitality', 'Electricity use in retail and hospitality',
   'Fixed trading hours make out-of-hours use easy to spot. Refrigeration, signs and kitchen equipment are the most common causes.',
   'Demand follows trading hours, with some use for preparation before opening and cleaning after closing. In food retail and hospitality, refrigeration means a high base load.',
   ['Fridges without night blinds or covers', 'Signs and display lighting on all night', 'Kitchen equipment on long before service', 'Heating and cooling on an out-of-date schedule'],
   'Include preparation and cleaning time in the opening hours.',
   [('Why is our base load so high?', "Usually refrigeration. Check night blinds, door seals and temperature settings first."),
    ('How do I compare several shops or venues?', 'Load one file per meter. The analyser ranks them and compares sites by building type.')]),
]

SECTOR_PHOTOS = {
    'schools-electricity.html': ('town-school-leisure', 'Illustration of a town with a school, a sports pitch and a swimming pool among streets of houses'),
    'offices-council-buildings.html': ('estate-town', 'Illustration of a town with offices, a town hall, a school, a leisure centre, housing and an energy centre'),
    'leisure-centres.html': ('town-school-leisure', 'Illustration of a leisure centre with an outdoor pool next to a school and sports pitch'),
    'healthcare-electricity.html': ('estate-hospital', 'Illustration of a hospital estate with clinical buildings, a multi-storey car park, plant compounds and a substation'),
    'industrial-warehouses.html': ('estate-business-park', 'Illustration of a business park with warehouses, a plant compound, battery storage, a substation and ground-mounted solar'),
    'retail-hospitality.html': ('estate-business-park', 'Illustration of commercial units with car parking, delivery vans and on-site plant'),
}

for file, short, h1, lead, normal, checks, calendar_tip, faqs in SECTOR_DATA:
    PAGES.append(guide_page(
      file, f'{short}: what half-hourly data shows', h1, lead,
      f'Half-hourly electricity data in {short.lower()}: what normal looks like, what to check first and how to set opening hours.',
      f'''
<p class="answer">{normal}</p>
{photo(*SECTOR_PHOTOS[file])}
<h2 id="check">What to check first</h2>
<ul>{''.join(f'<li>{c}</li>' for c in checks)}</ul>

<h2 id="calendar">Setting the opening hours</h2>
<p>{calendar_tip}</p>
''',
      [('check', 'What to check first'), ('calendar', 'Setting the opening hours')],
      faqs,
      [('out-of-hours-electricity.html', 'Out-of-hours use', 'How to find and reduce use while closed.'),
       ('base-load.html', 'Base load', 'What always runs.'),
       ('sectors.html', 'Other sectors', 'Schools, offices, leisure, healthcare, industrial and retail.')],
      f'{short}: what normal half-hourly demand looks like and what to check first.',
      crumbs=[HOME, SECTORS, (short, file)]))

PAGES.append(Page(
  'sectors.html', 'What to look for by sector | Half Hourly Insights',
  'What half-hourly electricity data shows in schools, offices and council buildings, leisure centres, healthcare, industrial sites and retail.',
  page_hero('Sectors', 'What to look for in your sector', 'Each type of building uses electricity differently. Choose yours to see what normal looks like and what to check first.',
            crumbs=[HOME, SECTORS]) +
  '<section class="section"><div class="section-inner">' +
  photo('estate-town', 'Illustration of a town with offices, a town hall, a school, a leisure centre, housing and an energy centre', cls='figure figure-wide', lazy=False) +
  '<div class="link-grid">' +
  ''.join(link_card(f, s, lead, 'Read more') for f, s, _, lead, *_ in SECTOR_DATA) +
  '</div></div></section>' + cta('Check your own sites', 'Load several meters at once and the analyser ranks them, so you know which site to look at first.'),
  crumbs=[HOME, SECTORS], section='Sectors', summary='Index of sector pages.'))

GUIDE_LIST = [
    ('get-your-data.html', 'Getting your half-hourly data', 'Who has it, what to ask for, a letter template, and the file formats the analyser reads.'),
    ('example-office-analysis.html', 'Worked example: one office, one year', 'What the analyser found in a year of data from a small office.'),
    ('example-school-analysis.html', 'Worked example: a primary school', 'Heating left on through half term, evening lettings, and term dates.'),
    ('reading-a-heatmap.html', 'How to read a heatmap', 'Every half hour of a year on one chart, and the patterns to look for.'),
    ('out-of-hours-electricity.html', 'Out-of-hours electricity use', 'How to find use while the building is closed, and reduce it.'),
    ('base-load.html', 'Base load', 'What always runs, how to measure it and how to reduce it.'),
    ('supply-capacity.html', 'Supply capacity and kVA', 'Room for heat pumps, EV charging and other new equipment.'),
    ('proving-savings.html', 'Proving a saving worked', 'How to compare before and after fairly.'),
    ('half-hourly-settlement.html', 'Half-hourly settlement (MHHS) explained', 'What the move to half-hourly settlement means, and the timetable to 2027.'),
    ('glossary.html', 'Glossary', 'kW, kWh, kVA, base load, MPAN and other terms.'),
    ('how-it-works.html', 'How the analyser works', 'Each step, from reading your file to the report.'),
]
NAV_PARENT['get-your-data.html'] = 'guides.html'
PAGES.append(Page(
  'guides.html', 'Guides to half-hourly electricity data | Half Hourly Insights',
  'Simple guides to half-hourly electricity data: getting it, out-of-hours use, base load, supply capacity and worked examples.',
  page_hero('Guides', 'Guides to half-hourly data', 'Clear answers to the questions people ask when they first look at half-hourly electricity data.',
            crumbs=[HOME, GUIDES]) +
  '<section class="section"><div class="section-inner"><div class="link-grid">' +
  ''.join(link_card(f, t, d) for f, t, d in GUIDE_LIST) +
  '</div><p class="note" style="margin-top:32px">Looking for your sector? See <a href="sectors.html" style="color:var(--blue);text-decoration:underline">what to look for by sector</a>.</p></div></section>'
  + cta('Ready to look at your own data?', "It's free, there's no sign-up, and nothing is uploaded."),
  crumbs=[HOME, GUIDES], section='Guides', summary='Index of guides.'))
