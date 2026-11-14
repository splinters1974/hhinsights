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
| `tools/build_guide.py` | Builds the downloadable user guide (`site/downloads/half-hourly-insights-user-guide.pdf`) from `tools/guide/guide.html` and the screenshots in `tools/guide/img`. Run `python3 tools/build_guide.py` after editing the guide. |
| `analyser/` | Source of the analyser (React, TypeScript, Vite). |

## Updating the analyser

```
cd analyser
npm ci
npm test        # calculation checks
npm run build   # writes site/analyser/index.html
```

The engine is shared with the internal Data Analyser. Changes made there can be copied into `analyser/src`; this copy is branded Half Hourly Insights only.

## Who runs it

Run by Kinetic Energy Consulting, as with the UK Solar Calculator: the footer,
copyright, contact page ("Sponsored by" logo and Paul Johnston's contact card)
and privacy notice say so. These are set at the top of `tools/build_pages.py`.

## Publishing on GitHub Pages

`.github/workflows/pages.yml` publishes `site/` on every push to `main`. Turn it on once: Settings, Pages, Build and deployment, Source: **GitHub Actions**. The site is then at the root of the Pages address.

Until then (Source: deploy from a branch), the top-level `index.html` forwards visitors to `site/`.

## Before going live

- **Enquiry emails:** the contact form sends to Formspree, using the same form as the UK Solar Calculator (`FORM_ENDPOINT` in `tools/pages_core.py`), so enquiries arrive in the same inbox with the subject "New Half Hourly Insights enquiry". To send them elsewhere, create a new form in Formspree and change `FORM_ENDPOINT`.
- **Domain (to be confirmed):** set `SITE_URL` in `tools/kit.py` and rebuild. Every page then gets canonical and absolute share links, `robots.txt` points at the sitemap, and `sitemap.xml` is written. Then submit the sitemap in Google Search Console and Bing Webmaster Tools.
- **Privacy notice:** confirm how long enquiries are kept (marked in `tools/build_pages.py`, privacy section).
