#!/usr/bin/env python3
"""Validate Attendly's generated SEO pages and local references."""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str]]] = []
        self.text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append((tag, dict((key, value or "") for key, value in attrs)))

    def handle_data(self, data: str) -> None:
        self.text_parts.append(data)


def local_target(page: Path, value: str) -> Path | None:
    parsed = urlparse(value)
    if parsed.scheme or value.startswith("#"):
        return None
    return (page.parent / parsed.path).resolve()


def main() -> int:
    failures: list[str] = []
    pages = [ROOT / "blog.html", ROOT / "faq.html", *sorted((ROOT / "blog").glob("*.html"))]
    if not pages:
        print("FAIL: no generated content pages found")
        return 1

    for page in pages:
        parser = PageParser()
        parser.feed(page.read_text())
        tags = parser.tags
        title_count = sum(1 for tag, _ in tags if tag == "title")
        h1_count = sum(1 for tag, _ in tags if tag == "h1")
        meta_names = {attrs.get("name") for tag, attrs in tags if tag == "meta"}
        canonical_count = sum(1 for tag, attrs in tags if tag == "link" and attrs.get("rel") == "canonical")
        if title_count != 1 or h1_count != 1 or "description" not in meta_names or canonical_count != 1:
            failures.append(f"{page.relative_to(ROOT)}: expected one title, H1, description, and canonical")

        for tag, attrs in tags:
            if tag == "img":
                if not attrs.get("alt", "").strip() and "attendly_logo" not in attrs.get("src", ""):
                    failures.append(f"{page.relative_to(ROOT)}: image missing alt text")
                target = local_target(page, attrs.get("src", ""))
                if target and not target.exists():
                    failures.append(f"{page.relative_to(ROOT)}: missing image {attrs.get('src')}")
            for key in ("href", "src"):
                target = local_target(page, attrs.get(key, ""))
                if target and target.suffix and not target.exists():
                    failures.append(f"{page.relative_to(ROOT)}: broken local {key} {attrs.get(key)}")

        for script_tag, attrs in tags:
            if script_tag != "script" or attrs.get("type") != "application/ld+json":
                continue
            script_index = tags.index((script_tag, attrs))
            # JSON-LD is read from source because HTMLParser stores only tags.
            block = re.search(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', page.read_text(), re.S)
            if block:
                try:
                    json.loads(block.group(1))
                except json.JSONDecodeError as error:
                    failures.append(f"{page.relative_to(ROOT)}: invalid JSON-LD ({error})")
                break

    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        failures.append("sitemap.xml is missing")
    else:
        sitemap_text = sitemap.read_text()
        for page in pages:
            if page.name != "blog.html" and page.parent.name == "blog":
                if page.stem not in sitemap_text:
                    failures.append(f"sitemap.xml missing {page.stem}")

    if failures:
        print("\n".join(f"FAIL: {failure}" for failure in failures))
        return 1
    print(f"PASS: validated {len(pages)} content pages, local assets, metadata, and sitemap")
    return 0


if __name__ == "__main__":
    sys.exit(main())
