"""
The core pages: home, how it works, getting your data, FAQ, contact, thanks,
privacy and 404. Bodies are HTML; metadata for search and AI tools is added
in core_pages() at the bottom.

Written for a general business reader, in the voice of the team that runs the
site ("we"). Explain terms on first use; write as much as the reader needs.
"""
from kit import (CONTACT_EMAIL, CONTACT_NAME, OPERATOR, OPERATOR_URL, SOLAR_URL, APP, Page,
                 cta, photo, faq_section, guide, page_hero, related, updated_line, GUIDE_PDF, guide_download)

FORM_ENDPOINT = 'https://formspree.io/f/xeagedqj'  # Half Hourly Insights enquiries form in Formspree

HOME = ('Home', 'index.html')
GUIDES = ('Guides', 'guides.html')

PAGES = {}

# ── HOME ────────────────────────────────────────────────────────────────
PAGES['index.html'] = ('Half Hourly Insights: free business electricity data analysis',
  'Free analysis of half-hourly (HH) electricity data for UK businesses and public sector sites: use while closed, base load, peaks and unusual days.',
  f'''<div class="hero-wrap">
<div class="hero-media" aria-hidden="true"><img src="images/hero-town.jpg" srcset="images/hero-town-900.jpg 800w, images/hero-town.jpg 1440w" sizes="100vw" width="1440" height="1080" alt="" fetchpriority="high"></div>
<section class="hero" aria-labelledby="hero-h">
  <div class="hero-copy">
    <p class="hero-audience">For UK businesses and public sector sites with half-hourly (HH) electricity data</p>
    <h1 id="hero-h">Where is your business's electricity going?</h1>
    <p class="hero-lead">Load the half-hourly readings from your business electricity meters. Within a minute you'll see how much your buildings use while they're closed, what never switches off, how close you get to your supply limit, and what each of these costs you.</p>
    <p class="hero-check">Free, with no sign-up. Not sure whether you have half-hourly data? <a href="get-your-data.html">Here's how to check</a>.</p>
    <p class="hero-check hero-not">This site is for business and public sector meters only. It isn't designed for household electricity.</p>
    <div class="hero-points">
      <div><strong>Biggest costs first</strong><span>Ranked by cost, with the evidence for each</span></div>
      <div><strong>Many sites at once</strong><span>One file per meter, with every site ranked</span></div>
      <div><strong>Private</strong><span>Your data stays on your computer</span></div>
    </div>
  </div>
  <div class="start-card">
    <h2>Start with your HH meter file</h2>
    <p>An Excel or CSV file for each meter. All the common supplier layouts work.</p>
    <a href="analyser/" class="btn btn-gold btn-lg">Analyse my data</a>
    <p class="start-sample"><a href="sample-report.html">Or see a sample report first</a></p>
    <div class="start-result">
      <div class="k">From the example file (a made-up office)</div>
      <div class="big">33%</div>
      <div class="small">of its electricity was used while the building was closed</div>
    </div>
    <p class="or">No data to hand? <a href="sample-report.html">See a sample report</a>, or <a href="samples/example-office.csv" download>download our example file</a> and load it into the analyser.</p>
  </div>
</section>
</div>

<section class="section">
  <div class="section-inner">
    <div class="head-row">
      <h2 class="section-title">What half-hourly data shows</h2>
      <p>Your bill gives one total for the month. Half-hourly data records your use every 30 minutes, 48 readings a day, so you can see when electricity is used and spot use that shouldn't be happening.</p>
    </div>
    <div class="reasons">
      <div><h3>Use while closed</h3><p>Electricity used when the building should be shut, over and above what always runs. It's often the cheapest saving to make, because it can usually be fixed by changing timers and control settings.</p></div>
      <div><h3>Base load</h3><p>The minimum your building uses at all times, including overnight and at weekends. Because it runs all year, even a small reduction makes a noticeable saving.</p></div>
      <div><h3>Peaks and supply capacity</h3><p>Your busiest half hours compared with the maximum your electricity connection allows, and how much room is left for heat pumps or EV charging.</p></div>
      <div><h3>Unusual days</h3><p>Days that don't follow the normal pattern, and lasting changes that suggest something was left on, or that a fix has worked.</p></div>
      <div><h3>Weekends and bank holidays</h3><p>Days when the site should be quiet but isn't, checked against the opening hours you enter.</p></div>
      <div><h3>Savings estimates</h3><p>What you could save by cutting use while closed or reducing peaks. Where two savings overlap, they're only counted once.</p></div>
    </div>
  </div>
</section>

<section class="section privacy-band">
  <div class="section-inner">
    <h2 class="section-title">Your data stays on your computer</h2>
    <p class="section-lead">The analyser does all its work inside your web browser. Your meter files are read on your own computer and are never sent to us or anyone else.</p>
    <div class="reasons">
      <div><h3>Nothing uploaded</h3><p>No server is involved in the analysis. Once the page has loaded, you can disconnect from the internet and carry on working.</p></div>
      <div><h3>No account</h3><p>You don't need to sign up or give an email address, and the site uses no tracking cookies.</p></div>
      <div><h3>You keep the results</h3><p>Reports, spreadsheets and project files are saved to your computer. Save a project to come back to it later.</p></div>
    </div>
  </div>
</section>

<section class="section band-mist">
  <div class="section-inner">
    <div class="split">
      <div>
        <span class="section-kicker">The analyser</span>
        <h2 class="section-title">What you get for each site</h2>
        <p class="section-lead">Each site opens with its three most costly issues to investigate, and a rating for how reliable the evidence is. Every figure is labelled as measured or estimated.</p>
        <ul class="ticks">
          <li><strong>PDF reports</strong> for each site and for your whole estate, plus Excel files for your own analysis</li>
          <li><strong>A heatmap</strong> showing every half hour of the year on one chart</li>
          <li><strong>Data checks</strong> for missing readings, zero days, clock changes and duplicate rows before any figures are shown</li>
          <li><strong>Customer dashboards</strong>, a password-protected copy you can send to a client</li>
        </ul>
      </div>
      <div>
        <div class="shot"><img src="images/shot-site.png" width="1360" height="900" alt="The analyser showing a site's headline figures, energy split and top issues to investigate" loading="lazy"></div>
        <p class="shot-caption">A site page from the example file. All data on this site is made up.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="section-inner">
    <div class="head-row">
      <h2 class="section-title">How it works in three steps</h2>
      <p>No account and nothing to install. It works in Chrome or Edge on any recent computer. For a step-by-step walk-through, <a href="{GUIDE_PDF}" download style="color:var(--blue);text-decoration:underline">download the user guide</a> (PDF).</p>
    </div>
    <div class="steps">
      <div><div class="step-head"><span class="step-n">1</span><span class="step-line"></span></div><h3>Load your files</h3><p>Drag in one file for each meter. The analyser works out the layout, checks the readings and tells you what it found.</p></div>
      <div><div class="step-head"><span class="step-n">2</span><span class="step-line"></span></div><h3>Set opening hours</h3><p>Enter when each building is open. The figures for use while closed depend on this, so the analyser asks you to confirm them.</p></div>
      <div><div class="step-head"><span class="step-n">3</span><span class="step-line"></span></div><h3>Review and share</h3><p>Work through the findings, then download PDF reports, Excel files or a customer dashboard.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="section-inner split">
    <div>
      <span class="section-kicker">Who it's for</span>
      <h2 class="section-title">Any building with a half-hourly meter</h2>
      <p class="section-lead">Schools, offices, council buildings, leisure centres, hospitals, factories and shops all use electricity differently. That's why the analyser compares each site with its own opening hours rather than a general benchmark.</p>
      <p style="margin-top:24px"><a href="sectors.html" class="btn btn-outline">What to look for in your sector</a></p>
    </div>
    <div>{photo('town-street', 'A town high street with an electric bus, a civic building and a car charging at a roadside charger')}</div>
  </div>
</section>

<section class="section band-mist">
  <div class="section-inner">
    <div class="head-row">
      <h2 class="section-title">Guides</h2>
      <p>Clear answers to the questions people ask when they first look at half-hourly data.</p>
    </div>
    <div class="link-grid" style="margin-top:36px">
      <a class="link-card has-thumb" href="example-office-analysis.html"><div class="card-thumb"><img src="images/guides/example-office-analysis.jpg" srcset="images/guides/example-office-analysis-600.jpg 600w, images/guides/example-office-analysis.jpg 1200w" sizes="(max-width: 700px) 100vw, 400px" width="1200" height="630" alt="" loading="lazy"></div><h3>Worked example</h3><p>A year of data from one office, and what the analyser found.</p><span class="more">Read the example</span></a>
      <a class="link-card has-thumb" href="out-of-hours-electricity.html"><div class="card-thumb"><img src="images/guides/out-of-hours-electricity.jpg" srcset="images/guides/out-of-hours-electricity-600.jpg 600w, images/guides/out-of-hours-electricity.jpg 1200w" sizes="(max-width: 700px) 100vw, 400px" width="1200" height="630" alt="" loading="lazy"></div><h3>Out-of-hours use</h3><p>How to find electricity used while the building is closed, and reduce it.</p><span class="more">Read the guide</span></a>
      <a class="link-card has-thumb" href="base-load.html"><div class="card-thumb"><img src="images/guides/base-load.jpg" srcset="images/guides/base-load-600.jpg 600w, images/guides/base-load.jpg 1200w" sizes="(max-width: 700px) 100vw, 400px" width="1200" height="630" alt="" loading="lazy"></div><h3>Base load</h3><p>What always runs, why it matters and how to reduce it.</p><span class="more">Read the guide</span></a>
      <a class="link-card has-thumb" href="supply-capacity.html"><div class="card-thumb"><img src="images/guides/supply-capacity.jpg" srcset="images/guides/supply-capacity-600.jpg 600w, images/guides/supply-capacity.jpg 1200w" sizes="(max-width: 700px) 100vw, 400px" width="1200" height="630" alt="" loading="lazy"></div><h3>Supply capacity</h3><p>Your supply limit, and whether there's room for heat pumps and EV charging.</p><span class="more">Read the guide</span></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="section-inner split">
    <div><span class="section-kicker">Sister site</span><h2 class="section-title">Thinking about solar too?</h2></div>
    <div><p class="section-lead">Solar panels generate in daylight, so they save the most when a building uses plenty of electricity during the day. Your half-hourly data shows how much that is. Our <a href="{SOLAR_URL}" style="color:var(--blue);text-decoration:underline">UK Solar Calculator</a> estimates system size, savings and payback for your roof.</p>
    {photo('solar-private-wire', 'Aerial view of a solar farm connected by cable to a substation and a business park beside farmland')}</div>
  </div>
</section>

{cta('Want help with your results?', 'We can help you turn the findings into savings, or carry out a full energy audit across your sites.')}
''')

# ── HOW IT WORKS ────────────────────────────────────────────────────────
PAGES['how-it-works.html'] = ('How it works | Half Hourly Insights',
  'What the analyser does with your half-hourly data: how it reads files, checks quality, sets the base load, prices use while closed and builds findings.',
  page_hero('How it works', 'What the analyser does with your data',
            'A step-by-step explanation, from reading your file to the figures in the report. In the analyser, each finding also has a "show calculation and evidence" link with the full working.',
            crumbs=[HOME, ('How it works', 'how-it-works.html')]) +
  guide(updated_line() + '''
<p class="answer">The analyser checks every half-hourly reading, works out how much electricity the site uses when it's open and when it's closed, and prices the difference at your rates. It tells you where to look. Someone who knows the building then decides what to change.</p>
''' + photo('switchroom-tablet', 'Three people in a switch room looking at data on a tablet beside open electrical panels', 'The findings tell you where to look. A walk round the building tells you why.') + guide_download('Want the practical steps?') + '''

<h2 id="files">1. Reading your files</h2>
<p>Load one file for each meter, as Excel (.xlsx or .xls) or CSV. Three layouts work:</p>
<ul><li><strong>Day per row:</strong> a date, then 48 half-hourly readings. This is the most common supplier format.</li><li><strong>Day per column:</strong> the same, turned on its side.</li><li><strong>Timestamped:</strong> one reading per row, with its date and time.</li></ul>
<p>The analyser shows how it read each file: which column held the dates, whether readings were in kWh or kW, and anything it ignored. If a file covers more than a year, the last 12 months are analysed by default. You can choose a different period, and long-term trends still use the whole file.</p>

<h2 id="checks">2. Checking the data</h2>
<p>Before showing any figures, the analyser looks for problems that would make them wrong:</p>
<ul><li>missing readings, which are left out rather than counted as zero</li><li>days of zero readings, which usually point to a meter or data fault</li><li>days when the clocks change, and duplicate rows, which it holds back for you to decide on</li><li>single readings far above the usual peak</li></ul>
<p>Each site is rated Good, Check or Poor. You can exclude readings you know are wrong and record why, and the reason is saved with the analysis.</p>

<h2 id="calendar">3. Opening hours</h2>
<p>The figures for use while closed depend on knowing when each building should be open. Every site starts with standard office hours, marked as unconfirmed until you check them. You can set hours for all sites at once or one at a time, including closures, bank holidays and overnight shifts. Findings based on unconfirmed hours get a lower confidence rating.</p>

<h2 id="base">4. Base load and use while closed</h2>
<p><strong>Base load</strong> is the level of demand a site rarely drops below. The analyser measures it as the 5th percentile of all valid half-hourly readings, which means demand is higher than this 95% of the time. It's the equipment that never switches off, such as servers, fridges and anything on standby.</p>
<p><strong>Closed-hours excess</strong> is the electricity used while the site is closed, over and above the base load. Sites are ranked by this figure because it's often the cheapest use to reduce, usually by changing timers, controls and building management settings rather than buying new equipment.</p>

<h2 id="costs">5. Costs and annual figures</h2>
<p>Costs use the unit rates you enter, either one flat rate or different rates for different times of day. They leave out standing charges, capacity charges and other fixed costs. They show what a pattern costs you now and are not a promise of savings.</p>
<p>Annual figures are scaled up from the valid readings. With less than about 11 months of good data they're marked as indicative, and with less than six months they aren't shown.</p>

<h2 id="findings">6. Findings</h2>
<p>Each finding has two separate ratings. <strong>Impact</strong> shows how much it matters, based on cost and share of total use. <strong>Confidence</strong> shows how reliable the evidence is, based on data quality and whether the opening hours are confirmed. A finding with high impact and low confidence is worth checking before you quote it.</p>

<h2 id="capacity">7. Capacity and headroom</h2>
<p>Enter your agreed supply capacity (in kVA, from your bill or connection agreement) and an assumed power factor. The analyser compares every half hour with it and works out how much extra constant load the site could take before reaching the limit. Treat this as an early check, because only your network operator can confirm it.</p>

<h2 id="limits">What it can't tell you</h2>
<ul><li>Data from the main meter shows when electricity is used, but not which equipment is using it. Findings are things to check on site.</li><li>Figures are not adjusted for weather or changes in occupancy.</li><li>Carbon figures use a single conversion factor for the year, which you enter.</li></ul>
''' + related([('example-office-analysis.html', 'Worked example', 'The method applied to one office, step by step.'),
               ('out-of-hours-electricity.html', 'Out-of-hours use', 'Finding and reducing use while the building is closed.'),
               ('base-load.html', 'Base load', 'What always runs, and why it matters.')]), '''    <nav class="toc" aria-label="On this page"><div class="toc-title">On this page</div><ol>
      <li><a href="#files">Reading your files</a></li><li><a href="#checks">Checking the data</a></li><li><a href="#calendar">Opening hours</a></li><li><a href="#base">Base load and use while closed</a></li><li><a href="#costs">Costs and annual figures</a></li><li><a href="#findings">Findings</a></li><li><a href="#capacity">Capacity and headroom</a></li><li><a href="#limits">What it can't tell you</a></li></ol></nav>''')
  + cta('Try it on your own data', "It's free, there's no sign-up, and nothing is uploaded."))

# ── GET YOUR DATA ───────────────────────────────────────────────────────
GET_DATA_FAQS = [
    ('What is half-hourly electricity data?', "A record of the electricity used in each half hour of the day. That's 48 readings a day and 17,520 in a normal year. It shows when a site uses electricity as well as how much."),
    ('How far back can I get data?', 'Ask for at least 12 months, and up to three years if your supplier has it. A full year shows seasonal patterns and means annual figures are measured rather than estimated.'),
    ('Does it cost anything to get my data?', 'Ask your supplier. Many provide it free on request or through your online account.'),
    ('Where do I find my MPAN?', 'On your electricity bill. It is the 13-digit supply number, usually in a box labelled S or "Supply number".'),
]

PAGES['get-your-data.html'] = ('How to get your half-hourly electricity data',
  'Where to find your half-hourly (HH) electricity data, who to ask, what to ask for and which file formats the analyser reads.',
  page_hero('Guide', 'How to get your half-hourly data',
            "Most organisations already have this data. It just isn't shown on the bill. Here's where to find it and what to ask for.",
            crumbs=[HOME, GUIDES, ('Getting your half-hourly data', 'get-your-data.html')]) +
  guide(updated_line() + '''
<p class="answer">Ask your electricity supplier for the half-hourly consumption data for each of your meters, covering at least the last 12 months, as a spreadsheet. Many suppliers also let you download it from your online account.</p>

<h2 id="who">Who has it</h2>
<p>If your meter records half-hourly readings, your <strong>supplier</strong> receives them and can send them to you. Larger business sites have had half-hourly meters for years, and more meters are moving to <a href="half-hourly-settlement.html">half-hourly settlement</a>, so it's worth asking even for smaller premises.</p>
<p>You may also find it in:</p>
<ul><li><strong>Your supplier's online account</strong>, often under "consumption", "usage" or "data download"</li><li><strong>Your energy broker or energy manager</strong>, if you have one</li><li><strong>A building management or energy monitoring system</strong> that can export meter data</li><li><strong>A smart meter app or service</strong> that offers half-hourly downloads</li></ul>

<h2 id="ask">What to ask for</h2>
<p>A request like this works:</p>
<div class="note"><strong>Example request</strong><br>Please send the half-hourly consumption data (kWh) for meter [MPAN], from [date] to [date], as an Excel or CSV file with one row per day and 48 half-hourly columns.</div>
<ul><li><strong>One file per meter.</strong> Name each file after the site, because the analyser uses the file name as the site name.</li><li><strong>At least 12 months of data</strong>, so annual figures and seasonal patterns are reliable. Up to three years helps show longer-term trends.</li><li><strong>Readings in kWh for each half hour</strong> are best. Files in kW also work, and the analyser tells you which it found.</li></ul>
<p>Your meter's MPAN (the 13-digit supply number) is on your electricity bill.</p>
<p><a href="downloads/half-hourly-data-request.docx" download><strong>Download a letter template</strong></a> (Word). It lists what to ask for, with spaces for your MPANs and dates.</p>

<h2 id="formats">File formats the analyser reads</h2>
<div class="table-wrap"><table><thead><tr><th>Layout</th><th>Looks like</th></tr></thead><tbody>
<tr><td>Day per row</td><td>Date, then 48 columns of half-hourly readings</td></tr>
<tr><td>Day per column</td><td>Dates across the top, 48 rows of readings</td></tr>
<tr><td>Timestamped</td><td>One row per reading, with its date and time</td></tr></tbody></table></div>
<p>Excel (.xlsx, .xls) and CSV files both work. Extra columns, such as meter references, are ignored. If a file can't be read, the analyser explains why.</p>
<p>Not sure what your file should look like? <a href="samples/example-office.csv" download>Download our example file</a> and compare.</p>
''' + guide_download('Got your file?') + '''

<h2 id="no-data">If your supplier can't provide it</h2>
<p>If your supplier says the meter doesn't record half-hourly readings, ask whether it can be replaced with a smart or advanced meter that does. In the meantime, check whether a building management or monitoring system on site keeps its own records. Monthly meter readings will show how use changes through the year, but they can't show the daily and overnight patterns this analyser looks for.</p>
''' + faq_section(GET_DATA_FAQS) + related([
    ('example-office-analysis.html', 'Worked example', 'What a year of data shows about one office.'),
    ('out-of-hours-electricity.html', 'Out-of-hours use', 'The first thing to look at once you have the data.'),
    ('how-it-works.html', 'How the analyser works', 'What it does with your file, step by step.')]), '''    <nav class="toc" aria-label="On this page"><div class="toc-title">On this page</div><ol><li><a href="#who">Who has it</a></li><li><a href="#ask">What to ask for</a></li><li><a href="#formats">File formats the analyser reads</a></li><li><a href="#no-data">If your supplier can't provide it</a></li></ol></nav>''')
  + cta('Got your file?', 'Load it now. It takes about a minute and the data stays on your computer.'))

# ── FAQ ─────────────────────────────────────────────────────────────────
FAQ = [
  ('Using the analyser', [
    ('Can I use it for my home?', 'No. The site and the analyser are built for business and public sector buildings, with opening hours, closures and supply capacity in mind, so the results wouldn\'t mean much for a household. For advice on home energy use and bills, <a href="https://www.citizensadvice.org.uk/consumer/energy/" rel="noopener">Citizens Advice</a> is a good place to start.'),
    ('Is it really free?', "Yes. There's no charge, no account and no limit on the number of sites. If you'd like help acting on the results you can contact us, but there's no obligation."),
    ('Do I need to install anything?', "No. It runs in Chrome or Edge on a recent computer. It isn't designed for phones, because the charts need a larger screen."),
    ('How many sites can I load?', 'As many as your computer can handle. Each meter file becomes a site, and the analyser ranks them so you know which to look at first.'),
    ('Is there a user guide?', f'Yes. <a href="{GUIDE_PDF}" download>Download the user guide</a> (PDF). It takes you through getting your data, loading it, setting opening hours, reading the results, downloading reports and creating customer dashboards.'),
    ('Can I save my work?', 'Yes. Save a project file to your computer and open it again later. It contains the readings and all your settings, so store it as carefully as the original data.'),
    ('Can I share results with a client or colleague?', "Yes. You can download a PDF report for one site or your whole portfolio, export to Excel, or create a customer dashboard. That's a password-protected copy of the analyser containing only their sites."),
  ]),
  ('Your data', [
    ('Is my data uploaded anywhere?', 'No. The analysis runs entirely in your web browser. Your meter files are read on your own computer and nothing is sent to us or anyone else. Once the page has loaded you can even disconnect from the internet and keep working.'),
    ('What data do I need?', 'Half-hourly electricity readings for each meter, ideally covering 12 months or more. <a href="get-your-data.html">Here is how to get them.</a>'),
    ('What if my file has gaps or errors?', 'The analyser finds them before showing any figures. Missing readings are left out rather than counted as zero, and days with zero readings or clock changes are flagged for you to decide on.'),
  ]),
  ('The results', [
    ('Are the costs savings?', 'No. They show what a pattern costs now at the rates you entered. Any saving depends on what you change. The savings estimates are clearly labelled as estimates.'),
    ('How accurate is it?', "It's as accurate as the data and opening hours you give it. Each finding shows a confidence rating and the evidence behind it, and each figure is labelled as measured or estimated."),
    ('Can it tell me which equipment is wasting energy?', 'No. Data from the main meter shows when electricity is used, but not what is using it. The findings tell you when and where to look, and a visit to the building finds the cause.'),
  ]),
]
PAGES['faq.html'] = ('Questions and answers | Half Hourly Insights',
  'Common questions about the free half-hourly electricity analyser: cost, privacy, the data you need and what the results mean.',
  page_hero('FAQ', 'Questions and answers', 'If your question isn\'t answered here, <a href="contact.html" style="color:var(--blue);text-decoration:underline">ask us</a>.') +
  '<section class="section"><div class="section-inner" style="max-width:820px">' +
  ''.join(f'<h2 class="faq-group">{g}</h2><div class="faq">' + ''.join(
      f'<details><summary>{q}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in items) + '</div>'
          for g, items in FAQ) +
  '</div></section>' + cta('Still have a question?', 'Try the analyser with the example file, or get in touch.'))

# ── CONTACT ─────────────────────────────────────────────────────────────
PAGES['contact.html'] = ('Contact | Half Hourly Insights',
  'Talk to an energy expert about your half-hourly results, a full energy audit or help reducing out-of-hours use across your sites.',
  page_hero('Contact', 'Talk to an expert',
            "The analyser shows you where to look. If you'd like help turning the findings into savings, tell us about your sites and we'll be in touch. There's no obligation.") +
  f'''<section class="section"><div class="section-inner contact-grid">
<div class="contact-info">
  <a href="{OPERATOR_URL}" target="_blank" rel="noopener noreferrer" class="kec-logo-link">
    <span class="kec-sponsored-by">Sponsored by</span>
    <img src="images/kec-logo.svg" alt="{OPERATOR}" class="kec-logo-img" width="220" height="105">
  </a>
  {photo('contact-photo', 'A laptop showing an electricity demand chart on a desk, beside a printed report and a notebook')}
  <h2>{CONTACT_NAME}</h2>
  <p>Get in touch to talk through your results, or for help reducing out-of-hours use across your sites. We aim to reply within one working day.</p>
  <dl class="contact-details">
    <div><dt>Email</dt><dd><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></dd></div>
    <div><dt>Response time</dt><dd>Within 1 working day</dd></div>
    <div><dt>Coverage</dt><dd>Across the UK</dd></div>
  </dl>
</div>
<form class="form" id="enquiry" method="POST" action="{FORM_ENDPOINT}">
  <input type="hidden" name="_subject" value="New Half Hourly Insights enquiry">
  <input type="hidden" name="site" value="Half Hourly Insights">
  <p class="hp"><label>Leave this empty <input name="_gotcha" tabindex="-1" autocomplete="off"></label></p>
  <div class="form-row">
    <div><label for="name">Name <span class="req">*</span></label><input id="name" name="name" autocomplete="name" required></div>
    <div><label for="email">Email <span class="req">*</span></label><input id="email" name="email" type="email" autocomplete="email" required></div>
  </div>
  <div class="form-row">
    <div><label for="org">Organisation</label><input id="org" name="organisation" autocomplete="organization"></div>
    <div><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
  </div>
  <div class="form-row">
    <div><label for="sector">Sector</label><select id="sector" name="sector"><option value="">Choose one</option><option>Education</option><option>Local authority</option><option>Healthcare</option><option>Leisure</option><option>Commercial offices</option><option>Industrial</option><option>Retail and hospitality</option><option>Other</option></select></div>
    <div><label for="sites">Number of sites</label><select id="sites" name="sites"><option value="">Choose one</option><option>1</option><option>2 to 10</option><option>11 to 50</option><option>More than 50</option></select></div>
  </div>
  <div><label for="message">How can we help? <span class="req">*</span></label><textarea id="message" name="message" required placeholder="For example: we ran our 12 schools through the analyser and would like help with the out-of-hours findings."></textarea>
  <p class="help">Please don't paste meter data here. If we need it, we'll agree a secure way to share it.</p></div>
  <label class="check"><input type="checkbox" name="consent" value="yes" required> <span>I agree to you storing these details to reply to my enquiry, as set out in the <a href="privacy.html" style="color:var(--blue);text-decoration:underline">privacy notice</a>. <span class="req">*</span></span></label>
  <p class="form-error" role="alert" hidden></p>
  <div><button class="btn btn-gold btn-lg" type="submit">Send enquiry</button></div>
  <p class="help">If the form doesn't work for you, email <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> instead. Please don't attach meter files.</p>
</form>
</div></section>
<script>
// Send the enquiry to Formspree, then show our own thank-you page.
// Without JavaScript the form posts to Formspree directly.
document.getElementById('enquiry').addEventListener('submit', async (e) => {{
  e.preventDefault();
  const form = e.target, btn = form.querySelector('button[type=submit]'), err = form.querySelector('.form-error');
  btn.disabled = true; btn.textContent = 'Sending…'; err.hidden = true;
  try {{
    const res = await fetch(form.action, {{ method: 'POST', body: new FormData(form), headers: {{ Accept: 'application/json' }} }});
    if (res.ok) {{ window.location.href = 'thanks.html'; return; }}
    const data = await res.json().catch(() => ({{}}));
    err.textContent = (data.errors || []).map((x) => x.message).join(' ') || 'Something went wrong. Please try again, or email us instead.';
  }} catch {{
    err.textContent = 'We could not send your enquiry. Please check your connection and try again, or email us instead.';
  }}
  err.hidden = false; btn.disabled = false; btn.textContent = 'Send enquiry';
}});
</script>''')

PAGES['thanks.html'] = ('Thank you | Half Hourly Insights', 'Your enquiry has been sent.',
  page_hero('Contact', 'Thank you', 'Your enquiry has been sent. We\'ll reply by email, usually within one working day.',
            '\n    <a href="analyser/" class="btn btn-gold btn-lg">Back to the analyser</a>'),
  '  <meta name="robots" content="noindex">\n')

# ── PRIVACY ─────────────────────────────────────────────────────────────
PAGES['privacy.html'] = ('Privacy | Half Hourly Insights',
  'How Half Hourly Insights handles your data: meter files never leave your computer, and enquiry details are only used to reply.',
  page_hero('Privacy', 'Privacy notice', 'In short, your meter data never leaves your computer. If you contact us, we only use your details to reply.') +
  guide(f'''
<h2 id="analyser">The analyser</h2>
<p>The analyser runs entirely in your web browser. Meter files you load are read on your own computer. They are never uploaded and we never see them. The same goes for everything you enter (opening hours, rates, notes) and everything you download (PDFs, spreadsheets, project files and customer dashboards).</p>
<p>The analyser stores nothing in your browser between visits. Save a project file if you want to come back to your work.</p>

<h2 id="enquiries">Enquiries</h2>
<p>If you send the contact form, we receive the details you enter: your name, email, organisation, phone, sector, number of sites and message. We only use them to reply to your enquiry and any follow-up you ask for. We don't sell them or add you to a mailing list.</p>
<p>{OPERATOR} is responsible for the details you send (the data controller). The form is sent through Formspree, a form-handling service, which emails your enquiry to us and keeps a copy in our Formspree account on our behalf. Formspree may process data outside the UK; its own privacy policy explains how.</p>
<p>We keep enquiry details only for as long as we need them to deal with your enquiry and any follow-up you ask for. We then delete them, from our email and from Formspree, unless we have to keep them for a legal reason. You can ask us to delete them sooner at any time.</p>

<h2 id="cookies">Cookies and tracking</h2>
<p>This site sets no cookies and runs no advertising or tracking scripts. Fonts are served from this site rather than a third party.</p>

<h2 id="rights">Your rights</h2>
<p>You can ask what we hold about you, and ask us to correct or delete it, by emailing <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>. You can also complain to the Information Commissioner's Office (ico.org.uk).</p>
'''))

# ── SAMPLE REPORT ───────────────────────────────────────────────────────
# Figures are the office worked example (site/samples/example-office.csv) as
# the analyser reports them. Keep the two pages in step.
PAGES['sample-report.html'] = ('Sample electricity report for an office | Half Hourly Insights',
  'A sample half-hourly electricity report for a made-up UK office: use while closed, base load, findings and what could be saved.',
  page_hero('Sample report', 'What a report looks like',
            'See the kind of results the analyser produces before you find your own meter data. This is a made-up office with made-up readings.',
            crumbs=[HOME, ('Sample report', 'sample-report.html')]) +
  f'''<section class="section"><div class="section-inner sample">
<div class="note"><strong>Made-up example.</strong> The office and its meter readings are invented, so nothing here is a real customer's result. Every figure is what the analyser reports for our example file, at an illustrative 25p/kWh.</div>

<h2 class="section-title">The year at a glance</h2>
<p class="section-lead">A small office, open 07:00 to 19:00 on weekdays, with 363 days of valid readings.</p>
<div class="stat-grid">
  <div><strong>79,191 kWh</strong><span>electricity used in the year, costing about £19,798</span></div>
  <div><strong>33%</strong><span>of it used while the office was closed</span></div>
  <div><strong>2.6 kW</strong><span>base load: what never switches off</span></div>
  <div><strong>£2,776</strong><span>a year spent on use while closed, above the base load</span></div>
</div>

<figure class="figure"><img src="images/heatmap-office.png" width="2464" height="896" alt="Heatmap of the office year: a dark weekday band, pale nights, and some busy Saturdays" loading="lazy"><figcaption>Every half hour of the year on one chart: one column per day, darker for higher demand. The weekday band is clear, and some Saturdays are as busy as weekdays.</figcaption></figure>

<h2 class="section-title">What the analyser found</h2>
<div class="finding-grid">
  <article class="finding">
    <span class="finding-tag high">High impact</span>
    <h3>Use while closed</h3>
    <p class="finding-value">£2,776 a year</p>
    <p>11,035 kWh used outside opening hours, above the base load. Almost half of it (5,155 kWh) is on Saturdays; weekday evenings and nights add 3,750 kWh.</p>
    <p><strong>What to check:</strong> whether the office is used on Saturdays, and the heating and ventilation schedules.</p>
  </article>
  <article class="finding">
    <span class="finding-tag medium">Medium impact</span>
    <h3>Bank holidays like working days</h3>
    <p class="finding-value">7 bank holidays</p>
    <p>Seven bank holidays, including Christmas Day, used at least 80% of a normal weekday's electricity (1,408 kWh above base load in all).</p>
    <p><strong>What to check:</strong> whether the building controls know about bank holidays.</p>
    <p class="finding-note">Already included in the £2,776.</p>
  </article>
  <article class="finding">
    <span class="finding-tag low">Low impact</span>
    <h3>Early starts and late finishes</h3>
    <p class="finding-value">£629 a year</p>
    <p>About 1,250 kWh above base load in the two hours before opening, and the same again in the two hours after closing.</p>
    <p><strong>What to check:</strong> timer and heating start-up settings.</p>
    <p class="finding-note">Already included in the £2,776.</p>
  </article>
</div>
<p>The smaller findings are parts of the £2,776, not extra to it, so don't add them up. The base load is separate: 2.6 kW running all year costs about £5,700.</p>

<h2 class="section-title">What could actually be saved?</h2>
<p>The figures above are what each pattern costs now. They are not a promised saving. What you save depends on what you change, and some of that closed-hours use may turn out to be needed, such as a regular Saturday team. The way to find out is to:</p>
<ol class="sample-steps">
  <li><strong>Confirm the opening hours.</strong> If Saturdays are planned working days, much of the £2,776 is normal use.</li>
  <li><strong>Walk round the building</strong> on a Saturday and after closing time, and note what's switched on.</li>
  <li><strong>Change one setting at a time</strong>, such as the heating schedule or bank holiday calendar.</li>
  <li><strong>Compare the weeks before and after</strong> with the analyser's before-and-after view. That gives you a measured saving rather than an estimate.</li>
</ol>

<div class="sample-cta">
  <a class="btn btn-gold btn-lg" href="analyser/">Analyse my own data</a>
  <a class="btn btn-outline btn-lg" href="samples/example-office.csv" download>Download the example file</a>
</div>
<p>For the full method, figure by figure, read the <a href="example-office-analysis.html">worked example</a>. To understand your own figures, see <a href="how-it-works.html">how the analyser works</a>.</p>
</div></section>''' + cta('Ready to see your own results?', 'Load your half-hourly meter file. It takes about a minute and your data stays on your computer.'))

PAGES['404.html'] = ('Page not found | Half Hourly Insights', 'This page does not exist.',
  page_hero('404', 'Page not found', 'That page doesn\'t exist. Try the home page or open the analyser.',
            '\n    <a href="index.html" class="btn btn-gold btn-lg">Home</a>'),
  '  <meta name="robots" content="noindex">\n')




def core_pages():
    """The pages above, with breadcrumbs, schema and llms.txt lines."""
    home = ('Home', 'index.html')
    meta = {
        'index.html': dict(schema=[APP], section='Core pages',
                           summary='What the analyser shows, the three steps, and the privacy model (analysis runs in the browser).'),
        'how-it-works.html': dict(crumbs=[home, ('How it works', 'how-it-works.html')], article=True, section='Core pages',
                                  summary='The method in full: reading files, data checks, opening hours, base load (5th percentile), closed-hours excess, costs, annualisation, findings, capacity, and limits.'),
        'get-your-data.html': dict(crumbs=[home, ('Guides', 'guides.html'), ('Getting your half-hourly data', 'get-your-data.html')],
                                   article=True, faqs=GET_DATA_FAQS, section='Guides',
                                   summary='Who holds half-hourly data, what to ask your supplier for, the file layouts the analyser reads, and what to do if your supplier cannot provide it.'),
        'faq.html': dict(crumbs=[home, ('FAQ', 'faq.html')], faqs=[qa for _, items in FAQ for qa in items], section='Core pages',
                         summary='Cost, privacy, the data needed and what the results mean.'),
        'contact.html': dict(crumbs=[home, ('Contact', 'contact.html')], section='Core pages',
                             summary=f'Enquiries to {OPERATOR}, which runs the site.'),
        'thanks.html': dict(noindex=True),
        'privacy.html': dict(crumbs=[home, ('Privacy', 'privacy.html')]),
        'sample-report.html': dict(crumbs=[home, ('Sample report', 'sample-report.html')], section='Core pages',
                                   summary='A sample report for a made-up office: 33% of use while closed, £2,776 a year above base load, base load 2.6 kW, findings and what could be saved.'),
        '404.html': dict(noindex=True),
    }
    out = []
    for file, (title, desc, body, *extra) in PAGES.items():
        extra_head = (extra[0] if extra else '').replace('  <meta name="robots" content="noindex">\n', '')
        out.append(Page(file, title, desc, body, extra_head=extra_head, **meta.get(file, {})))
    return out
