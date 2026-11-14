# Half Hourly Insights

Free half-hourly electricity analysis for UK businesses and public bodies,
in the design language of uksolarcalculator.co.uk. The analyser runs entirely
in the visitor's browser: meter data is never uploaded.

## What's here

| Path | What it is |
| --- | --- |
| `site/` | The published website (Netlify publishes this folder, see `netlify.toml`). Plain HTML and CSS, no build step on the server. |
| `site/analyser/index.html` | The analyser: one self-contained page, built from `analyser/`. |
| `site/samples/example-office.csv` | A made-up year of half-hourly data for visitors to try. |
| `tools/build_pages.py` | Builds every page in `site/` from one layout (head, navigation, footer). Edit page text there, then run `python3 tools/build_pages.py`. |
| `analyser/` | Source of the analyser (React, TypeScript, Vite). |

## Updating the analyser

```
cd analyser
npm ci
npm test        # calculation checks
npm run build   # writes site/analyser/index.html
```

The engine is shared with the internal Data Analyser. Changes made there can be copied into `analyser/src`; this copy is branded Half Hourly Insights only.

## Before going live

- **Domain:** add canonical URLs, absolute Open Graph image URLs and a sitemap once the domain is fixed.
- **Enquiry form:** uses Netlify Forms (no third-party script). In Netlify, set form notifications to send to the inbox that should receive leads.
- **Privacy notice:** fill in who the data controller is and how long enquiries are kept (marked in `tools/build_pages.py`, privacy section).
- **Footer:** add the operating company's name and contact details.
