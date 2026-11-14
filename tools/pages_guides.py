"""
Guides and sector pages. Each guide opens with a direct answer (what search
and AI answer engines quote), carries a few questions marked up as FAQPage,
and ends with links to related guides.

Written for a general business reader: plain words, terms explained on first
use, as long as it needs to be and no longer. "Closed-hours excess" is the
analyser's figure; "out-of-hours use" is the general idea.

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
  'We ran a year of half-hourly data from a small office through the analyser. The office and its data are made up, but every figure below is exactly what the analyser reports.',
  'One office, one year of half-hourly data: use while closed, base load, peaks against supply capacity, and what to do next.',
  f'''
<p class="answer">This office used a third of its electricity (33%) while the building was closed. Leaving aside what always has to run, that closed-hours use costs about £2,800 a year at 25p/kWh, and almost half of it happens on Saturdays.</p>

<div class="note"><strong>Made-up data.</strong> We invented this office so we could show the method without using anyone's real data. <a href="samples/example-office.csv" download>Download the file</a> and load it into the <a href="analyser/">analyser</a> to follow along.</div>

<h2 id="headline">The headline figures</h2>
<div class="table-wrap"><table><thead><tr><th>Measure</th><th class="num">Value</th><th>What it means</th></tr></thead><tbody>
<tr><td>Electricity a year</td><td class="num">79,191 kWh</td><td>Scaled up from 363 days of valid readings (99.5% coverage)</td></tr>
<tr><td>Energy cost a year</td><td class="num">£19,798</td><td>At a flat rate of 25p/kWh, before standing and capacity charges</td></tr>
<tr><td>Base load</td><td class="num">2.6 kW</td><td>The level demand rarely drops below</td></tr>
<tr><td>Busiest half hour</td><td class="num">25.5 kW</td><td>28 January 2025, midday</td></tr>
<tr><td>Use while closed</td><td class="num">33%</td><td>Using the default office hours, 07:00 to 19:00 on weekdays</td></tr>
<tr><td>Closed-hours excess</td><td class="num">£2,776</td><td>Electricity used while closed, above the base load, at 25p/kWh</td></tr>
</tbody></table></div>

<h2 id="split">Where the electricity goes</h2>
<p>The analyser splits each half hour's use at the base load. The three parts add up to the total:</p>
<ul><li><strong>Base load, 29%</strong> (22,606 kWh). What runs around the clock, whether anyone is in or not.</li><li><strong>Use above base load while open, 57%</strong> (45,062 kWh). The building in normal use: lights, heating, computers and kitchens during the working day.</li><li><strong>Closed-hours excess, 14%</strong> (11,035 kWh). Use above base load while the building should be closed. This is the place to start, because it usually costs little to fix.</li></ul>

<h2 id="findings">What the analyser found</h2>
<h3>1. Use while closed: £2,776 a year (high impact)</h3>
<p>Breaking this down by type of day is the most useful step, because each type usually has a different cause:</p>
<div class="table-wrap"><table><thead><tr><th>When</th><th class="num">Above base load</th></tr></thead><tbody>
<tr><td>Saturdays</td><td class="num">5,155 kWh</td></tr><tr><td>Weekday evenings and nights</td><td class="num">3,750 kWh</td></tr>
<tr><td>Bank holidays</td><td class="num">1,408 kWh</td></tr><tr><td>Sundays</td><td class="num">722 kWh</td></tr></tbody></table></div>
<p>Saturdays account for almost half. Sundays are quiet, so this isn't heating or ventilation running all weekend. The building is being used on some Saturdays. If that's planned, add Saturdays to the calendar and the figure falls. If it isn't, a Saturday booking or a few staff may be running the whole building.</p>

<h3>2. Seven bank holidays look like working days (medium impact)</h3>
<p>On seven bank holidays, including Christmas Day and Boxing Day, the office used at least 80% of a normal weekday's electricity. If the office was closed, the heating and ventilation schedules probably don't include bank holidays, which is very common. If it was open, the calendar needs updating.</p>

<h3>3. Early starts and late finishes: £629 a year (low impact)</h3>
<p>Demand rises before opening and stays high after closing. That's about 1,250 kWh a year above base load in the two hours before opening, and the same again in the two hours after closing. Timers and heating start-up settings are the usual cause, and they're quick to adjust.</p>

<h2 id="capacity">Supply capacity</h2>
<p>Assuming an agreed supply capacity of 40 kVA and a power factor of 0.95, the busiest half hour reaches 27 kVA, which is 67% of capacity. Keeping a 10% safety margin, the site could take about 9 kW of extra constant load. That's enough for modest EV charging, such as one 7 kW charger, but nowhere near enough for a heat pump to heat the whole building. See <a href="supply-capacity.html">supply capacity and kVA</a>.</p>

<h2 id="next-steps">What we'd do next</h2>
<ol><li><strong>Confirm the opening hours</strong>, including Saturdays. Every closed-hours figure depends on them.</li><li><strong>Check the heating and ventilation schedules</strong> for bank holidays and start times.</li><li><strong>Walk round the building on a Saturday</strong> to see what's switched on and who is using it.</li><li><strong>Look at the base load.</strong> 2.6 kW running all year is about 22,800 kWh, roughly £5,700 at 25p/kWh. See <a href="base-load.html">how to reduce it</a>.</li></ol>
<p>57% of this office's electricity is used during the working day, which is when solar panels generate. Our {SOLAR} estimates what a roof system would save.</p>
''',
  [('headline', 'The headline figures'), ('split', 'Where the electricity goes'), ('findings', 'What the analyser found'), ('capacity', 'Supply capacity'), ('next-steps', "What we'd do next")],
  [('Is this real data?', "No. We made up the office and its readings so we could show the method without using anyone's real data. Every figure is what the analyser reports for the example file."),
   ('How long does an analysis like this take?', 'Loading a year of data takes about a minute. Confirming the opening hours and reading the findings takes longer, and matters more.'),
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
  'Electricity used while a building should be closed is often the cheapest kind to cut. This guide explains how to find it in half-hourly data, what usually causes it, and who to involve in fixing it.',
  'How to find out-of-hours electricity use in half-hourly data, what usually causes it, and how to reduce it by changing timers and controls.',
  '''
<p class="answer">Out-of-hours use is electricity used while a building should be closed. To find it, compare each half hour with the opening hours and take away what always has to run (the base load). What's left is the closed-hours excess. It's usually the cheapest use to cut, because the fix is often a change to a timer or control setting.</p>

<h2 id="what">What counts as out-of-hours</h2>
<p>Any half hour outside opening hours counts: evenings, nights, weekends, bank holidays and closure periods. Some of this use is unavoidable. Servers, fridges, security systems and emergency lighting have to run all the time, and together they make up the <a href="base-load.html">base load</a>.</p>
<p>The figure to focus on is the <strong>excess</strong>, meaning use while closed above the base load. The analyser calls this the closed-hours excess and ranks sites by it, so you can see which buildings to look at first.</p>

<h2 id="find">How to find it</h2>
<ol><li><strong>Set the opening hours accurately.</strong> Every figure depends on them, so include bank holidays, closure weeks and any regular evening or weekend use.</li><li><strong>Look at the heatmap.</strong> It shows every half hour of the year on one chart. Opening hours appear as a dark band, and anything dark outside that band is out-of-hours use.</li><li><strong>Break it down by type of day.</strong> Weeknights, Saturdays, Sundays and bank holidays usually have different causes.</li><li><strong>Check the start and end of the day.</strong> If demand rises an hour or two before opening, or stays high after closing, timers or heating start-up settings are usually to blame.</li></ol>

<h2 id="causes">What usually causes it</h2>
<ul><li>Heating, ventilation and air conditioning running to the wrong schedule, or not set up for bank holidays</li><li>Lights left on, or on timers that no longer match how the building is used</li><li>A small evening or weekend booking that runs the whole building</li><li>Equipment left on manual override after maintenance, then forgotten</li><li>IT, catering and hot water equipment left on instead of being put on timers</li></ul>

<h2 id="cut">How to cut it</h2>
<p>Most fixes are changes to settings: building management system schedules, timers, holiday calendars and switch-off routines. Start with the biggest block of use, which is often weekends or a regular evening. Then check the half-hourly data a month later to see whether it worked. The analyser's before-and-after comparison is designed for this.</p>

<h2 id="who">Who to involve</h2>
<p>Fixes usually need two people working together: someone who can change the controls, such as your facilities team or building management system contractor, and someone who knows how the building is really used, such as a site manager or caretaker. Share the heatmap and the breakdown by type of day with both. It's much easier to agree a new schedule when everyone can see exactly when the building is using electricity.</p>
''',
  [('what', 'What counts as out-of-hours'), ('find', 'How to find it'), ('causes', 'What usually causes it'), ('cut', 'How to cut it'), ('who', 'Who to involve')],
  [('Is all out-of-hours use waste?', 'No. Some equipment has to run all the time. The part worth investigating is the excess, meaning use while closed above the base load.'),
   ('Why do opening hours matter so much?', "They decide which half hours count as closed. If a building is used on Saturdays but the calendar says it's closed, Saturday use shows up as out-of-hours. Confirm the hours before acting on the figures."),
   ('How quickly can I see whether a change worked?', "Within a few weeks. Compare the same days before and after the change using the analyser's before-and-after view.")],
  [('base-load.html', 'Base load', 'The other half of the picture: what always runs.'),
   ('example-office-analysis.html', 'Worked example', 'Out-of-hours use in one office, with figures.'),
   ('sectors.html', 'By sector', 'What normal looks like in schools, offices, leisure centres and more.')],
  'What out-of-hours electricity use is, how to find it in half-hourly data (opening hours, heatmap, day types, start and end of the day), common causes, fixes and who to involve.'))

# ── BASE LOAD ───────────────────────────────────────────────────────────
PAGES.append(guide_page(
  'base-load.html',
  'Base load electricity: what it is and how to cut it',
  'Base load: what never switches off',
  'Every building has a level of electricity use it never drops below. Because that use continues every hour of the year, even small reductions add up.',
  'What base load electricity is, how to measure it from half-hourly data, what makes it up, and how to reduce it. Each kilowatt running all year is 8,760 kWh.',
  '''
<p class="answer">Base load is the minimum electricity a building uses at all times, overnight and at weekends as well as during the day. Each kilowatt of base load runs for 8,760 hours a year. That's 8,760 kWh, or about £2,190 at 25p/kWh. You can measure it from half-hourly data, find out what makes it up, and switch off anything that doesn't need to run.</p>

<h2 id="measure">How to measure it</h2>
<p>The analyser takes every valid half-hourly reading, converts it to kW (the kWh reading divided by half an hour) and finds the level that demand stays above 95% of the time. This is called the 5th percentile, and it's what the analyser uses as the base load.</p>
<p>It doesn't use the single lowest reading, because one meter fault or power cut could set it and make the base load look lower than it really is. The analyser shows the lowest half hour alongside so you can compare.</p>

<h2 id="what">What makes it up</h2>
<ul><li>IT: servers, network equipment and phone systems</li><li>Refrigeration: kitchen fridges, freezers, vending machines and water coolers</li><li>Pumps and fans that run continuously</li><li>Water heaters and boilers kept on standby</li><li>Security systems, fire alarms and emergency lighting</li><li>Equipment left on standby, or left running by mistake</li></ul>

<h2 id="reduce">How to reduce it</h2>
<ol><li><strong>Walk round the building at night or at a weekend</strong> and note everything that's switched on. It's often a surprise.</li><li><strong>Sort what you find</strong> into must run, could run less, and shouldn't be on.</li><li><strong>Fix the easy ones first</strong>, such as timers on water heaters and vending machines, switch-off routines and combining servers.</li><li><strong>Check the base load every month.</strong> A step up usually means new equipment has been installed or something has been left on. The analyser flags lasting changes like this.</li></ol>

<h2 id="worth">Working out the saving</h2>
<p>Because base load runs every hour of the year, savings are easy to estimate: multiply the kilowatts you remove by 8,760 hours and by your unit rate. At 25p/kWh, 1 kW is worth about £2,190 a year, and switching off a 0.5 kW water heater that was left on all the time saves about £1,100.</p>
''',
  [('measure', 'How to measure it'), ('what', 'What makes it up'), ('reduce', 'How to reduce it'), ('worth', 'Working out the saving')],
  [('What is a typical base load?', 'It depends on the building. An office with a lot of IT, or a site with refrigeration, will have a much higher base load than a school. Compare each site with its own history, and with similar buildings in your estate.'),
   ('Why is my base load higher at weekends than overnight on weekdays?', "It shouldn't be. If it is, something is switching on at weekends, such as frost protection on the heating, a scheduled process or a booking. Check the weekend pattern on the heatmap."),
   ('How much does 1 kW of base load cost?', "It runs 8,760 hours a year, so it uses 8,760 kWh. At 25p/kWh that's about £2,190 a year. Multiply 8,760 by your own rate to check.")],
  [('out-of-hours-electricity.html', 'Out-of-hours use', 'Use above the base load while the building is closed.'),
   ('supply-capacity.html', 'Supply capacity', 'The other end of the scale: your busiest half hours.'),
   ('example-office-analysis.html', 'Worked example', 'Base load in one office, with figures.')],
  'What base load is, how to measure it from half-hourly data (5th percentile, not the minimum), what makes it up, how to reduce it; 1 kW all year is 8,760 kWh.'))

# ── SUPPLY CAPACITY ─────────────────────────────────────────────────────
PAGES.append(guide_page(
  'supply-capacity.html',
  'Supply capacity and kVA: room for heat pumps and EVs',
  'Supply capacity and kVA',
  'Before adding heat pumps, EV chargers or other new equipment, check how close your busiest half hours already come to your agreed supply capacity.',
  'Agreed supply capacity explained: kW to kVA, comparing half-hourly peaks with capacity, and room for heat pumps and EV charging.',
  '''
<p class="answer">Your agreed supply capacity is the maximum demand your electricity connection is set up for, measured in kVA. To see how much room you have, convert your busiest half hours from kW to kVA (divide by the power factor) and compare them with the agreed capacity. The gap is your headroom for new equipment such as heat pumps and EV chargers.</p>

''' + photo('plant-outside', 'Two engineers with a tablet beside packaged plant, flues and pipework outside a large building', "New equipment such as heat pumps has to fit within the site's supply. Half-hourly data shows how close the busiest periods already come to it.") + '''
<h2 id="what">What agreed supply capacity is</h2>
<p>Larger electricity supplies have an agreed capacity, sometimes called authorised or available capacity. It's set in the connection agreement and usually shown on the bill in kVA. You normally pay a daily charge for it whether you use it or not. If you go over it you may face extra charges, and the network operator may ask you to increase it.</p>

<h2 id="kva">kW and kVA</h2>
<p>Meters measure energy in kWh. Half-hourly data gives the average power in each half hour, in kW. Capacity is set in kVA, which also includes reactive power: power drawn by equipment such as motors that doesn't do useful work. The two are linked by the power factor:</p>
<div class="note"><strong>kVA = kW ÷ power factor.</strong> At a power factor of 0.95, a 95 kW peak is 100 kVA. If your bill includes reactive power charges, your power factor is probably below 0.95.</div>

<h2 id="headroom">Working out headroom</h2>
<ol><li><strong>Find your busiest half hours</strong> over at least a year, so winter peaks are included.</li><li><strong>Convert them to kVA</strong> using your power factor.</li><li><strong>Keep a safety margin</strong>, for example 10%, below the agreed capacity.</li><li><strong>Your headroom</strong> is the largest constant extra load you could add without going over that margin in any half hour.</li></ol>
<p>Half-hourly readings are averages, so they smooth out very short spikes. Treat this as an early check, and confirm with your network operator before relying on it.</p>

<h2 id="new-load">Heat pumps and EV charging</h2>
<p>A heat pump uses much less electricity than the heat it produces. With a coefficient of performance (COP) of 3, a heat pump producing 150 kW of heat draws about 50 kW of electricity. It works hardest in winter, which is usually when a building's peaks are highest, so the two add together. EV charging is different: if it happens overnight, it falls when most sites are quietest. The analyser lets you test a new load at a chosen time of day and season against your actual half-hourly peaks.</p>
''',
  [('what', 'What agreed supply capacity is'), ('kva', 'kW and kVA'), ('headroom', 'Working out headroom'), ('new-load', 'Heat pumps and EV charging')],
  [('Where do I find my agreed supply capacity?', 'On your electricity bill or connection agreement, in kVA. Your supplier can confirm it.'),
   ('What power factor should I use?', "If you don't know it, 0.95 is a reasonable starting assumption. It's probably lower if your bill shows reactive power charges."),
   ('Is half-hourly data enough to plan a new connection?', "It's a good first check, but half-hour averages hide very short peaks. For a significant new load, speak to your network operator before committing.")],
  [('base-load.html', 'Base load', 'The demand that never goes away.'),
   ('example-office-analysis.html', 'Worked example', 'Peaks against capacity in one office.'),
   ('how-it-works.html', 'How the analyser works', 'Including how headroom is worked out.')],
  'Agreed supply capacity in kVA, kW to kVA via power factor, headroom from half-hourly peaks with a safety margin, and checking heat pumps and EV charging.'))

# ── WORKED EXAMPLE: SCHOOL ──────────────────────────────────────────────
PAGES.append(guide_page(
  'example-school-analysis.html',
  'Worked example: a primary school\'s half-hourly data',
  'Worked example: one primary school',
  'We ran a year of half-hourly data from a primary school through the analyser, after entering its term dates. The school is made up, but every figure is what the analyser reports.',
  'A primary school\'s year of half-hourly data: heating left on through half term, evening lettings, and what the analyser found once term dates were entered.',
  '''
<p class="answer">With its term dates entered, this school used 31% of its electricity while closed. That's about £1,260 a year above what always runs, at 25p/kWh. The biggest single issue was October half term, when the empty building used more than twice what it should have.</p>

<div class="note"><strong>Made-up data.</strong> <a href="samples/example-school.csv" download>Download the file</a> and load it into the <a href="analyser/">analyser</a> to follow along. Set the building type to School and enter the term dates below as closures.</div>

<h2 id="setup">Setting it up</h2>
<p>The analyser never assumes school holidays, because they vary between schools and from year to year. You enter them. For this school:</p>
<ul><li>Building type: School (open 07:00 to 17:30 on weekdays)</li><li>Six closures: Easter, May half term, summer, October half term, Christmas and February half term</li><li>Hours marked as confirmed</li></ul>
<p>Without the term dates, holiday weeks would be treated as normal school days, and heating left on during a holiday would look like normal use.</p>

<h2 id="headline">The headline figures</h2>
<div class="table-wrap"><table><thead><tr><th>Measure</th><th class="num">Value</th></tr></thead><tbody>
<tr><td>Electricity a year</td><td class="num">57,753 kWh</td></tr><tr><td>Energy cost a year (25p/kWh)</td><td class="num">£14,438</td></tr>
<tr><td>Base load</td><td class="num">1.9 kW</td></tr><tr><td>Busiest half hour</td><td class="num">30.1 kW</td></tr>
<tr><td>Use while closed</td><td class="num">31%</td></tr><tr><td>Closed-hours excess</td><td class="num">£1,261 a year</td></tr></tbody></table></div>

<h2 id="heatmap">The year at a glance</h2>
<figure class="figure"><img src="images/heatmap-school.png" width="2464" height="896" alt="Heatmap of a school year: dark blocks in term time, blank holidays, a pale block across October half term and thin stripes on Tuesday and Thursday evenings" loading="lazy"><figcaption>One column per day and one row per half hour. Term weeks are dark and holidays should be blank, but October half term isn't.</figcaption></figure>
<p>Two things stand out: a pale block across all of October half term, and thin stripes after 18:00 on two evenings a week during term. See <a href="reading-a-heatmap.html">how to read a heatmap</a>.</p>

<h2 id="findings">What the analyser found</h2>
<h3>1. Heating left on through October half term</h3>
<p>The three days with the most out-of-hours use all fell in half term, each about 100 kWh above base load. The analyser flagged a lasting change: from 25 October, demand was at least 15% above its expected level on five of nine days, and on average more than double. The pattern (07:00 to 17:00 on weekdays, with nobody in) suggests the heating and ventilation stayed on their term-time schedule. It's a common problem in schools: the building controls know about the long holidays but not the half terms.</p>
<h3>2. Evening lettings</h3>
<p>Weekday evenings make up the largest share of the closed-hours excess, at 2,765 kWh above base load. The stripes on Tuesday and Thursday evenings are a regular hall letting. Lettings are fine, and often bring in useful income, but they should be entered in the calendar as open hours. It's also worth checking whether a hall booking is lighting and heating more of the building than it needs.</p>
<h3>3. Holidays and weekends</h3>
<p>The holidays added 1,157 kWh above base load, most of it in October. Saturdays and Sundays were close to base load (556 kWh and 526 kWh above it over the year), which is what you'd expect.</p>

<h2 id="next-steps">What we'd do next</h2>
<ol><li><strong>Add the full holiday calendar to the building management system</strong>, so heating and ventilation switch off for half terms as well as the long holidays.</li><li><strong>Add the lettings to the analyser's calendar</strong>, then check what the hall booking switches on.</li><li><strong>Check the next half term</strong> using the analyser's before-and-after comparison, to see whether the fix worked.</li></ol>
''',
  [('setup', 'Setting it up'), ('headline', 'The headline figures'), ('heatmap', 'The year at a glance'), ('findings', 'What the analyser found'), ('next-steps', "What we'd do next")],
  [('Do I have to enter term dates?', 'Yes. The analyser never assumes them, because they vary between schools and from year to year. Enter them as closures. Without them, holiday weeks count as normal school days.'),
   ('Should a school use nothing in the holidays?', 'No. The base load carries on (IT, fridges, security). Holiday use above the base load is what to look at.'),
   ('Is this real data?', "No. We made up the school and its readings so we could show the method without using anyone's real data.")],
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
<p class="answer">A half-hourly heatmap has one column for each day and one row for each half hour, with darker colours for higher demand. Normal use shows as a dark band during opening hours. Anything dark outside that band, such as at night, at weekends or in holidays, is worth checking.</p>

<h2 id="axes">What you're looking at</h2>
<ul><li><strong>Across:</strong> days, from the start of the period to the end.</li><li><strong>Down:</strong> time of day, from midnight at the top to midnight at the bottom.</li><li><strong>Colour:</strong> demand in that half hour, from pale (low) to dark (high).</li></ul>
<p>A year contains about 17,500 half hours. That's far too many numbers to read in a table, but the heatmap shows them all at once, which is why it's often the quickest way to understand a building.</p>

<figure class="figure"><img src="images/heatmap-office.png" width="2464" height="896" alt="Heatmap of an office year: a dark weekday band, pale nights, and weekends that are sometimes busy" loading="lazy"><figcaption>An office (made-up data). The weekday band is clear, and some Saturdays are as busy as weekdays.</figcaption></figure>

<h2 id="normal">What normal looks like</h2>
<p>For a building used on weekdays, you'd expect a dark horizontal band during working hours, regular pale gaps at weekends, and pale nights. Winter is often slightly darker than summer. The edges of the band show when the building actually starts and stops using electricity each day, which isn't always when the doors open and close.</p>

<h2 id="patterns">Patterns worth checking</h2>
<div class="table-wrap"><table><thead><tr><th>What you see</th><th>What it usually means</th></tr></thead><tbody>
<tr><td>A pale block where it should be blank, such as a holiday week</td><td>Heating or ventilation running to the normal schedule with nobody in</td></tr>
<tr><td>Thin stripes in the evening on the same weekdays</td><td>Regular evening use, such as lettings, classes or cleaning</td></tr>
<tr><td>The dark band starting well before opening</td><td>Heating or ventilation set to start too early</td></tr>
<tr><td>Nights that get darker from a certain date</td><td>New equipment, or something left on, has raised the base load</td></tr>
<tr><td>A single dark column</td><td>One unusual day, such as an event, a fault or a reading error</td></tr>
<tr><td>Grey or striped gaps</td><td>Missing data (not zero use)</td></tr></tbody></table></div>

<figure class="figure"><img src="images/heatmap-school.png" width="2464" height="896" alt="Heatmap of a school year showing term blocks, holidays, a pale half-term block and evening stripes" loading="lazy"><figcaption>A primary school (made-up data). The pale block in late October is heating left on through half term, and the stripes after 18:00 are evening lettings. See the <a href="example-school-analysis.html">worked example</a>.</figcaption></figure>

<h2 id="next">Putting a cost on what you see</h2>
<p>The heatmap shows you where to look, and the figures tell you how much it matters. In the analyser, click any day to compare its half hours with a typical day. Then use the out-of-hours and unusual-day findings to put a cost on what you've spotted.</p>
''',
  [('axes', "What you're looking at"), ('normal', 'What normal looks like'), ('patterns', 'Patterns worth checking'), ('next', 'Putting a cost on what you see')],
  [('What is a carpet plot?', 'Another name for the same chart: one column per day and one row per half hour, coloured by demand.'),
   ('Why are some days grey?', "They have no valid readings. Missing data is shown as missing rather than as zero, so gaps don't look as if the building was switched off."),
   ('Can I see one day in detail?', 'Yes. In the analyser, click any day on the heatmap to compare its half hours with a typical day of the same kind.')],
  [('example-school-analysis.html', 'Worked example: school', 'The school heatmap, explained finding by finding.'),
   ('out-of-hours-electricity.html', 'Out-of-hours use', 'Putting a cost on what the heatmap shows.'),
   ('glossary.html', 'Glossary', 'The terms used in these guides.')],
  'How to read a half-hourly heatmap (days across, time of day down, colour for demand) and the patterns that point to waste.'))

# ── PROVING A SAVING ────────────────────────────────────────────────────
PAGES.append(guide_page(
  'proving-savings.html',
  'How to prove an energy saving worked, with half-hourly data',
  'Proving a saving worked',
  "You've changed a setting or replaced some equipment. Half-hourly data can show whether it made a difference, as long as you compare like with like.",
  'How to use half-hourly data to show whether a change saved energy: matched before-and-after periods, the right measure, and what can mislead.',
  '''
<p class="answer">Compare a period before the change with a matching period after it. Use the same days of the week, the same types of day (open, closed, holiday) and enough weeks to even out day-to-day variation. Then look at the part of demand the change should affect, such as base load or out-of-hours use, rather than the total bill.</p>

''' + photo('board-review', 'A team reviewing charts and printed reports around a meeting table, with solar panels and battery units outside the window', 'A saving is easier to sign off when the before-and-after comparison is fair.') + '''
<h2 id="match">Compare like with like</h2>
<ul><li><strong>Compare the same types of day.</strong> Compare weekdays with weekdays and holidays with holidays. A before period with several bank holidays in it will make the after period look better or worse than it really is.</li><li><strong>Use enough data.</strong> Four to eight weeks either side is usually enough to show a real change. A single week can be thrown off by one unusual day.</li><li><strong>Keep the periods close together.</strong> The closer they are, the less the weather and the seasons get in the way.</li><li><strong>Leave out the change itself.</strong> Skip the days when the work was being carried out.</li></ul>

<h2 id="measure">Measure the right thing</h2>
<p>Choose the measure the change should affect:</p>
<div class="table-wrap"><table><thead><tr><th>Change</th><th>Look at</th></tr></thead><tbody>
<tr><td>Heating or ventilation schedules</td><td>Out-of-hours use, and demand around opening and closing</td></tr>
<tr><td>Switching off equipment overnight</td><td>Base load</td></tr>
<tr><td>LED lighting</td><td>Demand during opening hours</td></tr>
<tr><td>Holiday settings in the building controls</td><td>Use during closures</td></tr></tbody></table></div>
<p>Total consumption mixes the effect of your change with everything else that happened, such as changes in occupancy, the weather or new equipment. A genuine saving can get lost in it, and so can a change that didn't work.</p>

<h2 id="weather">Weather and seasons</h2>
<p>Electric heating and cooling depend on the weather. If the period before the change was colder than the period after, some of the drop is down to the weather. For heating changes, compare the same weeks a year apart as a cross-check, or adjust for weather using degree days if you have them.</p>

<h2 id="analyser">In the analyser</h2>
<ul><li><strong>Did a change make a difference?</strong> on the Base load tab compares matched weeks either side of a date you choose.</li><li><strong>Compare periods</strong> on the Heatmap tab shows any two periods side by side.</li><li><strong>Persistent changes</strong> on the Unusual days tab flags lasting shifts automatically, so you can check whether a change shows up when you'd expect.</li></ul>
<p>If you need a formal measurement and verification of savings, for example for a funded project or an energy performance contract, the International Performance Measurement and Verification Protocol (IPMVP) sets out recognised methods.</p>
''',
  [('match', 'Compare like with like'), ('measure', 'Measure the right thing'), ('weather', 'Weather and seasons'), ('analyser', 'In the analyser')],
  [('How long should I wait before checking?', 'Four to eight weeks of data after the change, compared with the same length of time before it, is usually enough to see a real change.'),
   ('Why has our bill not gone down?', 'A saving in one place can be hidden by changes elsewhere, such as occupancy, weather, prices or new equipment. Compare the specific measure the change should affect.'),
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
  "Britain is moving every electricity meter onto half-hourly settlement. Here's what that means for businesses and public sector organisations, and why it makes your half-hourly data more useful.",
  'What market-wide half-hourly settlement (MHHS) is, the timetable to 2027, who runs it, and what it means for business and public sector electricity customers.',
  '''
<p class="answer">Market-wide half-hourly settlement (MHHS) means suppliers will be charged for the electricity their customers actually use in each half hour, instead of an estimate based on standard usage profiles. The move began in October 2025 and is due to finish in May 2027. If you have a smart or advanced meter, your half-hourly readings become part of how your electricity is settled, so it's worth asking your supplier for them.</p>

''' + photo('site-plans-substation', 'Four people in hard hats and high-visibility vests reviewing site plans next to a substation and solar panels') + '''
<h2 id="what">What it is</h2>
<p>Large sites have been settled half-hourly for years. Most smaller sites have been settled using standard profiles, which are estimates of when a typical customer uses electricity. MHHS replaces those estimates with actual half-hourly readings wherever a meter can provide them.<sup><a href="#sources">1</a></sup></p>
<p>The programme's stated objective is "to maximise the opportunities provided by smart metering by developing and implementing an enduring process for MHHS, that delivers benefits for consumers and enables a smart, flexible energy system."<sup><a href="#sources">2</a></sup></p>

<h2 id="who">Who runs it</h2>
<p>Ofgem decided to go ahead with MHHS on 20 April 2021.<sup><a href="#sources">1</a></sup> Ofgem is the programme sponsor and appointed Elexon as Senior Responsible Owner and Implementation Manager. Delivery is led by the energy industry.<sup><a href="#sources">2</a></sup></p>

<h2 id="timeline">The timetable</h2>
<div class="table-wrap"><table><thead><tr><th>Date</th><th>Milestone</th></tr></thead><tbody>
<tr><td>20 April 2021</td><td>Ofgem decision to introduce MHHS (originally planned to finish in October 2025)</td></tr>
<tr><td>21 October 2025</td><td>Migration to the new arrangements began, for all meter types</td></tr>
<tr><td>7 May 2027</td><td>Migration due to be complete, with all energy settled under the new arrangements</td></tr>
<tr><td>2 July 2027</td><td>Settlement moves from a 14-month to a four-month timetable</td></tr></tbody></table></div>
<p>Dates as published by Ofgem and the MHHS programme in November 2026. Check the programme's milestone page for the latest.<sup><a href="#sources">1, 3</a></sup></p>

<h2 id="you">What it means for your organisation</h2>
<ul><li><strong>You don't need to do anything to be moved across.</strong> Your supplier handles it.</li><li><strong>Microbusinesses can't opt out.</strong> Ofgem's decision says half-hourly data will be processed for settlement for domestic customers unless they opt out, and that microbusiness customers will not be able to opt out.<sup><a href="#sources">1</a></sup></li><li><strong>Tariffs may change.</strong> Ofgem expects MHHS to encourage suppliers to offer tariffs that reward using electricity at cheaper times of day, known as time-of-use tariffs.<sup><a href="#sources">1</a></sup></li><li><strong>Half-hourly data becomes standard.</strong> If your meter records half-hourly readings, your supplier uses them. Ask for a copy and you can see exactly when your sites use electricity.</li></ul>
<p>Under half-hourly settlement and time-of-use tariffs, the time of day you use electricity will matter more. Understanding your half-hourly pattern now, including what runs overnight and at weekends, will help you choose a suitable tariff and reduce costs.</p>
''' + sources([
    ('Ofgem: Electricity Retail Market-wide Half-hourly Settlement: Decision and Full Business Case (20 April 2021)', 'https://www.ofgem.gov.uk/decision/electricity-retail-market-wide-half-hourly-settlement-decision-and-full-business-case'),
    ('MHHS Programme: Programme overview', 'https://www.mhhsprogramme.co.uk/programme-information/programme-overview'),
    ('MHHS Programme: Key programme milestones', 'https://www.mhhsprogramme.co.uk/programme-information/key-programme-milestones')]),
  [('what', 'What it is'), ('who', 'Who runs it'), ('timeline', 'The timetable'), ('you', 'What it means for your organisation')],
  [('When does market-wide half-hourly settlement finish?', "Migration is due to be complete on 7 May 2027, with the move to a four-month settlement timetable on 2 July 2027, according to the MHHS programme's published milestones."),
   ('Do I need to do anything?', 'No. Your supplier moves your meters across. It is worth asking them for your half-hourly data, so you can see when your sites use electricity.'),
   ('Can a business opt out of half-hourly data collection?', "Ofgem's 2021 decision says microbusiness customers will not be able to opt out of their half-hourly data being processed for settlement. Domestic customers can opt out.")],
  [('get-your-data.html', 'Getting your data', 'What to ask your supplier for.'),
   ('glossary.html', 'Glossary', 'Settlement, MPAN, kVA and other terms.'),
   ('out-of-hours-electricity.html', 'Out-of-hours use', 'The first thing to look at in your data.')],
  'Market-wide half-hourly settlement: Ofgem decision 20 April 2021; migration began 21 October 2025, due complete 7 May 2027; four-month settlement timetable from 2 July 2027; microbusinesses cannot opt out.'))

# ── GLOSSARY ────────────────────────────────────────────────────────────
GLOSSARY = [
  ('Agreed supply capacity', 'The maximum demand, in kVA, an electricity connection is set up for. It appears on larger electricity bills and is also called authorised or available capacity. <a href="supply-capacity.html">More</a>.'),
  ('Annualised figure', 'A yearly figure scaled up from the valid readings available. It is used when the data covers less than a full year or has gaps.'),
  ('Base load', 'The level of demand a building rarely drops below: what never switches off. The analyser measures it as the 5th percentile of half-hourly demand. <a href="base-load.html">More</a>.'),
  ('Closed-hours excess', 'Electricity used while a building should be closed, above its base load. The analyser ranks sites by it. <a href="out-of-hours-electricity.html">More</a>.'),
  ('Coverage', 'The share of expected half-hourly readings that are present and valid.'),
  ('Degree days', 'A measure of how cold (heating degree days) or warm (cooling degree days) a period was. Used to compare energy use across periods with different weather.'),
  ('DNO', "Distribution network operator. The company that runs the local electricity network and your site's connection to it. The first two digits of your MPAN show which one. <a href=\"mpan-profile-class.html#bottom\">More</a>."),
  ('Half-hourly (HH) data', 'A record of the electricity used in every half hour: 48 readings a day.'),
  ('Heatmap', 'A chart of every half hour in a period, with one column per day and one row per half hour, coloured by demand. Also called a carpet plot. <a href="reading-a-heatmap.html">More</a>.'),
  ('kVA', 'Kilovolt-ampere. A measure of apparent power, and the unit supply capacity is set in. kVA = kW ÷ power factor.'),
  ('kW', 'Kilowatt. A measure of power: the rate electricity is being used at a given moment. Divide a half-hourly reading in kWh by 0.5 to get the average kW for that half hour.'),
  ('kWh', 'Kilowatt-hour. A measure of energy, and what you are billed for. Using 1 kW for one hour is 1 kWh.'),
  ('Load factor', 'Average demand divided by peak demand. A low load factor means demand has short, high peaks.'),
  ('Market-wide half-hourly settlement (MHHS)', 'The move to settle every electricity meter in Great Britain using half-hourly data. <a href="half-hourly-settlement.html">More</a>.'),
  ('MPAN', 'Meter point administration number. The 13-digit number on the bottom line of the supply number on an electricity bill. It identifies the supply point. <a href="mpan-profile-class.html">More</a>.'),
  ('Peak demand', 'The highest half-hourly average demand in a period, usually in kW or kVA.'),
  ('Power factor', 'The ratio of real power (kW) to apparent power (kVA), between 0 and 1. Equipment such as motors lowers it.'),
  ('Profile class', 'The first two digits of the top line of the supply number. 00 means the supply is settled half-hourly; 01 to 08 mean use is estimated from standard profiles. <a href="mpan-profile-class.html#top">More</a>.'),
  ('Settlement', "The process that works out how much electricity each supplier's customers used, and when, so suppliers pay the right amount for it."),
  ('Time-of-use tariff', 'A tariff with different unit rates at different times of day, such as day and night rates.'),
]
NAV_PARENT['glossary.html'] = 'guides.html'
PAGES.append(Page(
  'glossary.html', 'Glossary of half-hourly electricity terms',
  'Simple definitions of half-hourly electricity terms: base load, kW, kWh, kVA, power factor, MPAN, agreed supply capacity, settlement and more.',
  page_hero('Guide', 'Glossary', 'Simple definitions of the terms used in half-hourly electricity data and on this site.',
            crumbs=[HOME, GUIDES, ('Glossary', 'glossary.html')])
  + guide(updated_line() + '<p class="answer">Half-hourly (HH) data is a record of the electricity a meter measures in every half hour: 48 readings a day, usually in kWh. The terms you will meet most often are kWh (energy, what you are billed for), kW (how fast electricity is being used at a given moment), base load (the demand that never switches off) and kVA (the unit your supply capacity is set in).</p>'
          + '<dl class="glossary">' + ''.join(
      f'<div id="{t.lower().split(" (")[0].replace(" ", "-")}"><dt>{t}</dt><dd>{d}</dd></div>' for t, d in GLOSSARY) + '</dl>')
  + cta('See the terms in your own data', "It's free, there's no sign-up, and nothing is uploaded."),
  crumbs=[HOME, GUIDES, ('Glossary', 'glossary.html')], article=True, section='Guides',
  summary='Definitions: base load, closed-hours excess, kW, kWh, kVA, power factor, MPAN, agreed supply capacity, settlement, MHHS, heatmap, load factor and more.',
  schema=[{'@type': 'DefinedTermSet', 'name': 'Half-hourly electricity glossary', 'hasDefinedTerm': [
      {'@type': 'DefinedTerm', 'name': t, 'description': strip_tags(d).replace(' More.', '')} for t, d in GLOSSARY]}]))

# ── SECTORS ─────────────────────────────────────────────────────────────
SECTOR_DATA = [
  ('schools-electricity.html', 'Schools and colleges', 'Electricity use in schools and colleges',
   "Schools are closed for about 13 weeks a year, so holidays and weekends should show very little use. When they don't, a schedule usually needs fixing.",
   'During holidays, weekends and evenings, use should be close to the base load. Schools differ from offices mainly in the length of their holidays, so enter the term dates in the calendar before anything else.',
   ['Heating and ventilation running through holidays, especially half terms', 'IT suites, servers and interactive screens left on overnight', 'Kitchen equipment and water heaters left on during holidays', 'Evening lettings that run the whole building for one hall or pitch', 'Pool or sports hall equipment on the same schedule as the main building'],
   'Enter each holiday as a closure, and any regular evening lettings as open hours. The out-of-hours figures will then reflect what the school can actually control.',
   [('Should holiday use be zero?', 'No. The base load carries on (IT, fridges, security). Holiday use above the base load is what to look at.'),
    ('How do I handle evening lettings?', "Enter them in the calendar as open hours so they don't count as out-of-hours use. Then check whether the letting really needs the whole building heated and lit.")]),
  ('offices-council-buildings.html', 'Offices and council buildings', 'Electricity use in offices and council buildings',
   'Office electricity use should drop sharply when people go home. Whatever carries on running is worth investigating.',
   'You should see a clear weekday pattern, with demand falling to the base load in the evening and at weekends. Hybrid working has made many offices quieter on Mondays and Fridays, but heating, ventilation and lighting often still run as if every desk were full.',
   ['Air handling and cooling running all night or all weekend', 'Heating or cooling starting well before staff arrive', 'Whole floors lit for a cleaner or one person working late', 'Server rooms and comms cupboards with their own cooling', 'Council buildings used for evening meetings or elections, which need adding to the calendar'],
   'If Mondays and Fridays are quieter, set different hours for each day of the week. Also add bank holidays, which many building schedules miss.',
   [('Why does our office use so much at weekends?', 'Usually heating, ventilation or cooling running to the wrong schedule, or a weekend activity using the whole building. The breakdown by type of day shows which.'),
    ('Has hybrid working changed what to look for?', 'Yes. Compare quiet weekdays with busy ones. If demand barely changes, equipment is running to a full-occupancy schedule.')]),
  ('leisure-centres.html', 'Leisure centres and pools', 'Electricity use in leisure centres and pools',
   'Long opening hours and pools that run around the clock make leisure centres heavy electricity users. Start by understanding what makes up the overnight use.',
   'Expect a high base load from pool pumps, ventilation and dehumidification, with opening hours from early morning to late evening, seven days a week.',
   ['Pool hall ventilation and dehumidification running at daytime levels overnight', 'Filtration pumps that could run more slowly outside opening hours', 'Sports hall and studio lighting left on between bookings', 'Saunas, steam rooms and water heaters switched on earlier than needed', 'Equipment that kept running while the centre was closed for maintenance'],
   'Opening hours vary by day and change during school holidays, so enter them carefully. A centre open 14 hours a day has a short closed period, and small changes to settings in that period make a big difference.',
   [('Is a high base load normal for a pool?', 'Yes. Pool equipment has to run continuously. What matters is whether it runs harder than needed outside opening hours, for example ventilation at full speed overnight.'),
    ('What should I look at first?', 'Overnight use, and how quickly demand falls after closing. Pool covers and slower overnight ventilation and filtration are common places to start.')]),
  ('healthcare-electricity.html', 'Healthcare', 'Electricity use in healthcare buildings',
   'Hospitals and many care settings run 24 hours a day, so out-of-hours use is less relevant. Comparing day with night, and peaks with supply capacity, tells you more.',
   'Expect continuous use with a rise during the day. Clinics, surgeries and offices on the same estate keep office hours and should be treated like offices.',
   ['Night-time use in non-clinical areas that is close to daytime use', 'Weekend use in outpatient and administrative buildings', 'Peaks already close to supply capacity, before electric heating or EV charging is added', 'Steps up in base load after new equipment or a refurbishment', 'Sub-meters for different buildings or wings, if you have them'],
   'Set 24-hour buildings as always open, so the analysis focuses on base load, peaks and changes over time. Give clinics and offices their actual opening hours.',
   [('Can out-of-hours analysis work for a hospital?', 'For the main 24-hour building, compare day with night and track the base load instead. For clinics and offices on the estate, out-of-hours analysis works as it does for any office.'),
    ('Why does supply capacity matter so much in healthcare?', 'Replacing gas heating with heat pumps adds a large electrical load in winter. Check how close your winter peaks already come to the agreed capacity first.')]),
  ('industrial-warehouses.html', 'Industrial and warehouses', 'Electricity use in industrial sites and warehouses',
   "With shift work, getting the calendar right matters more than anything. Once it's set, use during shutdowns, compressed air leaks and refrigeration are easy to see.",
   'Demand follows the shift pattern, stepping up when a shift starts and down when it ends. During planned shutdowns, use should fall close to the base load.',
   ['Compressed air left on overnight and at weekends (leaks show as a steady load once production stops)', 'Refrigeration and chillers working harder than they need to', 'Shutdown weeks where use never gets close to the base load', 'Lighting in high-bay warehouses left on outside shift times', 'Peaks compared with capacity, before adding EV charging for vans or forklifts'],
   'Enter shift times, including night shifts, and planned shutdowns, so the analysis can separate production from everything else.',
   [('How do I spot compressed air leaks?', 'Look at demand after production has stopped. If the compressors keep running with nothing using air, the steady load is often leaks.'),
    ('Can the analyser handle night shifts?', 'Yes. Opening hours can run past midnight, and each day of the week can have different hours.')]),
  ('retail-hospitality.html', 'Retail and hospitality', 'Electricity use in retail and hospitality',
   'Fixed trading hours make out-of-hours use easy to spot. Refrigeration, signs and kitchen equipment are the most common causes.',
   'Demand follows trading hours, with some use for preparation before opening and cleaning after closing. In food retail and hospitality, refrigeration means a high base load.',
   ['Fridges and display cases without night blinds or covers', 'Signs and display lighting on timers that run all night', 'Kitchen extraction and equipment switched on long before service', 'Heating and cooling still on an old schedule after trading hours changed', 'Seasonal hours that were never updated in the building controls'],
   'Include preparation and cleaning time in the opening hours, so the out-of-hours figure only shows use that could be avoided.',
   [('Why is our base load so high?', "In food retail and hospitality it's mostly refrigeration. Check night blinds, door seals and temperature settings first."),
    ('How do I compare several shops or venues?', 'Load one file for each meter. The analyser ranks sites by closed-hours excess and lets you compare your estate by building type.')]),
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
<p>Use these as a starting point. Each site is compared with its own calendar, so getting the hours right matters more than the type of building.</p>
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
            crumbs=[HOME, SECTORS], image='sectors') +
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
    ('out-of-hours-electricity.html', 'Out-of-hours electricity use', 'How to find use while the building is closed, reduce it, and who to involve.'),
    ('base-load.html', 'Base load', 'What always runs, how to measure it and how to reduce it.'),
    ('supply-capacity.html', 'Supply capacity and kVA', 'Room for heat pumps, EV charging and other new equipment.'),
    ('proving-savings.html', 'Proving a saving worked', 'How to compare before and after fairly.'),
    ('half-hourly-settlement.html', 'Half-hourly settlement (MHHS) explained', 'What the move to half-hourly settlement means, and the timetable to 2027.'),
    ('mpan-profile-class.html', 'Reading your MPAN', 'Profile class, network region and what half-hourly settlement changes.'),
    ('electricity-benchmarks.html', 'Electricity benchmarks by sector', 'Typical kWh per m² for offices, shops, schools and more.'),
    ('glossary.html', 'Glossary', 'kW, kWh, kVA, base load, MPAN and other terms.'),
    ('how-it-works.html', 'How the analyser works', 'Each step, from reading your file to the report.'),
]
NAV_PARENT['get-your-data.html'] = 'guides.html'
PAGES.append(Page(
  'guides.html', 'Guides to half-hourly electricity data | Half Hourly Insights',
  'Simple guides to half-hourly electricity data: getting it, out-of-hours use, base load, supply capacity and worked examples.',
  page_hero('Guides', 'Guides to half-hourly data', 'Clear answers to the questions people ask when they first look at half-hourly electricity data.',
            crumbs=[HOME, GUIDES], image='guides') +
  '<section class="section"><div class="section-inner"><div class="link-grid">' +
  ''.join(link_card(f, t, d) for f, t, d in GUIDE_LIST) +
  '</div><p class="note" style="margin-top:32px">Looking for your sector? See <a href="sectors.html" style="color:var(--blue);text-decoration:underline">what to look for by sector</a>.</p></div></section>'
  + cta('Ready to look at your own data?', "It's free, there's no sign-up, and nothing is uploaded."),
  crumbs=[HOME, GUIDES], section='Guides', summary='Index of guides.'))
