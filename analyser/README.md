# Analyser source

The half-hourly analyser behind the website's /analyser/ page. `npm run build`
makes one self-contained HTML file and copies it to `../site/analyser/index.html`.
`npm test` runs the calculation checks; `npm run lint` checks the analyser code.

All analysis runs in the browser (`src/local/`): parsing, data quality,
calendars, findings, scenarios, PDFs and Excel. `src/standalone/` holds the
screens. The files under `src/components`, `src/api` and `src/App.tsx` are a
server-backed variant that the website build does not use.
