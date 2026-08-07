# Shubham Gade — Academic Website Release Candidate V8

A minimalist academic portfolio for **Shubham Gade**, built with Astro for GitHub Pages.

## Public identity

- **Visible name:** Shubham Gade
- **Role:** PhD Researcher
- **Professional identity:** Agricultural Engineer · Precision Agriculture Researcher
- **Institution:** Asian Institute of Technology (AIT), Thailand
- **Website:** `https://shubham-anil-gade.github.io`
- **ORCID:** `0000-0003-1671-8394`
- **Scopus Author ID:** `57226315750`

## Pages

- Home
- About
- Research
- Publications
- Projects
- Posts
- Awards & Recognition
- Contact
- Academic CV (PDF + DOCX)

## Repository name

Create the GitHub repository using the exact name:

`shubham-anil-gade.github.io`

For a user-site repository with this exact name, the configured `site` URL in `astro.config.mjs` is sufficient and no `/repo-name/` base path is required.

## Deploy to GitHub Pages

1. Create the repository `shubham-anil-gade.github.io`.
2. Upload the contents of this project folder to the repository root.
3. Use `main` as the default branch.
4. Open **Settings → Pages** and select **GitHub Actions** as the source.
5. Push/commit the files. `.github/workflows/deploy.yml` will install, build and deploy the Astro site.
6. Check the first workflow run under **Actions**. Do not announce the site until that run is green and the live URL has been checked on desktop and mobile.

### Build note

Astro is pinned to `5.18.0`. The deployment workflow explicitly uses Node 24, installs dependencies with `npm install`, builds with `npm run build`, uploads the generated `dist/` folder, and deploys it through GitHub Pages. A package lock could not be generated in the preparation environment because its package mirror did not expose Astro. After the first successful deployment, generate and commit `package-lock.json` from a normal internet-connected machine for more reproducible future builds.

## Blog workflow

A Markdown starter is included at:

`src/drafts/post-template.md`

The Posts page is intentionally launch-safe and does not pretend unpublished articles already exist. When a genuine post is ready, publish it under `src/pages/posts/` and add it to the RSS feed logic.

## Public CV

The release contains a sanitized public academic CV:

- `public/files/Shubham_Gade_Academic_CV.pdf`
- `public/files/Shubham_Gade_Academic_CV.docx`

It excludes the private phone numbers, residential address and personal Gmail address contained in the older source CV.

## Pre-launch audit

See `PRE_LAUNCH_AUDIT_V8.md` for the full content, publication, awards, mobile, accessibility, SEO and deployment audit.
