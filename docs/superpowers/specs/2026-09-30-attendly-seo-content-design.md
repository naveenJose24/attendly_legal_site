# Attendly SEO Content System

## Goal

Expand the static Attendly marketing/legal site into a search-friendly student attendance resource with one FAQ hub and 20 useful, internally linked blog articles. The content should attract students searching for attendance calculations, attendance shortage guidance, subject tracking, and practical ways to improve consistency, while avoiding universal claims about institution-specific attendance policies.

## Audience and positioning

- Primary audience: English-speaking school and college students.
- Product role: Attendly is the calm tracking layer that helps students record classes, understand trends, and stay above their institution's target.
- Editorial voice: clear, reassuring, practical, non-judgmental.
- Policy safety: explain formulas and planning; tell readers to verify their own institution's rules, exemptions, condonation, and exam eligibility requirements.

## Search-intent clusters

1. Calculation: attendance percentage, attendance calculator, current percentage.
2. Recovery: classes needed to reach 75%, how many classes can be missed, attendance shortage.
3. Tracking: student attendance tracker, subject-wise tracking, semester attendance planner.
4. Prevention: improve attendance, attendance routine, streaks, absence planning.
5. Context: labs/tutorials, below-requirement outcomes, attendance and academic performance.

The research pass found recurring SERP language around current percentage, classes still available to miss, classes required to recover, subject-level calculation, and institution-specific thresholds. The content will target these intents directly rather than claiming verified monthly search volume.

## Site architecture

Add these static routes/files:

- `blog.html`: blog hub with category filters represented as anchor links, article cards, and links to FAQ.
- `faq.html`: grouped FAQ page with semantic `details`/`summary`, FAQ JSON-LD, and links into relevant articles.
- `blog/<slug>.html`: 20 standalone articles, each with unique title, description, canonical URL, Article JSON-LD, breadcrumbs, one generated hero image, and related-article links.
- `assets/blog/<slug>.webp`: generated article illustration assets.
- `sitemap.xml` and `robots.txt`: include the new public routes.

Use the existing static HTML/CSS/JS conventions. Reuse shared header/footer and add a small set of blog/document styles to `styles.css`; do not add a framework or CMS.

## Content set

1. How to Calculate Your Attendance Percentage
2. How Many Classes Can I Miss and Still Stay Above 75%?
3. Attendance Shortage: What It Means and What to Do Next
4. What Attendance Percentage Do You Need for College?
5. How to Improve Your Attendance Without Burning Out
6. The Easiest Way to Track Attendance by Subject
7. Attendance Calculator: Current Percentage, Classes Needed, and Classes You Can Miss
8. How Many Classes Do I Need to Attend to Reach 75%?
9. Present vs. Absent: How Attendance Percentages Actually Work
10. How to Track Attendance Across a Full Semester
11. What Happens When Your Attendance Falls Below the Requirement?
12. How to Build a Simple Weekly Attendance Routine
13. Attendance Tracking for Lab Classes and Tutorials
14. How to Recover From a Bad Attendance Week
15. Attendance Goals: Choosing a Safe Target Above the Minimum
16. How to Plan Absences Without Losing Attendance Eligibility
17. Common Attendance-Tracking Mistakes Students Make
18. How Attendance Streaks Help You Stay Consistent
19. Attendance vs. Academic Performance: What Students Should Know
20. The Complete Student Guide to Attendance Tracking

Each article should contain:

- one primary query and 2–4 related phrases used naturally;
- a direct answer near the top;
- formula or example where relevant;
- scannable H2/H3 sections;
- a “check your institution’s policy” note when discussing requirements;
- one Attendly-related next step without pretending the app provides unsupported functionality;
- two or more contextual internal links;
- a descriptive generated image with accurate alt text.

## Visual system

Generate one image per article using a consistent editorial illustration direction: soft indigo, coral, lilac, cream, simple student-life objects, no embedded text, no logos, no fake UI copy. Use filenames derived from the article slug. Alt text must describe the actual visual and its relationship to the article; it must not be a keyword list.

## SEO requirements

- Unique `<title>` and meta description for every page.
- One clear H1 per page.
- Canonical URL metadata.
- Open Graph and Twitter card metadata.
- Article JSON-LD on blog pages; FAQPage JSON-LD on the FAQ hub; BreadcrumbList JSON-LD on both.
- Descriptive link text and internal links from hub → article → related article → FAQ/support.
- No keyword stuffing, fabricated statistics, or unsupported promises.
- Use absolute canonical/OG URLs only after confirming the site’s production domain; otherwise leave a clearly marked site-base constant in the static template.

## Verification

- Parse all new HTML files and confirm one H1, title, description, canonical, image alt text, and valid local links.
- Confirm every blog slug appears in the hub and sitemap.
- Confirm every referenced image exists.
- Run `git diff --check`.
- Manually inspect the blog hub, one calculation article, one practical-advice article, FAQ page, and a mobile layout.

## Sources consulted

- ClassTrack attendance calculator: https://classtracks.auspia.space/attendance-calculator
- My Class Attendance calculator: https://myclassattendance.com/
- Class attendance and academic performance study: https://arxiv.org/abs/1702.01262

