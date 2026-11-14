# Phase 1 website improvement plan

**Repository:** `splinters1974/hhinsights`  
**Planning branch:** `planning/phase-1-site-improvements-2026-11`  
**Prepared:** 14 November 2026  
**Status:** Proposed only. No production changes authorised.

## Objective

Make the site safe to promote by fixing enquiry handling and privacy wording, letting visitors see a useful sample without providing a meter file, introducing all 25 approved images, correcting search/share metadata, and testing the visitor journey and analyser.

## Release guardrail

- Do all implementation on this branch or dedicated child feature branches. Do not commit to `main`, merge, open an auto-merge, change GitHub Pages settings, or publish/deploy without Martyn's explicit approval.
- **Important:** check the repository's GitHub Pages build source and any CI before implementation. If GitHub Pages deploys every pushed branch, keep implementation local or on a non-deploying branch until approval. This planning-only Markdown file does not alter the site.
- Before any release, supply a changes summary, a visual before/after review, the test evidence, remaining risks and a rollback plan.

## Findings confirmed in repository source

1. `site/contact.html` contains a POST form with `data-netlify="true"` and `action="thanks.html"`. The public URL is GitHub Pages. Do **not** assume Netlify will process submissions there; verify where POST requests go, then fix and test actual delivery.
2. `site/privacy.html` contains the placeholder `[Retention period to be confirmed.]` and identifies Netlify as the submission processor. It must reflect the confirmed arrangement and a real retention policy.
3. The homepage (`site/index.html`) offers a synthetic CSV download and a worked example but not a clear one-click, preloaded demonstration route.
4. Current pages use JPG imagery under `site/images/`; the 25 PNG replacements are stored in the user's Google Drive folder `HH analyser images`, not yet integrated into this repo.
5. Sampled pages (`site/index.html`, `site/guides.html`, `site/contact.html`) use relative `og:image` paths and have no canonical link in the checked head sections. `site/robots.txt` exists; `site/sitemap.xml` was not found at the expected location. Verify other deployment locations before adding.
6. `site/how-it-works.html` already discloses analysis limitations, input data checks and calculation methods. Preserve its distinction between identified patterns and verified savings.

## Workstream 1 — Enquiries and conversion (P0)

**Proposed changes**
- Confirm the desired inbox and the form provider, data processor, anti-spam controls and hosting arrangements. Pick one service that works from GitHub Pages (or deliberately migrate hosting). Do not rely on HTML attributes alone.
- Wire the form to the chosen endpoint, keep validation and spam protection, and show a truthful confirmation only after successful submission.
- Add a clear failure state with a mailto fallback; avoid losing typed answers if submission fails.
- Test destination email, confirmation, spam filtering and mobile submission.
- Keep the direct email contact method visible.

**Acceptance:** a test submission reaches the agreed inbox with all required fields; failure never shows a false success; no test customer data is used; evidence recorded.

## Workstream 2 — Privacy and trust (P0)

**Proposed changes**
- Replace the retention placeholder with a confirmed retention period and explain the chosen form processor and purposes of processing.
- Confirm the data-controller identity, contact details, lawful basis, user rights and relevant third-party services, then review the privacy notice against actual implementation.
- Check any claims that meter files never leave the user's device by inspecting network activity during a complete analyser workflow (including report export and dashboards).
- Use a verified domain-based contact address if available; otherwise retain an accurate address rather than inventing one.
- Avoid claiming third-party security certification without evidence.

**Acceptance:** no placeholders; processor and retention wording match actual practice; site claims are supported by tests.

## Workstream 3 — Sample analysis experience (P1)

**Proposed changes**
- Make the homepage's second primary action **Explore a sample report**, alongside **Analyse my data**.
- Use the existing explicitly fictional office sample and derived report. Prefer a preloaded read-only demonstration that requires no upload or setup; if that is technically impractical, create a clearly marked example-results page first.
- Show three understandable investigations with electricity cost, evidence, confidence, methodology and what to check next; do not present indicative costs as guaranteed savings.
- Offer the analyser CTA after the sample and make the sample accessible by keyboard and on mobile.

**Acceptance:** first-time visitor can view a meaningful synthetic result without supplying data, and can find the method and the next action.

## Workstream 4 — All 25 approved images (P1)

**Source:** Google Drive folder `HH analyser images`, 25 individually named PNG files, across earlier batches. Check each file is the latest approved version before importing.

- Guide cards (12): `guides`, `get-your-data`, `example-office-analysis`, `example-school-analysis`, `reading-a-heatmap`, `out-of-hours-electricity`, `base-load`, `supply-capacity`, `proving-savings`, `half-hourly-settlement`, `glossary`, `how-it-works`.
- Sector cards (7): `schools-electricity`, `offices-council-buildings`, `leisure-centres`, `healthcare-electricity`, `industrial-warehouses`, `retail-hospitality`, `sectors`.
- Generic location replacements (2): `estate-town` (1600 × 1200), `town-street` (1600 × 900). No recognisable Bristol landmarks.
- Core pages (4): `faq`, `contact`, `contact-photo` (1200 × 900), `og-image`.

**Proposed changes**
- Inspect titles, artefacts, crop safe areas and exact dimensions. The graphics are AI-generated, and some are enlarged artwork; flag any not suitable for large displays.
- Convert to well-compressed WebP for on-page display and retain 1200 × 630 share-safe images. Generate 600px variants where appropriate.
- Map every image to corresponding site pages, update `src`, `srcset`, width/height and social metadata, and remove recognisable location references only where replaced.
- Do not accidentally overwrite a different hero image. Ensure meaningful editorial images have alt text and decorative thumbnail images use empty alt text appropriately.

**Acceptance:** all 25 assets accounted for; no broken image URLs, clipped essential text, unwanted brands or Bristol landmarks; responsive sizes and image dimensions verified.

## Workstream 5 — SEO and sharing (P1)

**Proposed changes**
- Add absolute canonical URL, `og:url`, and absolute `og:image` URL to indexable pages, consistently using the actual GitHub Pages project path unless a custom domain is approved.
- Audit title and description uniqueness, sitemap coverage and robots location relative to GitHub Pages project root. Generate `site/sitemap.xml` if needed, with absolute deployed URLs, excluding thank-you or other `noindex` pages.
- Review structured data for absolute URL consistency and correct business identity; do not add invented ratings, reviews or FAQ-rich-result claims.
- Confirm GitHub Pages paths and preview images through deployed HTTP checks. Verify Google Search Console property and request indexing only once the approved release is live.

**Acceptance:** no relative/404 preview-image URLs; sitemap resolves in deployed location; metadata and canonical references match public URLs.

## Workstream 6 — QA and release evidence (P0 before launch)

**Must-test journeys**
1. Desktop and mobile: homepage, navigation, guides, sectors and contact.
2. Form: valid, invalid, spam field, server/network failure and confirmation.
3. Sample: no uploaded data required, visibly fictional, findings understandable.
4. Analyser: CSV/XLSX layouts, meter units, duplicate/missing readings, zero days, UK clock changes, incomplete years, unconfirmed hours and error handling.
5. Findings: recalculation against a known synthetic dataset; confidence/impact and base-load figures; no double-counting in savings scenarios.
6. Outputs: PDFs, spreadsheets and customer dashboard protections; inspect for unintended outbound meter-data requests.
7. SEO: HTTP 200/404, canonical, metadata, images, sitemap, link checks.
8. Accessibility/performance: keyboard focus, contrast, alt text, narrow screens and basic Lighthouse/Core Web Vitals checks.

**Acceptance:** critical journeys pass; any unresolved issue is categorised by severity, with ownership and a release decision.

## Implementation sequence

1. **P0 safety fixes:** enquiries, privacy, hosting/deployment guardrails.
2. **P1 experience:** sample report and action hierarchy.
3. **P1 visual/SEO:** integrate 25 images, metadata and sitemap.
4. **Release gate:** tests, evidence, screenshot review, approvals and rollback instructions.

## Decisions needed before implementation

- Which inbox and form provider should receive enquiries? Confirm whether Netlify processing is intentionally deployed separately from the public GitHub Pages site.
- Confirm retention period, controller contact details and privacy owner.
- Confirm whether the current synthetic office data may be used for the one-click demonstration.
- Confirm whether GitHub Pages will remain the public host and whether a custom domain is planned.
- Confirm that the exact 25 images in the Drive folder are the final versions.

## Deliverables for approval

- A changed-files list and draft pull request summary (without merging).
- Desktop/mobile screenshots, example report journey and complete asset manifest.
- Form delivery evidence, privacy checks, automated/manual test results, SEO validation and residual risk list.
- A clear go/no-go request before anything goes live.
