# Attendly SEO Content System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a static SEO blog hub, FAQ hub, 20 attendance-focused articles, generated article visuals, structured metadata, and sitemap coverage to Attendly.

**Architecture:** Keep the existing static HTML/CSS/JS site. Generate the repetitive article HTML from one checked-in content generator so metadata, schema, breadcrumbs, internal links, and accessibility stay consistent. Store each generated article and image as a normal deployable static file.

**Tech Stack:** HTML, CSS, vanilla JavaScript, Python standard library for deterministic content generation, generated WebP images from the built-in image-generation tool.

**Spec:** `docs/superpowers/specs/2026-09-30-attendly-seo-content-design.md`

## Global Constraints

- Primary audience is English-speaking school and college students.
- Explain formulas and planning without making universal claims about institution-specific rules.
- Every article has a unique title, description, H1, canonical, social metadata, Article JSON-LD, breadcrumbs, image alt text, and related links.
- Use soft indigo, coral, lilac, and cream editorial illustrations with no embedded text, logos, or fake UI copy.
- Do not add a framework, CMS, database, or unsupported Attendly feature claims.
- Verify local links, image existence, metadata, sitemap coverage, and `git diff --check`.

## Review Focus

- Missing or duplicated SEO metadata → validation script checks one title, description, canonical, and H1 per page.
- Invalid local links or image references → link checker resolves every local href/src.
- Attendance-policy overclaiming → content scan checks policy disclaimer language on requirement articles.
- Broken schema JSON → JSON parser validates every JSON-LD block.
- Mobile overflow from long article headings/cards → responsive CSS inspection and manual spot-check.

### Task 1: Content generator and validation tests

**Files:**
- Create: `tool/build_blog_content.py`
- Create: `tool/validate_blog_content.py`
- Create: `blog/content.json`

**Interfaces:**
- Generator consumes `blog/content.json` and writes `blog.html`, `faq.html`, `blog/*.html`.
- Validator consumes generated HTML plus `sitemap.xml` and returns a non-zero exit code for missing metadata, invalid JSON-LD, missing images, or broken local links.

- [ ] Write validator checks first and run them against the current site to confirm the new routes fail because they do not exist.
- [ ] Add the 20 article records, FAQ records, keyword intents, related links, and source notes to `blog/content.json`.
- [ ] Implement the generator with deterministic templates for blog hub, FAQ hub, and article pages.
- [ ] Run the validator after generation and confirm it passes.

### Task 2: Blog/FAQ presentation and shared SEO styles

**Files:**
- Modify: `styles.css`
- Modify: `index.html`
- Modify: `support.html`
- Create: `blog.html`
- Create: `faq.html`

- [ ] Add navigation links to Blog and FAQ while preserving existing legal/support links.
- [ ] Add responsive blog-card, article, FAQ, breadcrumbs, callout, source, and related-link styles.
- [ ] Generate and inspect the hub and FAQ pages for desktop/mobile structure.

### Task 3: Article assets and metadata coverage

**Files:**
- Create: `assets/blog/*.webp` for each article.
- Modify: `sitemap.xml`
- Create/modify: `robots.txt`

- [ ] Generate one consistent editorial illustration per article with the image-generation skill.
- [ ] Move each final image into the project asset directory with the content slug filename.
- [ ] Add all public routes to sitemap and reference its location from robots.txt.
- [ ] Re-run validator and confirm every image reference exists.

### Task 4: Full verification

- [ ] Run `python3 tool/validate_blog_content.py` and read the complete result.
- [ ] Run `git diff --check`.
- [ ] Manually inspect the hub, FAQ, one calculation article, one practical article, and mobile layout.
- [ ] Record any deferred visual polish separately from correctness failures.

