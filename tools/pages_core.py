"""
The core pages: home, how it works, getting your data, FAQ, contact, thanks,
privacy and 404. Bodies are HTML; metadata for search and AI tools is added
in core_pages() at the bottom.
"""
from kit import (CONTACT_EMAIL, CONTACT_NAME, OPERATOR, OPERATOR_URL, SOLAR_URL, APP, Page,
                 cta, photo, faq_section, guide, page_hero, related, updated_line)

HOME = ('Home', 'index.html')
GUIDES = ('Guides', 'guides.html')

PAGES = {}

# ── HOME ────────────────────────────────────────────────────────────────
PAGES['index.html'] = ('Half Hourly Insights: free half-hourly electricity analysis',
  'Free analysis of UK half-hourly electricity data: out-of-hours use, base load, peaks against capacity and unusual days. Runs in your browser.',
  f'''<div class="hero-wrap">
<div class="hero-media" aria-hidden="true"><img src="images/hero-heatmap.jpg" width="1600" height="900" alt="" fetchpriority="high"></div>
<section class="hero" aria-labelledby="hero-h">
  <div class="hero-copy">
    <p class="hero-pre">Free for UK businesses and public bodies. No sign-up.</p>
    <h1 id="hero-h">Where is your electricity going?</h1>
    <p class="hero-lead">Load your half-hourly meter data. In a minute you can see what runs when the building is shut, what never switches off, how close you get to your supply capacity, and what each pattern costs at your rates.</p>
    <div class="hero-points">
      <div><strong>Findings first</strong><span>Ranked by cost, with the evidence behind each one</span></div>
      <div><strong>Many sites</strong><span>One file per meter, the whole estate ranked</span></div>
      <div><strong>Private</strong><span>Runs in your browser; nothing is uploaded</span></div>
    </div>
  </div>
  <div class="start-card">
    <h2>Start with your meter file</h2>
    <p>Excel or CSV, one file per meter. Day-per-row, day-per-column and timestamped layouts all work.</p>
    <a href="analyser/" class="btn btn-gold btn-lg">Open the analyser</a>
    <div class="start-result">
      <div class="k">From the example file (a made-up office)</div>
      <div class="big">33%</div>
      <div class="small">of its electricity used when the building was shut</div>
    </div>
    <p class="or">No data to hand? <a href="samples/example-office.csv" download>Download an example file</a> (a made-up office) and load that, or <a href="example-office-analysis.html">read the worked example</a>.</p>
  </div>
</section>
</div>

<section class="section">
  <div class="section-inner">
    <div class="head-row">
      <h2 class="section-title">The patterns a bill can't show you</h2>
      <p>A bill tells you how much. Half-hourly data tells you when, and that is where most avoidable use hides.</p>
    </div>
    <div class="reasons">
      <div><h3>Out-of-hours use</h3><p>Energy used when the building should be shut, above what never switches off. Usually the cheapest saving: controls and schedules, not capital.</p></div>
      <div><h3>Base load</h3><p>The demand that never goes away, overnight and at weekends. Every kilowatt of it runs all year, so small cuts add up.</p></div>
      <div><h3>Peaks and capacity</h3><p>Your highest half hours against your agreed supply capacity, and how much new load (heat pumps, EV charging) the site could take.</p></div>
      <div><h3>Unusual days</h3><p>Days that don't match their usual pattern, and lasting changes that show when something was left on, or a fix worked.</p></div>
      <div><h3>Bank holidays and weekends</h3><p>Days the site should be quiet but isn't, checked against the opening hours you set.</p></div>
      <div><h3>Savings scenarios</h3><p>What-ifs such as cutting out-of-hours use or lowering peak demand, without counting the same saving twice.</p></div>
    </div>
  </div>
</section>

<section class="section privacy-band">
  <div class="section-inner">
    <h2 class="section-title">Your data never leaves your computer</h2>
    <p class="section-lead">The analyser is one web page that does all its work in your browser. Meter files are read on your machine and nothing is sent to us or anyone else.</p>
    <div class="reasons">
      <div><h3>No upload</h3><p>There is no server doing the analysis. Once the page has loaded, you can switch off your connection and keep working.</p></div>
      <div><h3>No account</h3><p>No sign-up, no email address, no tracking cookies.</p></div>
      <div><h3>You keep the outputs</h3><p>PDFs, spreadsheets and project files save to your computer. Save a project to pick up where you left off.</p></div>
    </div>
  </div>
</section>

<section class="section band-mist">
  <div class="section-inner">
    <div class="split">
      <div>
        <span class="section-kicker">The analyser</span>
        <h2 class="section-title">Findings first, evidence underneath</h2>
        <p class="section-lead">Each site opens on its top three investigations, ranked by cost, with how confident the evidence is. Every figure says whether it was measured or estimated.</p>
        <ul class="ticks">
          <li><strong>Site and estate PDFs</strong> ready to send, plus Excel for your own analysis</li>
          <li><strong>A year at a glance:</strong> every half hour in one heatmap</li>
          <li><strong>Data checks</strong> for gaps, zero days, clock changes and duplicate rows before any figure is shown</li>
          <li><strong>Customer dashboards:</strong> a locked, password-protected copy to send to a client</li>
        </ul>
      </div>
      <div>
        <div class="shot"><img src="images/shot-site.png" width="1360" height="900" alt="The analyser showing a site's headline figures, energy split and top investigations" loading="lazy"></div>
        <p class="shot-caption">A site page from the example file. All data on this site is made up.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="section-inner">
    <div class="head-row">
      <h2 class="section-title">Three steps</h2>
      <p>No account, no installation. Works in Chrome or Edge on any recent computer.</p>
    </div>
    <div class="steps">
      <div><div class="step-head"><span class="step-n">1</span><span class="step-line"></span></div><h3>Load your files</h3><p>Drag in one file per meter. The analyser reads the layout, checks the data and tells you exactly what it found.</p></div>
      <div><div class="step-head"><span class="step-n">2</span><span class="step-line"></span></div><h3>Set the hours</h3><p>Tell it when each building is open. Out-of-hours findings depend on this, so it asks you to confirm.</p></div>
      <div><div class="step-head"><span class="step-n">3</span><span class="step-line"></span></div><h3>Read and share</h3><p>Work through the findings, then download PDFs, Excel or a customer dashboard.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="section-inner split">
    <div>
      <span class="section-kicker">Who it's for</span>
      <h2 class="section-title">Schools, offices, leisure centres, hospitals and businesses</h2>
      <p class="section-lead">Any building with a half-hourly meter. Every building type has its own normal, so the analyser compares each site with its own opening hours, not a benchmark.</p>
      <p style="margin-top:24px"><a href="sectors.html" class="btn btn-outline">What to look for in your sector</a></p>
    </div>
    <div>{photo('town-street', 'A town street with an energy centre, offices, a civic building, an electric bus and a car charging at a roadside charger')}</div>
  </div>
</section>

<section class="section band-mist">
  <div class="section-inner">
    <div class="head-row">
      <h2 class="section-title">Guides</h2>
      <p>Plain-English answers to the questions that come up when you first look at half-hourly data.</p>
    </div>
    <div class="link-grid" style="margin-top:36px">
      <a class="link-card" href="example-office-analysis.html"><h3>Worked example</h3><p>One office, one year of data, and what the analyser found.</p><span class="more">Read the example</span></a>
      <a class="link-card" href="out-of-hours-electricity.html"><h3>Out-of-hours use</h3><p>How to find electricity used when the building is shut, and cut it.</p><span class="more">Read the guide</span></a>
      <a class="link-card" href="base-load.html"><h3>Base load</h3><p>What never switches off, why it matters and how to bring it down.</p><span class="more">Read the guide</span></a>
      <a class="link-card" href="supply-capacity.html"><h3>Supply capacity</h3><p>kVA, your agreed capacity, and room for heat pumps and EV charging.</p><span class="more">Read the guide</span></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="section-inner split">
    <div><span class="section-kicker">Sister site</span><h2 class="section-title">Thinking about solar too?</h2></div>
    <div><p class="section-lead">Half-hourly data shows how much of your electricity you use in daylight hours, which is what on-site solar can supply. The <a href="{SOLAR_URL}" style="color:var(--blue);text-decoration:underline">UK Solar Calculator</a>, from the same team, estimates system size, savings and payback for your roof.</p></div>
  </div>
</section>

{cta('Want a second pair of eyes on the results?', 'The analyser shows where to look. If you want help turning findings into savings, or a full energy audit across your estate, get in touch.')}
''')

# ── HOW IT WORKS ────────────────────────────────────────────────────────
PAGES['how-it-works.html'] = ('How it works | Half Hourly Insights',
  'What the analyser does with your half-hourly data: how it reads files, checks quality, sets the base load, prices out-of-hours use and builds findings.',
  page_hero('How it works', 'What the analyser does with your data',
            'Plain-English notes on every step, from reading the file to the figures in the report. The full method is in the analyser itself: every finding has a "show calculation and evidence" link.',
            crumbs=[HOME, ('How it works', 'how-it-works.html')]) +
  guide(updated_line() + '''
<p class="answer">The analyser reads every half-hourly reading, checks it, works out what the site uses when it's open and when it's shut, and prices the difference at your rates. It shows where to look, not what to fix.</p>

<h2 id="files">1. Reading your files</h2>
<p>Load one file per meter, as Excel (.xlsx, .xls) or CSV. Three layouts work:</p>
<ul><li><strong>Day per row:</strong> a date, then 48 half-hourly readings (the most common supplier format).</li><li><strong>Day per column:</strong> the same, turned on its side.</li><li><strong>Timestamped:</strong> one reading per row with its date and time.</li></ul>
<p>The analyser tells you how it read each file: which column held the dates, whether readings were kWh or kW, and anything it ignored. Files covering more than a year are analysed over the last 12 months by default; you can pick any other period, and long-term trends still use the whole file.</p>

<h2 id="checks">2. Checking the data</h2>
<p>Before showing any figure, the analyser looks for problems that would make it wrong:</p>
<ul><li>missing readings and gaps (left out, never counted as zero)</li><li>days of zero readings, which usually mean a meter or data fault</li><li>clock-change days and duplicate rows, which it holds back for you to decide</li><li>single readings far above the normal peak</li></ul>
<p>Each site gets a verdict (Good, Check or Poor) and you can exclude anything you know is wrong, with a reason that's kept with the analysis.</p>

<h2 id="calendar">3. Opening hours</h2>
<p>Out-of-hours findings depend on knowing when a building should be open. Every site starts with typical office hours, clearly marked as unconfirmed. Set the hours for all sites at once or one by one, including closures, bank holidays and overnight shifts. Findings that rely on unconfirmed hours carry lower confidence.</p>

<h2 id="base">4. Base load and out-of-hours use</h2>
<p>The <strong>base load</strong> is the level the site rarely drops below: the 5th percentile of all valid half-hourly demand. It's what never switches off, such as servers, fridges and standby loads.</p>
<p><strong>Closed-hours excess</strong> is energy used while the site is shut, above that base load. This is the figure the analyser ranks sites by, because it is often the cheapest consumption to tackle: through controls, time clocks and building management settings rather than new equipment.</p>

<h2 id="costs">5. Costs and annual figures</h2>
<p>Costs are energy cost at the rates you enter: one flat rate, or time bands such as day and night. They exclude standing charges, capacity charges and other fixed costs. They show what a pattern costs now, not a guaranteed saving.</p>
<p>Annual figures are scaled from the valid readings. With less than about 11 months of good data they are marked indicative, and under six months they aren't shown at all.</p>

<h2 id="findings">6. Findings</h2>
<p>Each finding has two separate labels. <strong>Impact</strong> is how much it matters, based on cost and share of use. <strong>Confidence</strong> is how good the evidence is, based on data quality and whether the hours are confirmed. A high-impact, low-confidence finding is worth checking, not quoting.</p>

<h2 id="capacity">7. Capacity and headroom</h2>
<p>Enter your agreed supply capacity (in kVA, from your bill or connection agreement) and an assumed power factor. The analyser compares every half hour against it and works out how much constant new load the site could add before it runs short. It's a screen, not confirmation from your network operator.</p>

<h2 id="limits">What it can't tell you</h2>
<ul><li>Whole-site data shows when demand happens, not which equipment causes it. Findings are things to check on site.</li><li>Figures aren't adjusted for weather or changes in occupancy.</li><li>Carbon figures use the factor you enter, one value for the year.</li></ul>
''' + related([('example-office-analysis.html', 'Worked example', 'The method applied to one office, step by step.'),
               ('out-of-hours-electricity.html', 'Out-of-hours use', 'Finding and cutting use when the building is shut.'),
               ('base-load.html', 'Base load', 'What never switches off, and why it matters.')]), '''    <nav class="toc" aria-label="On this page"><div class="toc-title">On this page</div><ol>
      <li><a href="#files">Reading your files</a></li><li><a href="#checks">Checking the data</a></li><li><a href="#calendar">Opening hours</a></li><li><a href="#base">Base load and out-of-hours use</a></li><li><a href="#costs">Costs and annual figures</a></li><li><a href="#findings">Findings</a></li><li><a href="#capacity">Capacity and headroom</a></li><li><a href="#limits">What it can't tell you</a></li></ol></nav>''')
  + cta('See it on your own data', 'Free, no sign-up, and nothing is uploaded.'))

# ── GET YOUR DATA ───────────────────────────────────────────────────────
GET_DATA_FAQS = [
    ('What is half-hourly electricity data?', 'A reading of the electricity used in every half hour of the day: 48 readings a day, 17,520 in a normal year. It shows when a site uses power, not just how much.'),
    ('How far back can I get data?', 'Ask for at least 12 months, and up to three years if it is available. A full year shows seasonal patterns and lets annual figures be measured rather than estimated.'),
    ('Does it cost anything to get my data?', 'Ask your supplier. Many provide half-hourly data on request or through their online account at no charge.'),
    ('Where do I find my MPAN?', 'On your electricity bill. It is the 13-digit supply number, usually shown in a box labelled S or "Supply number".'),
]

PAGES['get-your-data.html'] = ('How to get your half-hourly electricity data',
  'Where to find your half-hourly (HH) electricity data, who to ask, what to ask for and which file formats the analyser reads.',
  page_hero('Guide', 'How to get your half-hourly data',
            'Most organisations already have the data; it just isn\'t on the bill. Here is where to find it and what to ask for.',
            crumbs=[HOME, GUIDES, ('Getting your half-hourly data', 'get-your-data.html')]) +
  guide(updated_line() + '''
<p class="answer">Ask your electricity supplier for half-hourly consumption data for each meter, for the last 12 months or more, as a spreadsheet. Many suppliers also let you download it from their online account.</p>

<h2 id="who">Who has it</h2>
<p>If your meter records half-hourly readings, your <strong>supplier</strong> receives them and can send them to you. Larger business sites have had half-hourly meters for years, and more sites are moving to half-hourly settlement, so it's worth asking even for smaller premises.</p>
<p>Other places to look:</p>
<ul><li><strong>Your supplier's online portal:</strong> often under "consumption", "usage" or "data download".</li><li><strong>Your energy broker or energy manager</strong>, if you have one.</li><li><strong>A building management or monitoring system</strong> that exports meter data.</li><li><strong>Smart meter data</strong> through an app or service that offers half-hourly downloads.</li></ul>

<h2 id="ask">What to ask for</h2>
<p>Something like this works:</p>
<div class="note"><strong>Example request</strong><br>Please send the half-hourly consumption data (kWh) for meter [MPAN], from [date] to [date], as an Excel or CSV file with one row per day and 48 half-hourly columns.</div>
<ul><li><strong>One file per meter.</strong> Name each file after the site; the name becomes the site name in the analyser.</li><li><strong>At least 12 months</strong>, so annual figures and seasonal patterns are reliable. Up to three years is useful for trends.</li><li><strong>kWh per half hour</strong> is ideal. kW files also work; the analyser tells you which it found.</li></ul>
<p>Your meter's MPAN (the 13-digit supply number) is on your electricity bill.</p>
<p><a href="downloads/half-hourly-data-request.docx" download><strong>Download a letter template</strong></a> (Word): a ready-to-edit request listing what to ask for, with spaces for your MPANs and dates.</p>

<h2 id="formats">Formats the analyser reads</h2>
<div class="table-wrap"><table><thead><tr><th>Layout</th><th>Looks like</th></tr></thead><tbody>
<tr><td>Day per row</td><td>Date, then 48 columns of half-hourly readings</td></tr>
<tr><td>Day per column</td><td>Dates across the top, 48 rows of readings</td></tr>
<tr><td>Timestamped</td><td>One row per reading, with its date and time</td></tr></tbody></table></div>
<p>Excel (.xlsx, .xls) and CSV are all fine. Extra columns such as meter references are ignored. If a file can't be read, the analyser says why.</p>
<p>Not sure what yours looks like? <a href="samples/example-office.csv" download>Download our example file</a> and compare.</p>
''' + faq_section(GET_DATA_FAQS) + related([
    ('example-office-analysis.html', 'Worked example', 'What a year of data shows about one office.'),
    ('out-of-hours-electricity.html', 'Out-of-hours use', 'The first thing to look at once you have the data.'),
    ('how-it-works.html', 'How the analyser works', 'What it does with your file, step by step.')]), '''    <nav class="toc" aria-label="On this page"><div class="toc-title">On this page</div><ol><li><a href="#who">Who has it</a></li><li><a href="#ask">What to ask for</a></li><li><a href="#formats">Formats the analyser reads</a></li></ol></nav>''')
  + cta('Got your file?', 'Load it now. It takes about a minute and stays on your computer.'))

# ── FAQ ─────────────────────────────────────────────────────────────────
FAQ = [
  ('Using the analyser', [
    ('Is it really free?', 'Yes. There is no charge, no account and no limit on the number of sites. If you want help acting on the results, you can contact us, but you don\'t have to.'),
    ('Do I need to install anything?', 'No. It runs in Chrome or Edge on a recent computer. It isn\'t designed for phones; the charts need a bigger screen.'),
    ('How many sites can I load?', 'As many as your computer will hold. One file per meter; each becomes a site, and the analyser ranks them so you know where to start.'),
    ('Can I save my work?', 'Yes. Save a project file to your computer and open it again later. It holds the readings and every setting, so treat it like the original data.'),
    ('Can I share results with a client or colleague?', 'Download the site or portfolio PDF, export to Excel, or make a customer dashboard: a locked, password-protected copy of the analyser holding just their sites.'),
  ]),
  ('Your data', [
    ('Is my data uploaded anywhere?', 'No. The analysis runs entirely in your browser. Meter files are read on your computer and nothing is sent to us or anyone else. You can disconnect from the internet once the page has loaded and keep working.'),
    ('What data do I need?', 'Half-hourly electricity readings for each meter, ideally 12 months or more. <a href="get-your-data.html">Here is how to get them.</a>'),
    ('What if my file has gaps or errors?', 'The analyser finds them before it shows any figure. Missing readings are left out, never counted as zero; zero days and clock-change days are flagged for you to decide on.'),
  ]),
  ('The results', [
    ('Are the costs savings?', 'No. They are what a pattern costs now at the rates you entered. A saving depends on what you change. The savings scenarios are what-ifs, clearly labelled.'),
    ('How accurate is it?', 'As accurate as the data and the opening hours you give it. Every finding shows its confidence and the evidence behind it, and every figure says whether it was measured or estimated.'),
    ('Can it tell me which equipment is wasting energy?', 'No. Whole-site data shows when energy is used, not by what. The findings tell you where and when to look; a site visit finds the cause.'),
  ]),
]
PAGES['faq.html'] = ('Questions and answers | Half Hourly Insights',
  'Common questions about the free half-hourly electricity analyser: cost, privacy, the data you need and what the results mean.',
  page_hero('FAQ', 'Questions and answers', 'If your question isn\'t here, <a href="contact.html" style="color:var(--blue);text-decoration:underline">ask us</a>.') +
  '<section class="section"><div class="section-inner" style="max-width:820px">' +
  ''.join(f'<h2 class="faq-group">{g}</h2><div class="faq">' + ''.join(
      f'<details><summary>{q}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in items) + '</div>'
          for g, items in FAQ) +
  '</div></section>' + cta('Still have a question?', 'Open the analyser with the example file to see how it works, or get in touch.'))

# ── CONTACT ─────────────────────────────────────────────────────────────
PAGES['contact.html'] = ('Contact | Half Hourly Insights',
  'Talk to an energy expert about your half-hourly results, a full energy audit or help reducing out-of-hours use across your estate.',
  page_hero('Contact', 'Talk to an expert',
            'The analyser shows where to look. If you\'d like help turning findings into savings, tell us a little about your sites and we\'ll be in touch. No obligation.') +
  f'''<section class="section"><div class="section-inner contact-grid">
<div class="contact-info">
  <a href="{OPERATOR_URL}" target="_blank" rel="noopener noreferrer" class="kec-logo-link">
    <span class="kec-sponsored-by">Sponsored by</span>
    <img src="images/kec-logo.svg" alt="{OPERATOR}" class="kec-logo-img" width="220" height="105">
  </a>
  <h2>{CONTACT_NAME}</h2>
  <p>Get in touch to talk through your results, or about help reducing out-of-hours use across your sites. Enquiries are typically responded to within one working day.</p>
  <dl class="contact-details">
    <div><dt>Email</dt><dd><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></dd></div>
    <div><dt>Response time</dt><dd>Within 1 working day</dd></div>
    <div><dt>Coverage</dt><dd>Nationwide across the UK</dd></div>
  </dl>
</div>
<form class="form" name="enquiry" method="POST" action="thanks.html" data-netlify="true" netlify-honeypot="company_url">
  <input type="hidden" name="form-name" value="enquiry">
  <p class="hp"><label>Leave this empty <input name="company_url" tabindex="-1" autocomplete="off"></label></p>
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
  <div><label for="message">How can we help? <span class="req">*</span></label><textarea id="message" name="message" required placeholder="For example: we ran our 12 schools through the analyser and want help with the out-of-hours findings."></textarea>
  <p class="help">Please don't paste meter data here. If we need it, we'll agree a safe way to share it.</p></div>
  <label class="check"><input type="checkbox" name="consent" value="yes" required> <span>I agree to you storing these details to reply to my enquiry, as set out in the <a href="privacy.html" style="color:var(--blue);text-decoration:underline">privacy notice</a>. <span class="req">*</span></span></label>
  <div><button class="btn btn-gold btn-lg" type="submit">Send enquiry</button></div>
</form>
</div></section>''')

PAGES['thanks.html'] = ('Thank you | Half Hourly Insights', 'Your enquiry has been sent.',
  page_hero('Contact', 'Thank you', 'Your enquiry has been sent. We\'ll reply by email, typically within one working day.',
            '\n    <a href="analyser/" class="btn btn-gold btn-lg">Back to the analyser</a>'),
  '  <meta name="robots" content="noindex">\n')

# ── PRIVACY ─────────────────────────────────────────────────────────────
PAGES['privacy.html'] = ('Privacy | Half Hourly Insights',
  'How Half Hourly Insights handles your data: meter files never leave your computer; enquiry details are used only to reply.',
  page_hero('Privacy', 'Privacy notice', 'Short version: your meter data never leaves your computer. If you contact us, we use your details only to reply.') +
  guide(f'''
<h2 id="analyser">The analyser</h2>
<p>The analyser runs entirely in your web browser. Meter files you load are read on your computer. They are not uploaded, and we never see them. The same applies to everything you enter (opening hours, rates, notes) and everything you download (PDFs, spreadsheets, project files and customer dashboards).</p>
<p>The analyser stores nothing in your browser between visits. Save a project file if you want to come back to your work.</p>

<h2 id="enquiries">Enquiries</h2>
<p>If you send the contact form, we receive the details you enter: your name, email, organisation, phone, sector, number of sites and message. We use them only to reply to your enquiry and any follow-up you ask for. We don't sell them or add you to a mailing list.</p>
<p>{OPERATOR} is responsible for the details you send (the data controller). The form is processed by our website host, Netlify, which stores submissions on our behalf. [Retention period to be confirmed.]</p>

<h2 id="cookies">Cookies and tracking</h2>
<p>This site sets no cookies and runs no advertising or tracking scripts. Fonts are served from this site, not a third party.</p>

<h2 id="rights">Your rights</h2>
<p>You can ask what we hold about you, ask us to correct it or delete it, by emailing <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>. You can also complain to the Information Commissioner's Office (ico.org.uk).</p>
'''))

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
                                  summary='The method in full: reading files, data checks, opening hours, base load (5th percentile), out-of-hours excess, costs, annualisation, findings, capacity, and limits.'),
        'get-your-data.html': dict(crumbs=[home, ('Guides', 'guides.html'), ('Getting your half-hourly data', 'get-your-data.html')],
                                   article=True, faqs=GET_DATA_FAQS, section='Guides',
                                   summary='Who holds half-hourly data, what to ask your supplier for, and the file layouts the analyser reads.'),
        'faq.html': dict(crumbs=[home, ('FAQ', 'faq.html')], faqs=[qa for _, items in FAQ for qa in items], section='Core pages',
                         summary='Cost, privacy, the data needed and what the results mean.'),
        'contact.html': dict(crumbs=[home, ('Contact', 'contact.html')], section='Core pages',
                             summary=f'Enquiries to {OPERATOR}, which runs the site.'),
        'thanks.html': dict(noindex=True),
        'privacy.html': dict(crumbs=[home, ('Privacy', 'privacy.html')]),
        '404.html': dict(noindex=True),
    }
    out = []
    for file, (title, desc, body, *extra) in PAGES.items():
        extra_head = (extra[0] if extra else '').replace('  <meta name="robots" content="noindex">\n', '')
        out.append(Page(file, title, desc, body, extra_head=extra_head, **meta.get(file, {})))
    return out
