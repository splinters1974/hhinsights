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

The approved designs were resized and compressed into optimised JPEG/PNG files, then embedded inside self-contained SVG image wrappers in `site/images/phase1`. This was used because the available GitHub text-file action supports UTF-8, not direct binary asset updates. Visually these contain the supplied artwork, and all 25 files exist on the branch.

- The `<img>` elements on the reviewed pages now point to these SVG wrappers.
- The **existing JPEG/PNG social preview URLs remain unchanged** because social platforms may not accept SVG for Open Graph images. Before release, check and preferably replace social JPEGs with matching 1200 × 630 native raster assets.
- Confirm SVG wrapper display on Netlify, Chrome, Edge and Safari, and check the page CSP. If a browser blocks embedded image data, restore the original JPG references or switch to native raster assets before release.
- The originals remain in Google Drive, under `HH analyser images`. Compressed JPEG staging copies are in `Phase 1 web optimised assets (staging)`.
- Do not describe the SVG wrappers as true vector drawings; they contain JPEG or PNG data.

## Current Netlify form blocker (confirmed via connected Netlify project)

The Netlify project reports **Forms: not enabled**, and the form list returned **zero registered forms**. Although `site/contact.html` contains `data-netlify="true"`, this does not prove that submissions are being captured.

**Do not approve launch** until Netlify Forms is enabled on the correct project/deploy and a real test submission is received in the agreed inbox. Confirm anti-spam, confirmation redirect, submission notifications and whether the form processor and retention wording match the live setup.

No Netlify configuration was changed during this work.

## Tests completed without deployment

- Inspected metadata on 25 page files: canonical, absolute `og:url` and absolute social image URL present (the `thanks` page remains `noindex`).
- Confirmed all 25 SVG artwork files exist on the planning branch.
- Scanned reviewed pages for draft privacy placeholders: none identified.
- Reviewed which pages reference the new artwork, and that the sample route is linked from the homepage.
- Confirmed the branch is ahead of `main` with no commits pulled into production.
- Rendered a locally generated example of the self-contained SVG image wrapper in a vector renderer (not a complete browser test).

**GitHub Actions Phase 1 website checks completed successfully** on the draft pull request (run ID 43597918807). This validates the scripted static-site checks. A full deployed-browser or form submission session has not yet been verified.

## Release-blocking checks still required

1. **Form:** enable the site Forms feature and test real submission/email delivery; verify Netlify captures a record.
2. **Imaging:** browser-test staged SVGs and ensure social share images display the approved designs, not older versions.
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
