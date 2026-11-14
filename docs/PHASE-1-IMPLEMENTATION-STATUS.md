# Phase 1 implementation and release checklist

Prepared: 14 November 2026
Status: **Ready for review on a development branch; NOT approved for production**

Branch: `planning/phase-1-site-improvements-2026-11`
Public production branch: `main` (unchanged)
Netlify project: `halfhourlyinsights` (`63ad63f4-872f-4fa8-a21c-8c0d01546a81`)

## Completed in GitHub branch

- Added `site/sample-report.html`, a fictional small-office example visitors can read without uploading a file.
- Added an **Explore a sample report first** link on the homepage and adjusted the primary action to **Analyse my data**.
- Preserved the distinction between the cost of a pattern and a proven saving, and warned against adding overlapping findings together.
- Kept the existing Netlify form markup (rather than replacing it without evidence) and added a direct email fallback.
- Reworked the privacy notice to remove its unfinished retention-period placeholder and describe retention criteria, subject to business verification.
- Added canonical URLs and absolute Open Graph URLs/images across the reviewed indexable pages, using the Netlify site URL.
- Added `site/sitemap.xml` and its declaration in `site/robots.txt`; aligned the homepage canonical URL with the sitemap root.
- Imported and confirmed the presence of **all 25** approved image designs under `site/images/phase1/` and pointed content images on the relevant pages to them.
- Added `scripts/check-static-site.mjs` and a GitHub Actions workflow to check images, links, placeholders, sitemap and metadata on the planning branch.

## Image implementation note

All 25 approved designs have been exported as **native optimised JPEG or PNG files** and committed on this development branch. A development-only GitHub Actions workflow extracted the native files from self-contained SVG staging assets; it successfully committed them on the planning branch without touching `main`.

- Website image references now point to native files under `site/images/guides/` and `site/images/photos/`; the default preview is `site/images/og-image.png`.
- Existing Open Graph URLs now resolve to the new native image versions when this branch is eventually approved and deployed. No SVG social-preview dependency remains.
- Staging SVG wrappers in `site/images/phase1/` are retained solely to make generation reproducible. They are **not** used as page images.
- The originals remain in Google Drive under `HH analyser images`; compressed staging copies are in `Phase 1 web optimised assets (staging)`.
- A live browser and social-sharing check is still required after an approved deploy. This does not affect the completed native-image integration.

## Current Netlify form blocker (confirmed via connected Netlify project)

The Netlify project reports **Forms: not enabled**, and the form list returned **zero registered forms**. Although `site/contact.html` contains `data-netlify="true"`, this does not prove that submissions are being captured.

**Do not approve launch** until Netlify Forms is enabled on the correct project/deploy and a real test submission is received in the agreed inbox. Confirm anti-spam, confirmation redirect, submission notifications and whether the form processor and retention wording match the live setup.

No Netlify configuration was changed during this work.

## Tests completed without deployment

- Inspected metadata on 25 page files: canonical, absolute `og:url` and absolute social image URL present (the `thanks` page remains `noindex`).
- Confirmed all 25 staged SVG source files and all 25 native image files are present on the planning branch.
- Scanned reviewed pages for draft privacy placeholders: none identified.
- Reviewed which pages reference the new artwork, and that the sample route is linked from the homepage.
- Confirmed the branch is ahead of `main` with no commits pulled into production.
- Verified the development-only raster materialisation workflow committed the approved files; no live browser test has been claimed.

**GitHub Actions Phase 1 website checks completed successfully** on the draft pull request (run ID 43597918807). This validates the scripted static-site checks. A full deployed-browser or form submission session has not yet been verified.

## Release-blocking checks still required

1. **Form:** enable the site Forms feature and test real submission/email delivery; verify Netlify captures a record.
2. **Imaging:** verify the native JPG/PNG artwork, responsive cropping and social previews on a deployed preview or after approved production release.
3. **Data privacy:** the controller must approve the enquiry retention criteria and processor/consent wording.
4. **Analyser accuracy:** run sample CSV and an XLSX file; verify time-zone clock changes, gaps, duplicates, base load, cost figures, savings overlap and report exports.
5. **Browser/device:** test desktop and mobile navigation, layout, keyboard focus and contact submission; capture screenshots.
6. **SEO:** after approved deployment only, check live sitemap, robots, canonical URLs, social previews and Search Console indexing.
7. **Security/privacy:** verify meter data does not leave the browser throughout the complete workflow, including exports and dashboards.
8. **Approval:** compare branch against `main`, approve the change summary and rollback path. **No merge or production deployment without Martyn's explicit approval.**

## Suggested test commands after checking out the branch

```bash
node scripts/check-static-site.mjs
```

The GitHub Actions workflow `.github/workflows/phase1-static-qa.yml` runs the same static checks without deploying.

## Rollback

All implementation changes are isolated on the planning branch. Releasing requires an explicit merge or approved deployment. If post-release problems appear, revert the merge commit or restore the last known-good Netlify deploy, then re-check the form and core analyser journeys.
