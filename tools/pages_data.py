"""
Practical data guides: getting half-hourly data from named suppliers, reading
the MPAN, and electricity benchmarks by sector.

Supplier pages summarise only what each supplier says on its own public
pages, checked on the date in CHECKED. Every claim carries a numbered source.
They change: re-check each page and its sources at least once a year, and
whenever a reader reports a difference.
"""
from kit import long_date, sources
from pages_guides import GUIDES, HOME, guide_page

CHECKED = '2026-11-14'   # when the supplier pages' sources were last read


def ref(*n):
    return f'<sup><a href="#sources">{",".join(str(x) for x in n)}</a></sup>'


GOV_OFFER = ('Department for Business, Energy and Industrial Strategy: Maximising non-domestic smart meter consumer benefits, '
             'supporting industry guidance (June 2022)',
             'https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1080384/'
             'maximising-non-domestic-smart-meter-data-offer-industry-guidance.pdf')


def your_right(n):
    """The government's on-request data offer, cited as source n."""
    return f'''
<h2 id="right">Your right to the data</h2>
<p>Since 1 December 2022, business customers with a smart or advanced (AMR) meter, and anyone they nominate, can ask their supplier for up to 12 months of their historic smart meter data, free of charge and in a machine-readable format. The supplier must reply within 10 working days, either giving access or explaining why not and what to do next.{ref(n)}</p>
<p>So even if an online portal doesn't give you what you need, you can ask for the file directly.</p>
'''


SUPPLIER_LINKS = [
    ('half-hourly-data-british-gas.html', 'British Gas Business'), ('half-hourly-data-edf.html', 'EDF'),
    ('half-hourly-data-eon-next.html', 'E.ON Next'), ('half-hourly-data-npower-business-solutions.html', 'npower Business Solutions'),
    ('half-hourly-data-totalenergies.html', 'TotalEnergies Gas & Power')]


def ask_and_load(this=''):
    return '''
<h2 id="ask">What to ask for</h2>
<p>Ask for the half-hourly consumption data (kWh) for each meter, covering the last 12 months, as an Excel or CSV file. Quote each meter's MPAN, the supply number on your bill. Our <a href="get-your-data.html#ask">guide to getting your data</a> has a wording you can copy and a <a href="downloads/half-hourly-data-request.docx" download>letter template</a> (Word).</p>
<p>Check that the file has 48 readings for each day. A file of daily or monthly totals can't show the overnight and weekend patterns the <a href="analyser/">analyser</a> looks for.</p>
<p>Guides for other suppliers: ''' + ', '.join(f'<a href="{f}">{n}</a>' for f, n in SUPPLIER_LINKS if f != this) + '''.</p>
'''


def not_connected(name):
    return (f'<div class="note"><strong>Checked {long_date(CHECKED)}.</strong> Half Hourly Insights isn\'t connected with {name}. '
            f'This page summarises what {name} says on its own website. Portals and processes change, so follow the source links '
            'to check the current details. If something here is out of date, <a href="contact.html">let us know</a>.</div>')


SUPPLIER_TOC = [('portal', 'Online'), ('right', 'Your right to the data'), ('ask', 'What to ask for')]
SUPPLIER_NEXT = [('get-your-data.html', 'Getting your half-hourly data', 'What to ask for, whoever your supplier is.'),
                 ('mpan-profile-class.html', 'Reading your MPAN', 'Profile class, network region and meter type.'),
                 ('out-of-hours-electricity.html', 'Out-of-hours use', 'The first thing to look at once you have the data.')]

PAGES = []

# ── BRITISH GAS ─────────────────────────────────────────────────────────
PAGES.append(guide_page(
  'half-hourly-data-british-gas.html',
  'Half-hourly electricity data from British Gas Business',
  'Half-hourly data from British Gas Business',
  'Where British Gas business customers find their half-hourly electricity data, how to get access, and what to do if the portal doesn\'t give you a file you can use.',
  'How British Gas business customers get half-hourly electricity data: Energy360 DataView, how to request access, brokers, and the free 12-month data offer.',
  f'''
<p class="answer">British Gas business customers with a smart meter can see their half-hourly electricity data in Energy360 DataView, a free online platform. You ask British Gas for access through its online chat, and it says it will send your login details within 10 working days.{ref(1)}</p>
{not_connected('British Gas')}

<h2 id="portal">Energy360 DataView</h2>
<p>British Gas describes Energy360 DataView as its "free online platform for business customers with smart meters". It says you can:{ref(1)}</p>
<ul><li>zoom in on the half-hourly data with adjustable graphs</li><li>see out-of-hours reporting</li><li>access and download your daily energy consumption data, updated daily</li><li>set up scheduled reports and export your energy data</li></ul>
<p>Once you're logged in, British Gas says you'll see "actual consumption in a half hourly (HH) format".{ref(1)}</p>

<h2 id="access">How to get access</h2>
<ol><li><strong>Have a smart meter.</strong> If you don't, British Gas says you can request one free of charge.</li><li><strong>Ask for access</strong> through British Gas's online chat.</li><li><strong>Wait for your login details.</strong> British Gas says it sends them within 10 working days.</li><li><strong>Log in</strong> and look at your data.</li></ol>
<p>If your meter isn't smart, or its smart functions aren't working, British Gas says it can't show your data, but its customer care team can arrange a meter investigation or exchange.{ref(1)}</p>
<p>The Energy360 page is written for smart meter customers. If your site has an older half-hourly (AMR) meter, ask your account manager how to get the data, or use the request route below.</p>

<h2 id="brokers">Brokers and consultants</h2>
<p>A broker or other third party can request your half-hourly data for you, as long as they have the right authorisation on your account.{ref(1)}</p>
{your_right(3)}
<p>British Gas explained these rules to its business customers in March 2023, including that it would respond to data requests within 10 working days.{ref(2)}</p>
{ask_and_load('half-hourly-data-british-gas.html')}
''' + sources([
    ('British Gas: Energy360 DataView', 'https://www.britishgas.co.uk/business/gas-and-electricity/energy360'),
    ('British Gas business blog: The way businesses can request smart meter data is changing (31 March 2023)',
     'https://www.britishgas.co.uk/business/blog/the-way-businesses-can-request-smart-meter-data-is-changing'),
    GOV_OFFER]),
  [('portal', 'Energy360 DataView'), ('access', 'How to get access'), ('brokers', 'Brokers and consultants'),
   ('right', 'Your right to the data'), ('ask', 'What to ask for')],
  [('Does British Gas charge for half-hourly data?', 'British Gas describes Energy360 DataView as a free platform. Separately, government rules let business customers with a smart or advanced meter request up to 12 months of their data free of charge.'),
   ('How long does it take to get access?', 'British Gas says it sends Energy360 DataView login details within 10 working days of your request.'),
   ('Can my energy broker get the data for me?', 'Yes, if they have the right authorisation on your account, according to British Gas.')],
  SUPPLIER_NEXT,
  'British Gas Business half-hourly data: Energy360 DataView (free, smart meter customers, request via chat, login within 10 working days); brokers need authorisation; up to 12 months free on request under government rules.'))

# ── EDF ─────────────────────────────────────────────────────────────────
PAGES.append(guide_page(
  'half-hourly-data-edf.html',
  'Half-hourly electricity data from EDF (business)',
  'Half-hourly data from EDF',
  'EDF has different online routes for larger and smaller business customers. Here is what each one offers and how to get a file of half-hourly readings.',
  'How EDF business customers get half-hourly electricity data: MyBusiness Data Analysis and Data Export, Energy Hub and the smart meter data preference.',
  f'''
<p class="answer">EDF's larger business customers can download half-hourly data from the MyBusiness portal. Its Data Export tool exports up to a year of half-hourly data for up to 20 meters at a time, as a CSV or Excel file. Smaller business customers see their use in Energy Hub, part of MyAccount, once their smart meter data preference is set to half-hourly.{ref(1, 2)}</p>
{not_connected('EDF')}

<h2 id="portal">Larger businesses: MyBusiness</h2>
<p>EDF says MyBusiness lets you view and download smart meter consumption data "from as recently as 3 days ago".{ref(1)} There are two tools:</p>
<ul><li><strong>Data Analysis</strong>, in the sidebar, shows the data for up to four MPANs at once. You can choose a line or bar chart, change the granularity, set a date range of up to a year and choose which meters to show.</li><li><strong>Data Export</strong>, an option under Data Analysis, exports up to 350,000 records at a time. EDF says that is equivalent to a year of half-hourly data for up to 20 MPANs. You choose the sites from a list and download the data directly to CSV or Excel.</li></ul>
<p>For the analyser, export one file per meter where you can, so each site appears separately.</p>

<h2 id="small">Smaller businesses: Energy Hub and your data preference</h2>
<p>EDF says smart meters can send readings monthly, weekly, daily or every half hour, depending on your data preference. If you don't choose, it defaults to half-hourly, with the option to opt out within seven days.{ref(2)}</p>
<p>You can check or change the preference in MyAccount under "smart meter data preference", or by calling, emailing or texting EDF.{ref(2)} With the preference set to half-hourly, Energy Hub, a dashboard in MyAccount, shows your consumption in more detail.{ref(2, 3)}</p>
<p>EDF's public pages don't say whether Energy Hub lets you download half-hourly readings as a file. If it doesn't, ask EDF for the file under the rules below.</p>
{your_right(4)}
{ask_and_load('half-hourly-data-edf.html')}
''' + sources([
    ('EDF: Smart meter data for large business customers', 'https://www.edfenergy.com/large-business/customers/smart/smartdata'),
    ('EDF: Data is power: unlocking the power of half-hourly smart energy data (2 January 2025)',
     'https://www.edfenergy.com/energywise/small-business-data-is-power-half-hourly-smart-energy'),
    ('EDF: Small business online account management', 'https://www.edfenergy.com/energywise/small-business-effortless-online-account-management'),
    GOV_OFFER]),
  [('portal', 'Larger businesses: MyBusiness'), ('small', 'Smaller businesses: Energy Hub'),
   ('right', 'Your right to the data'), ('ask', 'What to ask for')],
  [('How many meters can I export from EDF at once?', 'EDF says MyBusiness Data Export handles up to 350,000 records at a time, equivalent to a year of half-hourly data for up to 20 MPANs.'),
   ('Why can\'t I see half-hourly data in Energy Hub?', 'Your smart meter data preference may be set to monthly, weekly or daily. EDF says you can change it in MyAccount under "smart meter data preference".'),
   ('How recent is the data in MyBusiness?', 'EDF says you can view and download consumption data from as recently as three days ago.')],
  SUPPLIER_NEXT,
  'EDF business half-hourly data: MyBusiness Data Analysis (4 MPANs) and Data Export (up to 350,000 records, about 20 MPANs for a year, CSV or Excel); small business Energy Hub with smart meter data preference set to half-hourly.'))

# ── E.ON NEXT ───────────────────────────────────────────────────────────
PAGES.append(guide_page(
  'half-hourly-data-eon-next.html',
  'Half-hourly electricity data from E.ON Next',
  'Half-hourly data from E.ON Next',
  'E.ON Next\'s public pages explain half-hourly meters and its metering services, but not a self-service download. Here is what it does say, and how to get the file.',
  'How E.ON Next business customers get half-hourly data: checking the meter, the Optimum tool, data collectors and the free 12-month data offer.',
  f'''
<p class="answer">E.ON Next doesn't describe a self-service download of half-hourly data for business customers on its public website. The simplest route is to ask for the file: if you have a smart or advanced meter, you're entitled to up to 12 months of data free of charge, with a reply within 10 working days.{ref(2)}</p>
{not_connected('E.ON Next')}

<h2 id="portal">What E.ON Next says about half-hourly meters</h2>
<ul><li>Half-hourly meters use automated meter reading (AMR) to record consumption every 30 minutes.{ref(1)}</li><li>If your profile class is 00, you're required to have a half-hourly meter. E.ON Next says you can check this in the first two digits of the MPAN on your bill, the top-left box, or on the meter itself.{ref(1)} (See <a href="mpan-profile-class.html">reading your MPAN</a>: under market-wide half-hourly settlement, 00 is starting to appear on smart meters too.)</li><li>A half-hourly meter also needs a meter operator, a data collector and a data aggregator. E.ON Next offers all three.{ref(1)}</li></ul>

<h2 id="collector">Your data collector has the readings too</h2>
<p>E.ON Next explains that the data collector collects your half-hourly data using a remote link, and the data aggregator validates it for billing and settlement. They can be different companies.{ref(1)} It may also be worth asking your data collector for the readings.</p>
<p>If E.ON is your data collector, E.ON Next says an entry-level version of its visualisation tool, Optimum, is included with the service, with upgrades available.{ref(1)} Ask whether your version can export half-hourly readings.</p>
{your_right(2)}
{ask_and_load('half-hourly-data-eon-next.html')}
''' + sources([
    ('E.ON Next: Half hourly meters', 'https://www.eonnext.com/business/half-hourly-meters'),
    GOV_OFFER]),
  [('portal', 'What E.ON Next says'), ('collector', 'Your data collector'), ('right', 'Your right to the data'), ('ask', 'What to ask for')],
  [('How do I know if I have a half-hourly meter?', 'E.ON Next says to look at the top-left box of the MPAN on your bill or meter: 00 means a half-hourly meter. As meters move to market-wide half-hourly settlement, smart meters can show 00 as well, so ask your supplier if you\'re not sure.'),
   ('What is Optimum?', 'E.ON\'s energy visualisation tool. E.ON Next says an entry-level version is included when E.ON is your half-hourly data collector.'),
   ('Who else holds my half-hourly data?', 'Your data collector, which collects the readings using a remote link. It may be a different company from your supplier.')],
  SUPPLIER_NEXT,
  'E.ON Next business half-hourly data: no self-service download described publicly; profile class 00 check; data collector holds readings; Optimum included with E.ON data collection; up to 12 months free on request.'))

# ── NPOWER BUSINESS SOLUTIONS ───────────────────────────────────────────
PAGES.append(guide_page(
  'half-hourly-data-npower-business-solutions.html',
  'Half-hourly data from npower Business Solutions',
  'Half-hourly data from npower Business Solutions',
  'npower Business Solutions customers can download a year of half-hourly data from their online account, or ask the Metering Team by email.',
  'How npower Business Solutions customers get half-hourly electricity data: the Dashboard Meters section (last 12 months) and email requests to the Metering Team.',
  f'''
<p class="answer">npower Business Solutions customers can download the last 12 months of half-hourly data from the Meters section of Dashboard, its online account system. You can also request it by email from the Metering Team at nbssmart@npower.com.{ref(1, 2)}</p>
{not_connected('npower Business Solutions')}

<h2 id="portal">Dashboard: the Meters section</h2>
<p>npower Business Solutions' Dashboard quickstart guide says the Meters section is where you submit meter reads, download consumption and view historical reads. You can search for meters by MPAN, MPRN (gas) or meter serial number.{ref(2)}</p>
<p>The option to use is "Download Half-Hourly (HH) data consumption". The guide says it gives "the last 12 months of HH data, or as far back as we have recorded if under 12 months".{ref(2)}</p>

<h2 id="email">Asking by email</h2>
<p>npower Business Solutions' metering page says you can request half-hourly data for your meter from the company that supplies you, and that its own customers should email the Metering Team at nbssmart@npower.com.{ref(1)}</p>
{your_right(3)}
{ask_and_load('half-hourly-data-npower-business-solutions.html')}
''' + sources([
    ('npower Business Solutions: Metering', 'https://npowerbusinesssolutions.com/my-account/metering'),
    ('npower Business Solutions: Dashboard quickstart guide (PDF)', 'https://npowerbusinesssolutions.com/hubfs/Dashboard-Quickstart-Guide.pdf'),
    GOV_OFFER]),
  [('portal', 'Dashboard: the Meters section'), ('email', 'Asking by email'), ('right', 'Your right to the data'), ('ask', 'What to ask for')],
  [('How far back can I download from Dashboard?', 'The last 12 months, or as far back as npower Business Solutions has recorded if that is less, according to its quickstart guide.'),
   ('Who do I email for half-hourly data?', 'npower Business Solutions customers can email the Metering Team at nbssmart@npower.com, as listed on its metering page.')],
  SUPPLIER_NEXT,
  'npower Business Solutions half-hourly data: Dashboard Meters section, "Download Half-Hourly (HH) data consumption", last 12 months; or email the Metering Team at nbssmart@npower.com.'))

# ── TOTALENERGIES ───────────────────────────────────────────────────────
PAGES.append(guide_page(
  'half-hourly-data-totalenergies.html',
  'Half-hourly electricity data from TotalEnergies',
  'Half-hourly data from TotalEnergies',
  'TotalEnergies Gas & Power has an online portal for half-hourly data from smart and AMR meters. Here is what it covers, how to get access, and what to do if your site isn\'t included.',
  'How TotalEnergies Gas & Power business customers get half-hourly data: the Insights portal, the request form, which meters it covers and the free offer.',
  f'''
<p class="answer">TotalEnergies Gas & Power business customers with a smart or AMR meter can view and download half-hourly data in TotalEnergies Insights, an online portal launched on 1 October 2024, with up to 12 months of history. You get access by completing its Half-Hourly Data Request Form.{ref(1)}</p>
{not_connected('TotalEnergies Gas & Power')}

<h2 id="portal">TotalEnergies Insights</h2>
<p>TotalEnergies says the portal lets you:{ref(1)}</p>
<ul><li>view, download and track your consumption, including half-hourly data with graphs</li><li>see a portfolio view if you have more than one site</li><li>receive data daily, for the previous day</li><li>set a consumption tracker and get notifications when use exceeds it</li></ul>
<p>It also notes that portal figures can differ from your bill because of timing, and that the portal data comes "direct from the meter".{ref(1)}</p>

<h2 id="which">Which meters it covers</h2>
<p>TotalEnergies' FAQ says that, for electricity, the portal covers "All AMR & Smart meters which are Non Half-Hourly settled (profile class 1-8)".{ref(1)} If your site is already settled half-hourly (profile class 00), the page doesn't say how to get its data online, so ask your account manager or use the request route below.</p>

<h2 id="access">How to get access</h2>
<p>TotalEnergies says customers who already use its online services are enrolled automatically, and others should complete the Half-Hourly Data Request Form linked from its half-hourly data page. To give a third party such as a broker access, contact its customer service team.{ref(1)}</p>
{your_right(2)}
{ask_and_load('half-hourly-data-totalenergies.html')}
''' + sources([
    ('TotalEnergies Gas & Power: Half-hourly consumption data',
     'https://business.totalenergies.uk/information-centre/energy-essentials/smart-and-amr-meters-business/half-hourly-energy-consumption'),
    GOV_OFFER]),
  [('portal', 'TotalEnergies Insights'), ('which', 'Which meters it covers'), ('access', 'How to get access'),
   ('right', 'Your right to the data'), ('ask', 'What to ask for')],
  [('Is my half-hourly settled site in TotalEnergies Insights?', 'TotalEnergies\' FAQ says the portal covers electricity meters that are not half-hourly settled (profile classes 1 to 8). For a profile class 00 site, ask your account manager.'),
   ('Why don\'t the portal figures match my bill?', 'TotalEnergies says there are always timing differences between half-hourly data and billed consumption, and that portal data comes direct from the meter.'),
   ('How much history does TotalEnergies Insights hold?', 'Up to 12 months, according to TotalEnergies.')],
  SUPPLIER_NEXT,
  'TotalEnergies Gas & Power half-hourly data: TotalEnergies Insights portal (from 1 October 2024, up to 12 months, smart and AMR meters not half-hourly settled, profile classes 1-8); access via the Half-Hourly Data Request Form.'))

SUPPLIERS = [
    ('half-hourly-data-british-gas.html', 'British Gas Business'),
    ('half-hourly-data-edf.html', 'EDF'),
    ('half-hourly-data-eon-next.html', 'E.ON Next'),
    ('half-hourly-data-npower-business-solutions.html', 'npower Business Solutions'),
    ('half-hourly-data-totalenergies.html', 'TotalEnergies Gas & Power'),
]

# ── MPAN AND PROFILE CLASS ──────────────────────────────────────────────
DNO = [
    ('10', 'East England', 'UK Power Networks (Eastern Power Networks)'),
    ('11', 'East Midlands', 'National Grid Electricity Distribution (East Midlands)'),
    ('12', 'London', 'UK Power Networks (London Power Networks)'),
    ('13', 'North Wales, Merseyside and Cheshire', 'SP Energy Networks (SP Manweb)'),
    ('14', 'West Midlands', 'National Grid Electricity Distribution (West Midlands)'),
    ('15', 'North East England', 'Northern Powergrid (Northeast)'),
    ('16', 'North West England', 'Electricity North West'),
    ('17', 'North Scotland', 'Scottish and Southern Electricity Networks (Scottish Hydro Electric Power Distribution)'),
    ('18', 'Central and Southern Scotland', 'SP Energy Networks (SP Distribution)'),
    ('19', 'South East England', 'UK Power Networks (South Eastern Power Networks)'),
    ('20', 'Southern England', 'Scottish and Southern Electricity Networks (Southern Electric Power Distribution)'),
    ('21', 'South Wales', 'National Grid Electricity Distribution (South Wales)'),
    ('22', 'South West England', 'National Grid Electricity Distribution (South West)'),
    ('23', 'Yorkshire', 'Northern Powergrid (Yorkshire)'),
]
PROFILE_CLASSES = [
    ('00', 'Half-hourly metered and settled'),
    ('01', 'Domestic unrestricted'),
    ('02', 'Domestic Economy 7'),
    ('03', 'Non-domestic unrestricted'),
    ('04', 'Non-domestic Economy 7'),
    ('05', 'Non-domestic maximum demand, peak load factor less than 20%'),
    ('06', 'Non-domestic maximum demand, peak load factor 20% to 30%'),
    ('07', 'Non-domestic maximum demand, peak load factor 30% to 40%'),
    ('08', 'Non-domestic maximum demand, peak load factor over 40%'),
]

PAGES.append(guide_page(
  'mpan-profile-class.html',
  'Reading your MPAN: profile class and network region',
  'Reading your MPAN',
  'The supply number on your electricity bill tells you more than most people realise: your network region, how your meter is settled and, for now, whether it is half-hourly.',
  'What the MPAN on a business electricity bill means: the 13-digit core, network region IDs, profile classes 00 to 08, and what half-hourly settlement changes.',
  f'''
<p class="answer">Your MPAN is the supply number on every electricity bill. The bottom line is the 13-digit MPAN itself, and its first two digits identify your network region. The top line starts with the profile class: 00 has meant a half-hourly metered supply, and 01 to 08 mean your use is estimated from standard profiles. As meters move to market-wide half-hourly settlement, smart meters are being given 00 too, so 00 no longer tells you which kind of meter you have.{ref(1, 2, 3)}</p>

<h2 id="where">Where to find it</h2>
<p>Suppliers must show the supply number on every bill, or at least once a year if no bill is sent.{ref(1)} It is often called the supply number or "S number", and is printed in two rows: a top line and a bottom line.{ref(1, 4)} E.ON Next notes that the MPAN is also on the meter itself.{ref(3)}</p>

<h2 id="bottom">The bottom line: your MPAN</h2>
<p>The bottom line is the Meter Point Administration Number (MPAN): a distributor ID, a unique reference number and a check digit.{ref(1)} It is 13 digits long.{ref(4)} This is the number to quote when you ask for half-hourly data, and it stays the same when you change supplier.</p>
<p>The first two digits, the distributor ID, tell you which network region you are in and so which distribution network operator (DNO) runs your local network:{ref(4, 5)}</p>
<div class="table-wrap"><table><thead><tr><th>Distributor ID</th><th>Region</th><th>Network operator</th></tr></thead><tbody>
''' + ''.join(f'<tr><td>{i}</td><td>{r}</td><td>{o}</td></tr>' for i, r, o in DNO) + f'''
</tbody></table></div>
<p>Numbers above 23 belong to independent network operators (IDNOs).{ref(4)} The region matters because network charges are set by each network operator, so they differ from one region to another.</p>

<h2 id="top">The top line: profile class and charging codes</h2>
<p>Traditionally the top line holds three codes: the profile class, the meter timeswitch code (MTC) and the line loss factor class (LLFC).{ref(1)} The line loss factor class links to the network charges and losses that apply to your supply.</p>
<p>The profile class tells the industry how your electricity use is estimated for settlement:{ref(2, 3)}</p>
<div class="table-wrap"><table><thead><tr><th>Profile class</th><th>Meaning</th></tr></thead><tbody>
''' + ''.join(f'<tr><td>{c}</td><td>{m}</td></tr>' for c, m in PROFILE_CLASSES) + f'''
</tbody></table></div>
<p>Classes 05 to 08 are for maximum demand meters, which record the highest demand in a period. The peak load factor is the electricity actually used in a period as a percentage of what would have been supplied if the maximum demand had been kept up for the whole period.{ref(2)} The government's smart meter rollout for businesses covers profile classes 1 to 4. Larger sites outside it already have advanced (AMR) meters.{ref(6)}</p>

<h2 id="mhhs">What half-hourly settlement changes</h2>
<p>Under <a href="half-hourly-settlement.html">market-wide half-hourly settlement</a>, profile classes are being removed, except for older meters that aren't smart.{ref(1)} Ofgem approved a new top-line format in 2023:{ref(1)}</p>
<ul><li>The profile class stays, but a meter that has moved to the new arrangements and no longer has a profile class shows 00.</li><li>The meter timeswitch code is replaced by a Standard Settlement Configuration (SSC) ID, shown as 0000 where it doesn't apply.</li><li>The line loss factor class is replaced by a DUoS tariff ID, which identifies the network charges that apply.</li></ul>
<p>The bottom line, your MPAN, doesn't change.{ref(1)}</p>
<p>In practice, 00 on a recent bill now means your supply is settled half-hourly. It no longer tells you whether you have a traditional half-hourly (AMR) meter or a smart meter. Either way, your meter records half-hourly readings, so ask your supplier for them.</p>
''' + sources([
    ('Ofgem: Decision to approve REC Change Proposal R0083, changes to supply number format for MHHS (November 2023)',
     'https://www.ofgem.gov.uk/sites/default/files/2023-11/Decision%20to%20approve%20REC%20Change%20Proposal%20R0083%20Changes%20to%20Supply%20Number%20Format%20for%20MHHS%20and%20to%20reject%20R0083A.pdf'),
    ('Elexon: Profiling (profile classes)', 'https://www.elexon.co.uk/bsc/settlement/profiling/'),
    ('E.ON Next: Half hourly meters', 'https://www.eonnext.com/business/half-hourly-meters'),
    ('EDF: Distribution network operators (MPAN prefix look-up)', 'https://www.edfenergy.com/node/5541'),
    ('Ofgem: List of all electricity licensees (August 2026)',
     'https://www.ofgem.gov.uk/sites/default/files/2026-06/List%20of%20all%20electricity%20licensees%20including%20suppliers.pdf'),
    GOV_OFFER]),
  [('where', 'Where to find it'), ('bottom', 'The bottom line: your MPAN'), ('top', 'The top line'), ('mhhs', 'What half-hourly settlement changes')],
  [('Does profile class 00 mean I have a half-hourly meter?', 'It used to. Under market-wide half-hourly settlement, meters that have moved across and have no profile class are shown as 00, smart meters included. So 00 now means the supply is settled half-hourly, from either kind of meter.'),
   ('How do I find my network operator from my MPAN?', 'The first two digits of the 13-digit MPAN are the distributor ID. Numbers 10 to 23 are the 14 regional network operators; higher numbers are independent network operators.'),
   ('Does my MPAN change when I switch supplier?', 'No. The MPAN identifies the supply point, so it stays the same.')],
  [('get-your-data.html', 'Getting your half-hourly data', 'What to ask for once you have your MPAN.'),
   ('half-hourly-settlement.html', 'Half-hourly settlement (MHHS)', 'The timetable and what it means for you.'),
   ('glossary.html', 'Glossary', 'kW, kWh, kVA and other terms.')],
  'The MPAN supply number: bottom line is the 13-digit MPAN (distributor ID 10-23 identifies the network region, unique reference, check digit); top line profile class 00-08, MTC, LLFC; under MHHS profile classes are removed and migrated meters show 00.'))

# ── BENCHMARKS ──────────────────────────────────────────────────────────
# BEES 2014-15 overarching tables, Figure 3.7 (premises with non-electrical uses)
# and Figure 3.8 (all-electric premises). kWh per m2 of gross internal area a year.
BEES_MIXED = [  # sector, 10th, lower quartile, median, upper quartile, 90th
    ('Offices', 36.9, 56.5, 87.5, 136.9, 206.1),
    ('Retail', 34.6, 70.3, 115.5, 175.2, 341.3),
    ('Hospitality', 76.0, 114.8, 193.3, 429.4, 975.8),
    ('Education', 29.5, 37.4, 48.7, 66.3, 79.3),
    ('Health', 54.9, 63.5, 83.4, 139.5, 275.1),
    ('Industrial', 26.2, 31.0, 42.1, 58.3, 96.6),
    ('Storage', 14.4, 21.4, 31.5, 56.7, 71.7),
    ('Emergency services', 45.6, 64.6, 117.0, 142.1, 244.6),
    ('Community, arts and leisure', 4.5, 8.3, 27.2, 79.8, 153.0),
]
BEES_ELECTRIC = [
    ('Offices', 81.9, 114.0, 124.4, 159.2, 244.8),
    ('Retail', 34.2, 80.2, 114.6, 177.5, 391.3),
    ('Hospitality', 75.8, 131.8, 490.1, 992.9, 1197.3),
    ('Industrial', 34.7, 45.0, 62.9, 80.6, 108.8),
    ('Storage', 14.4, 22.1, 37.0, 59.5, 73.2),
    ('Community, arts and leisure', 16.0, 24.3, 74.4, 170.5, 199.3),
]


def bees_table(rows, label):
    f = lambda v: f'{v:,.0f}'
    # Focusable so keyboard users can scroll it sideways on a narrow screen.
    return (f'<div class="table-wrap" tabindex="0" role="region" aria-label="{label}"><table><thead><tr><th>Sector</th><th class="num">Lowest 10%<br>below</th>'
            '<th class="num">Lower quartile</th><th class="num">Median</th><th class="num">Upper quartile</th>'
            '<th class="num">Highest 10%<br>above</th></tr></thead><tbody>'
            + ''.join(f'<tr><td>{s}</td>' + ''.join(f'<td class="num">{f(v)}</td>' for v in vals) + '</tr>' for s, *vals in rows)
            + '</tbody></table></div>')


PAGES.append(guide_page(
  'electricity-benchmarks.html',
  'Electricity benchmarks by sector: kWh per m² a year',
  'Electricity benchmarks by sector',
  'Is your building\'s electricity use normal? Government survey figures give the typical range for offices, shops, schools and other non-domestic buildings.',
  'Typical electricity use per square metre for UK non-domestic buildings by sector, from government survey data, and how DEC benchmarks work.',
  f'''
<p class="answer">A typical office in England and Wales that also uses gas or another fuel uses about 88 kWh of electricity per square metre of floor area a year, according to the government's Building Energy Efficiency Survey. Half of such offices use between about 57 and 137 kWh/m². Compare your building with the range for its sector, not a single number, and compare like with like: all-electric buildings use much more electricity.{ref(1, 2)}</p>

<h2 id="survey">Typical use by sector</h2>
<p>The Building Energy Efficiency Survey (BEES) modelled energy use in non-domestic buildings in England and Wales for 2014 to 2015. Its published tables give the spread of electricity use per square metre in each sector.{ref(1, 2)} Figures are kWh per m² of gross internal floor area a year.</p>
<h3>Buildings that also use gas or another fuel</h3>
{bees_table(BEES_MIXED, 'Electricity use per square metre, buildings that also use other fuels')}
<h3>All-electric buildings</h3>
{bees_table(BEES_ELECTRIC, 'Electricity use per square metre, all-electric buildings')}
<p>Source: BEES overarching tables, figures 3.7 and 3.8.{ref(2)} The median is the middle building: half use more, half use less. The quartiles mark the middle half of buildings.</p>

<h2 id="use">How to compare your own building</h2>
<ol><li><strong>Work out a year's electricity use in kWh.</strong> The <a href="analyser/">analyser</a> gives this from your half-hourly data, scaled to a year if a few days are missing.</li><li><strong>Find the gross internal floor area</strong> in m², measured to the inside of the outside walls on every floor. BEES uses this measure.{ref(3)}</li><li><strong>Divide one by the other.</strong> Or enter the floor area under Floor area (m²) in the analyser's site settings, and it shows kWh per m² for you.</li><li><strong>Pick the right table.</strong> If your heating is electric, use the all-electric figures.</li></ol>

<h2 id="limits">What these figures can and can't tell you</h2>
<ul><li><strong>They are from 2014 to 2015.</strong> Many buildings have changed since, for example through LED lighting or electric heating. Treat the figures as a broad guide, not a target.</li><li><strong>Sectors are broad.</strong> "Hospitality" covers everything from a café to a hotel with a pool, which is why its range is so wide.</li><li><strong>A high figure isn't proof of waste.</strong> Long opening hours, a server room or a commercial kitchen can push use up for good reasons. Half-hourly data shows <em>when</em> the electricity is used, which is the next question to ask.</li></ul>

<p>For what normal half-hourly use looks like in each type of building, see our sector guides: <a href="schools-electricity.html">schools</a>, <a href="offices-council-buildings.html">offices and council buildings</a>, <a href="leisure-centres.html">leisure centres</a>, <a href="healthcare-electricity.html">healthcare</a>, <a href="industrial-warehouses.html">industrial and warehouses</a> and <a href="retail-hospitality.html">retail and hospitality</a>.</p>

<h2 id="dec">Display Energy Certificates and CIBSE benchmarks</h2>
<p>Public authority buildings over 250 m² that the public often visits must display a Display Energy Certificate (DEC). For buildings over 1,000 m², it is renewed every year.{ref(4)}</p>
<p>A DEC's operational rating compares the building's actual energy use with a benchmark that is typical for its type. A rating of 100 is typical, 200 means twice the typical carbon emissions, and 0 means zero emissions.{ref(4)} The benchmarks were prepared by the Chartered Institution of Building Services Engineers (CIBSE) for 29 building categories, with electricity and other fuels shown separately.{ref(4)} They are published in CIBSE TM46, <em>Energy benchmarks</em> (October 2008), which CIBSE sells; CIBSE also runs an online Energy Benchmarking Dashboard with more recent data.{ref(5)}</p>
<p>You can look up the DEC for a public building, such as a nearby school or council office, on GOV.UK.{ref(6)}</p>
''' + sources([
    ('Department for Business, Energy and Industrial Strategy: Building Energy Efficiency Survey (BEES), 2016', 'https://www.gov.uk/government/publications/building-energy-efficiency-survey-bees'),
    ('BEES overarching tables (Excel), figures 3.7 and 3.8', 'https://assets.publishing.service.gov.uk/media/5a7f6a1bed915d74e33f648b/Overarching_report_excel_tables_publish.xlsx'),
    ('BEES overarching report (PDF): floor areas are gross internal area', 'https://assets.publishing.service.gov.uk/media/5a75964540f0b67f59fce0d4/BEES_overarching_report_FINAL.pdf'),
    ('GOV.UK: The government methodology for operational ratings, display energy certificates and recommendation reports (updated 11 November 2026)',
     'https://www.gov.uk/government/publications/government-methodology-for-producting-operational-ratings-display-energy-certificates-and-advisory-reports/the-government-methodology-for-operational-ratings-display-energy-certificates-and-recommendation-reports'),
    ('CIBSE: TM46 Energy benchmarks', 'https://www.cibse.org/knowledge-research/knowledge-portal/tm46-energy-benchmarks'),
    ('GOV.UK: Find an energy certificate', 'https://www.gov.uk/find-energy-certificate')]),
  [('survey', 'Typical use by sector'), ('use', 'How to compare your own building'), ('limits', 'What the figures can\'t tell you'),
   ('dec', 'DECs and CIBSE benchmarks')],
  [('How much electricity does a typical office use per square metre?', 'About 88 kWh per m² a year for an office that also uses gas or another fuel, and about 124 kWh per m² for an all-electric office, according to the government\'s Building Energy Efficiency Survey (2014 to 2015 data, England and Wales).'),
   ('Which floor area should I use?', 'Gross internal area: the floor area measured to the inside of the outside walls on every floor. That is the measure the survey figures use.'),
   ('What does a DEC rating of 100 mean?', 'That the building\'s energy use is typical for its type. 200 means twice the typical carbon emissions.')],
  [('base-load.html', 'Base load', 'What always runs, and how it shapes the annual total.'),
   ('out-of-hours-electricity.html', 'Out-of-hours use', 'Often the reason a building sits at the top of its range.'),
   ('sectors.html', 'By sector', 'What normal looks like in schools, offices, leisure centres and more.')],
  'Electricity benchmarks per m² (gross internal area) by sector from BEES 2014-15: offices median 88 kWh/m² (with other fuels) or 124 (all-electric); full quartile ranges for nine sectors; DEC operational rating 100 is typical, based on CIBSE TM46 benchmarks.'))
