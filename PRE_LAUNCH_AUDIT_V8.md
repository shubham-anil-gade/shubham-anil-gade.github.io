# Pre-launch Audit — Shubham Gade Academic Website V8

Audit date: August 2026

## Executive status

**Release-candidate status: READY FOR FIRST GITHUB PAGES BUILD**

The content, layout, internal navigation, publication record, award links, mobile behavior, accessibility basics and GitHub Pages configuration have been reviewed. Two items can only be completed after the site has a live URL: (1) confirming the first GitHub Actions build/deployment succeeds in the public repository, and (2) Google Search Console/indexing.

---

## 1. Final content audit — PASS

### Changes checked

- The homepage now makes **Shubham Gade** the primary visual identity.
- The line **“Engineering smarter agriculture through sensing and resource management.”** is a secondary heading.
- About, Research, Projects, Publications, Awards, Posts and Contact have distinct page roles instead of repeating the same narrative.
- Exact long-sentence duplication across page source was checked; no material duplicate long passages were found.
- Visible research photographs are no longer recycled across several page sections. Current visible use is one primary placement per research image.
- The homepage contains three selected publication highlights; the Publications page contains the full verified public publication record used for this release.
- The Posts page remains intentionally honest: no placeholder article is presented as already published.

### Identity and academic chronology checked against supplied CV

- PhD, Agricultural Systems and Engineering, AIT: **2023–2026 expected**.
- M.Tech., Irrigation and Drainage Engineering: **2018–2020**.
- B.Tech., Agricultural Engineering: **2014–2018**.
- Current website wording uses **PhD Researcher**, not “Dr.”.

---

## 2. Publications verification — PASS WITH DYNAMIC-PROFILE CAVEAT

The release lists **16 verified published items** plus **1 separately labelled public preprint**. DOI/publisher targets were checked against publisher/DOI or bibliographic records during the audit.

### 2026

1. Non-stationarity and temporal dependence of seasonal and extreme rainfall in Thailand and their linkages with ENSO and IOD — *Theoretical and Applied Climatology* — `10.1007/s00704-026-06315-7`
2. Agriculture and virtual water trade: Hidden impacts — Elsevier book chapter — `10.1016/B978-0-443-45116-4.00011-8`
3. Urbanization, industrialization, and water security: Theoretical perspectives and empirical evidence — Elsevier book chapter — `10.1016/B978-0-443-45116-4.00004-0`
4. Toward sustainable water security: A global spatiotemporal assessment of water scarcity and agricultural demand — Elsevier book chapter — `10.1016/B978-0-443-45116-4.00012-X`
5. A sustainable tool to mitigate water scarcity and air pollution in urban areas... — Elsevier book chapter — `10.1016/B978-0-443-41741-2.00002-8`

### 2025

6. Advancements in UAV remote sensing for agricultural yield estimation... — *Remote Sensing Applications: Society and Environment* 37, 101418 — `10.1016/j.rsase.2024.101418`
7. A systematic review on rainfall patterns of Thailand... — *Earth-Science Reviews* 264, 105102 — `10.1016/j.earscirev.2025.105102`
8. Assessing the Effects of Spatial Variability of Field Microtopography... — *Water Conservation Science and Engineering* 10:21 — `10.1007/s41101-025-00345-4`
9. Water footprints as a tool for integrated water resource management — Elsevier chapter — `10.1016/B978-0-443-30054-7.00006-9`

### 2024–2021

The remaining journal/chapter entries were cross-checked against DOI or publisher records. Two Pharma Innovation Journal papers use publisher-page links because a DOI was not established in the audit.

### Preprint

“The Potential of Weather and Climate Information Services to Support Small-Scale Agriculture in Thailand and Vietnam” is shown separately as a **Preprint (SSRN)**, DOI `10.2139/ssrn.5347196`, not mixed with peer-reviewed publications.

### Important maintenance rule

Google Scholar, Scopus, ResearchGate and ORCID are dynamic. The website record is accurate to the August 2026 audit but should be updated whenever a new paper is formally published or a preprint changes status.

---

## 3. Awards verification — PASS

Seven awards/recognitions are displayed. Verified official institutional pages are linked where a specific announcement was located:

- 2026 — 1st Prize, Oral Presentation, 4th Roorkee Water Conclave — official AIT news page.
- 2025 — Best Presentation Award, Hohai University International Summer Program — official AIT news page.
- 2025 — 2nd Prize, AIT Decarbonization Nexus / SDG Research Competition — official AIT sustainability page.
- 2024 — 3rd Prize, Regenerative Agriculture poster competition — official AIT news page.
- 2024 — 2nd Prize, SDGs Research Competition — official AIT news page.
- 2023 — 2nd Prize, Sustainability Expo / AIT SDG Research Fair — supported by supplied academic CV; no specific public award announcement was verified, so it is intentionally not linked.
- 2023 — Best Young Professional Staff Award, ICAR-NIASM — supported by supplied academic CV; no specific public award announcement was verified, so it is intentionally not linked.

The Awards page explicitly explains why the last two entries are unlinked rather than sending visitors to weak/generic pages.

The homepage and Awards page use the same green hover/focus interaction language as the project cards.

---

## 4. Public CV — PASS / USER REVIEW RECOMMENDED

A new public academic CV was prepared for the website in PDF and DOCX form. It:

- removes residential address;
- removes private phone numbers;
- removes personal Gmail;
- retains institutional email and academic-profile identifiers;
- updates the public publication record used by the website;
- includes all seven awards;
- includes the ASIS portal contribution;
- preserves the supplied academic chronology and thesis wording.

The PDF was rendered and visually checked page-by-page for clipping/overlap. It is launch-safe, but the user should still read it once for personal preference before treating it as the final career CV.

---

## 5. Mobile / tablet / desktop QA — PASS

Test viewports included:

- Desktop: 1440 × 1000
- Tablet: 768 × 1024
- Mobile: 390 × 844

Pages visually inspected include Home, About, Research, Publications, Projects, Awards, Posts and Contact across representative desktop/mobile widths.

Checks:

- no material horizontal overflow;
- mobile navigation switches to hamburger at the intended breakpoint;
- homepage name remains dominant on desktop/tablet/mobile;
- publication titles wrap without clipping;
- long email address wraps safely;
- project detail layout stacks appropriately;
- awards remain legible on mobile;
- image crops remain usable at responsive sizes.

A generic horizontal-overflow safeguard is included in the release CSS.

---

## 6. Technical launch preparation — PASS WITH ONE BUILD CAVEAT

### Present

- Astro static-site configuration
- GitHub Pages site URL configured
- GitHub Actions deployment workflow
- favicon
- `robots.txt`
- `sitemap.xml`
- RSS route
- custom 404 page
- canonical URLs
- Open Graph metadata
- Twitter card metadata
- structured `Person` JSON-LD
- ORCID / Scholar / Scopus / ResearchGate / LinkedIn / GitHub `sameAs` links
- alt text on visible images
- one H1 per audited offline page
- no duplicate HTML IDs in the offline page audit
- focus-visible styling
- skip-to-content link
- accessible mobile-menu `aria-expanded`, `aria-controls`, Escape-close and link-close behavior
- external `target="_blank"` links use `noopener noreferrer` in production source
- internal offline link checker: no missing internal targets/fragments in the generated preview
- WCAG contrast spot checks passed for primary text, muted text and white-on-green combinations

### Build caveat

The preparation environment’s npm mirror did not expose Astro, so a fresh local `npm install`/Astro production compile could not be executed here. The source is pinned to Astro `5.18.0`, and the GitHub Actions workflow explicitly selects Node 24, npm and `npm run build`. The **first GitHub Actions run is therefore the final build validation gate** before announcing the site.

---

## 7. GitHub Pages deployment readiness — READY; LIVE DEPLOYMENT STILL TO DO

Repository should be named exactly:

`shubham-anil-gade.github.io`

Target URL:

`https://shubham-anil-gade.github.io`

Deployment workflow follows the official Astro/GitHub Pages pattern using `withastro/action` and `actions/deploy-pages`.

Before announcing the link:

1. Upload the release source to the repository root.
2. Select **GitHub Actions** under Settings → Pages.
3. Confirm the first Actions run is green.
4. Open every primary route on the live domain.
5. Test at least one DOI link, one award link, the ASIS portal link, email, profile links and CV.
6. Test the live mobile menu on a phone.

---

## 8. Google visibility / indexing — PREPARED; CAN ONLY COMPLETE AFTER GO-LIVE

Technical prerequisites are ready: crawlable pages, robots file, sitemap, canonical URLs and structured identity metadata.

After the site is live:

1. Add `https://shubham-anil-gade.github.io/` to Google Search Console.
2. Submit `https://shubham-anil-gade.github.io/sitemap.xml`.
3. Request indexing for Home, About, Research, Publications and Projects.
4. Add the website URL to ORCID, LinkedIn and ResearchGate; add it to Google Scholar/Scopus profile fields where available.
5. Add it to the academic CV and institutional profile where appropriate.
6. Recheck Google indexing after several days/weeks; ranking cannot be guaranteed.

---

## Additional requested changes — COMPLETED

### Homepage hierarchy

**Shubham Gade** is now the primary hero heading. The research motto is intentionally smaller and secondary.

### ASIS portal

The Projects page now explains the ASIS web portal contribution conservatively: datasets/geospatial outputs were contributed to the portal, and the official ASIS Team section identifies “Er. Shubham Gade, Young Professional-II.” It does **not** claim sole development of the portal architecture.

Official portal: `https://niam.res.in/asis/`

### Publications button

Homepage button now reads **View all publications →** and links to the complete Publications page.

### Awards hover

Awards use a green hover/focus treatment consistent with Research in Application project cards.

---

## Final recommendation

**Proceed to GitHub Pages deployment.** Do not do another broad redesign before launch. The only true pre-announcement blocker is a successful first GitHub Actions build and a short live-domain smoke test. Google Search Console follows after publication.
