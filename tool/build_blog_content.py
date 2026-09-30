#!/usr/bin/env python3
"""Build Attendly's static blog and FAQ pages from blog/content.json."""
from __future__ import annotations

import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
raw_data = (ROOT / "blog/content.json").read_text()
# Keep the source resilient to a missing closing array bracket in hand-authored content.
raw_data = raw_data.replace('"},{"heading', '"]},{"heading')
DATA = json.loads(raw_data)
(ROOT / "blog/content.json").write_text(json.dumps(DATA, ensure_ascii=False, indent=2) + "\n")
BASE = "https://attendly.app"

FAQS = [
    ("How do I calculate attendance percentage?", "Divide classes or hours attended by the total conducted classes or hours, then multiply by 100. Keep the unit consistent and check how your institution treats cancelled, excused, or makeup sessions.", "calculate-attendance-percentage"),
    ("How many classes can I miss and still keep 75% attendance?", "It depends on your current attended total, classes already held, and remaining schedule. Use A ÷ (H + m) ≥ 0.75 for an estimate, then confirm your institution's rule.", "attendance-calculator-classes-can-miss"),
    ("How many classes do I need to attend to reach 75%?", "Solve (A + n) ÷ (H + n) ≥ 0.75 and round n up to a whole class. The result is a planning estimate, not a replacement for official advice.", "reach-75-attendance"),
    ("Why is my subject percentage different from my overall percentage?", "An overall figure can combine subjects with different class counts. A subject-level percentage uses only that subject's conducted and attended totals, which is often the more useful number.", "track-attendance-by-subject"),
    ("What should I do if my attendance is below the requirement?", "Check the official policy, confirm your recorded totals, ask about corrections or approved leave, and calculate the remaining classes you need to attend.", "attendance-below-requirement"),
    ("How often should I update an attendance tracker?", "Update it soon after each class, then spend a few minutes reviewing subject trends once a week. Short, regular updates are easier to trust than end-of-term reconstruction.", "weekly-attendance-routine"),
    ("Does Attendly decide whether I am eligible for an exam?", "No. Attendly helps you organize records and understand calculations. Your institution's official policy and records decide eligibility.", "college-attendance-percentage-required"),
    ("Can I track lab and tutorial attendance separately?", "Yes. Separate records are useful when labs or tutorials have different hours, schedules, or minimums. Confirm the official counting method for your course.", "lab-tutorial-attendance-tracking"),
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def json_script(value: object) -> str:
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


def header(active: str, prefix: str = "") -> str:
    return f'''<header class="site-header"><a class="brand" href="{prefix}index.html" aria-label="Attendly home"><img src="{prefix}assets/attendly_logo.webp" alt=""><span>Attendly</span></a><nav class="nav" aria-label="Primary navigation"><a href="{prefix}index.html">Home</a><a href="{prefix}blog.html" class="{'active' if active == 'blog' else ''}">Blog</a><a href="{prefix}faq.html" class="{'active' if active == 'faq' else ''}">FAQ</a><a href="{prefix}support.html">Support</a><a class="nav-cta" href="{prefix}support.html#contact">Get help <span aria-hidden="true">↗</span></a></nav></header>'''


def footer(prefix: str = "") -> str:
    return f'<footer class="site-footer"><div class="footer-brand"><img src="{prefix}assets/attendly_logo.webp" alt=""><span>Attendly</span></div><div class="footer-links"><a href="{prefix}index.html">Home</a><a href="{prefix}blog.html">Blog</a><a href="{prefix}faq.html">FAQ</a><a href="{prefix}support.html">Support</a><a href="{prefix}privacy-policy.html">Privacy</a><a href="{prefix}terms.html">Terms</a></div><div class="footer-copy">© <span data-year></span> Attendly</div></footer><script src="{prefix}script.js"></script>'


def page(title: str, description: str, canonical: str, body: str, schema: object, active: str, prefix: str = "") -> str:
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{esc(description)}"><link rel="icon" type="image/png" href="{prefix}assets/attendly-logo-transparent.png"><link rel="canonical" href="{esc(canonical)}"><meta property="og:type" content="article"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{esc(canonical)}"><meta property="og:site_name" content="Attendly"><meta name="twitter:card" content="summary_large_image"><title>{esc(title)} — Attendly</title><link rel="stylesheet" href="{prefix}styles.css"><script type="application/ld+json">{json_script(schema)}</script></head><body>{header(active, prefix)}<main>{body}</main>{footer(prefix)}</body></html>'''


def article_card(article: dict, prefix: str = "") -> str:
    fallback = f"{prefix}assets/blog/complete-student-attendance-guide.png"
    return f'''<article class="blog-card"><a href="{prefix}blog/{article['slug']}.html"><img src="{prefix}assets/blog/{article['slug']}.png" alt="{esc(article['alt'])}" loading="lazy" onerror="this.onerror=null;this.src='{fallback}'"><div class="blog-card-body"><p class="card-kicker">{esc(article['category'])}</p><h3>{esc(article['title'])}</h3><p>{esc(article['description'])}</p><span class="card-link">Read article <span aria-hidden="true">↗</span></span></div></a></article>'''


def build_blog_hub() -> None:
    cards = "".join(article_card(article) for article in DATA)
    body = f'''<section class="page-hero blog-hero"><h1>Attendance questions,<br><em>worked out.</em></h1><p>Short, practical notes for the moments students usually reach for a calculator: a percentage that changed, a missed week, or a rule that needs checking.</p><div class="blog-hero-links"><a class="button button-primary" href="faq.html">Open the FAQ <span aria-hidden="true">↗</span></a><span>Written around real student questions.</span></div></section><section class="blog-index"><div class="blog-index-heading"><h2>Find the number<br><em>you came for.</em></h2></div><div class="blog-grid">{cards}</div></section>'''
    schema = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Attendly attendance guides", "url": f"{BASE}/blog.html", "description": "Practical attendance guides for students."}
    (ROOT / "blog.html").write_text(page("Attendance Guides & Student Resources", "Practical student attendance guides about percentages, shortage, tracking, planning, and habits.", f"{BASE}/blog.html", body, schema, "blog"))


def build_faq() -> None:
    faq_items = "".join(f'<details class="faq-item"><summary>{esc(question)}</summary><p>{esc(answer)} <a href="blog/{slug}.html">Read the guide ↗</a></p></details>' for question, answer, slug in FAQS)
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer}} for question, answer, _ in FAQS]}
    body = f'''<section class="page-hero faq-hero"><p class="eyebrow">Questions students ask</p><h1>Clear answers for<br><em>messy numbers.</em></h1><p>Start here for the attendance formulas, planning questions, and policy reminders that come up most often.</p></section><section class="faq-layout"><div class="faq-intro"><p class="eyebrow">Before you decide</p><h2>Use the math as a guide, then check your own policy.</h2><p>Attendly helps you organize your records and understand the calculation. Your institution’s official handbook, portal, or academic office decides the rule that applies to you.</p><a class="text-link" href="support.html">Need more help? Contact support <span aria-hidden="true">↗</span></a></div><div class="faq-list">{faq_items}</div></section>'''
    (ROOT / "faq.html").write_text(page("Attendance FAQ for Students", "Answers to common student questions about attendance percentages, classes you can miss, shortage, tracking, and recovery.", f"{BASE}/faq.html", body, schema, "faq"))


def build_articles() -> None:
    for index, article in enumerate(DATA):
        sections = "".join(f'<section><h2>{esc(section["heading"])}</h2>{"".join(f"<p>{esc(paragraph)}</p>" for paragraph in section["paragraphs"])}</section>' for section in article["sections"])
        related = [next(item for item in DATA if item["slug"] == slug) for slug in article["related"]]
        related_cards = "".join(article_card(item, prefix="../") for item in related)
        labels = {"Calculations": "The calculation", "Recovery": "The practical answer", "Policy & Planning": "Before you decide", "Habits": "A workable starting point", "Tracking": "The useful setup", "Planning": "A way to think about it", "Study Skills": "What the evidence says", "Guides": "The short version"}
        next_steps = {"Calculations": ("Keep the formula close.", "Save the numbers you use most, then check the result against your institution’s records."), "Recovery": ("Make the next class count.", "A recovery plan starts with the official total and one honest look at the classes still ahead."), "Policy & Planning": ("Check the rule that applies.", "Use the calculation to prepare a better question for your course office or handbook."), "Habits": ("Make the next check small.", "A record becomes useful when it is easy to update after an ordinary class day."), "Tracking": ("Keep one clear record.", "Record the subject, the date, and the result while the details are still easy to remember."), "Planning": ("Look at the remaining classes.", "A simple count of what is left usually makes the decision less abstract."), "Study Skills": ("Use the number carefully.", "Attendance is one signal among several. Pair it with your course context and the support available to you."), "Guides": ("Start with one subject.", "You do not need a perfect system on day one. Begin with the course you are checking today.")}
        answer_label = labels.get(article["category"], "The practical answer")
        next_heading, next_copy = next_steps.get(article["category"], ("Take the next useful step.", "Keep the record current and check the official policy when the decision matters."))
        article_schema = {"@context": "https://schema.org", "@type": "Article", "headline": article["title"], "description": article["description"], "image": f"{BASE}/assets/blog/{article['slug']}.png", "author": {"@type": "Organization", "name": "Attendly"}, "publisher": {"@type": "Organization", "name": "Attendly"}, "mainEntityOfPage": f"{BASE}/blog/{article['slug']}.html"}
        breadcrumb_schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/index.html"}, {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE}/blog.html"}, {"@type": "ListItem", "position": 3, "name": article["title"], "item": f"{BASE}/blog/{article['slug']}.html"}]}
        body = f'''<article class="article-page"><div class="breadcrumbs"><a href="../index.html">Home</a><span>/</span><a href="../blog.html">Blog</a><span>/</span><span>{esc(article['category'])}</span></div><div class="article-heading"><p class="eyebrow">{esc(article['category'])}</p><h1>{esc(article['title'])}</h1><p class="article-lede">{esc(article['description'])}</p><p class="article-meta">Updated September 2026 · Attendly guide</p></div><img class="article-hero-image" src="../assets/blog/{article['slug']}.png" alt="{esc(article['alt'])}"><div class="article-body"><div class="answer-callout"><strong>{esc(answer_label)}</strong><p>{esc(article['answer'])}</p></div>{sections}<div class="policy-note"><strong>Check your institution’s version.</strong><p>Thresholds, approved absences, and exam eligibility can vary. Use this guide to frame the question, then confirm the answer in your official course or institution policy.</p></div><div class="article-next"><p class="eyebrow">Worth doing next</p><h2>{esc(next_heading)}</h2><p>{esc(next_copy)}</p><a class="button button-primary" href="../support.html">Visit support <span aria-hidden="true">↗</span></a></div></div></article><section class="related-section"><div class="related-heading"><p class="eyebrow">More on this</p><h2>Related guides</h2></div><div class="blog-grid">{related_cards}</div></section>'''
        schema = [article_schema, breadcrumb_schema]
        (ROOT / "blog" / f"{article['slug']}.html").write_text(page(article["title"], article["description"], f"{BASE}/blog/{article['slug']}.html", body, schema, "article", "../"))


def build_sitemap() -> None:
    fixed = ["index.html", "blog.html", "faq.html", "support.html", "privacy-policy.html", "terms.html", "deletion-request.html"]
    urls = fixed + [f"blog/{article['slug']}.html" for article in DATA]
    lines = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>", '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    lines.extend(f"  <url><loc>{BASE}/{url}</loc></url>" for url in urls)
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    (ROOT / "blog").mkdir(exist_ok=True)
    (ROOT / "assets/blog").mkdir(exist_ok=True)
    build_blog_hub()
    build_faq()
    build_articles()
    build_sitemap()
    print(f"Generated {len(DATA)} articles, blog.html, and faq.html")
