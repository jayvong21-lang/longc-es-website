#!/usr/bin/env python3
"""Fail when legacy or incomplete LongC contact details reach source or live pages."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


PRIMARY_PHONE = "18016526868"
SECONDARY_PHONE = "17750587110"
LEGACY_PHONES = {"185" + "0695" + "1837"}
PHONE_PATTERN = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
TEXT_SUFFIXES = {".html", ".js", ".json", ".md", ".py"}
EXCLUDED_DIRS = {".git", "__pycache__"}
DUAL_PHONE_FILES = {
    "news-detail.html",
    "geo_publisher/site_generator/templates/article.html",
    "geo_publisher/site_generator/templates/articles_list.html",
    "scripts/build_articles.py",
}


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        yield path


def audit_source(root: Path) -> list[str]:
    errors: list[str] = []
    for path in iter_text_files(root):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        relative = path.relative_to(root).as_posix()
        for phone in LEGACY_PHONES:
            if phone in text:
                errors.append(f"legacy phone {phone}: {relative}")

    for relative in sorted(DUAL_PHONE_FILES):
        path = root / relative
        if not path.exists():
            errors.append(f"required contact source missing: {relative}")
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        if PRIMARY_PHONE not in text or SECONDARY_PHONE not in text:
            errors.append(f"dual phone policy incomplete: {relative}")
    return errors


def fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": "LongC-contact-audit/1.0"})
    with urlopen(request, timeout=15) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status}")
        return response.read().decode("utf-8", errors="replace")


def audit_live(root: Path, base_url: str) -> list[str]:
    errors: list[str] = []
    allowed = {PRIMARY_PHONE, SECONDARY_PHONE}
    pages = sorted(
        path.relative_to(root).as_posix()
        for path in root.glob("*.html")
    ) + sorted(
        path.relative_to(root).as_posix()
        for path in (root / "articles").glob("*.html")
    )

    for relative in pages:
        url = f"{base_url.rstrip('/')}/{quote(relative)}?contactAudit=1"
        try:
            text = fetch(url)
        except (HTTPError, URLError, RuntimeError) as exc:
            errors.append(f"live fetch failed: {relative}: {exc}")
            continue
        for phone in sorted(set(PHONE_PATTERN.findall(text)) - allowed):
            errors.append(f"unexpected live phone {phone}: {relative}")
        for phone in LEGACY_PHONES:
            if phone in text:
                errors.append(f"legacy live phone {phone}: {relative}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--live", metavar="BASE_URL")
    args = parser.parse_args()

    root = args.root.resolve()
    errors = audit_source(root)
    if args.live:
        errors.extend(audit_live(root, args.live))

    if errors:
        print("CONTACT AUDIT FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    scope = "source and live pages" if args.live else "source"
    print(f"CONTACT AUDIT PASSED: {scope}; legacy phones=0; dual-phone policy=complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
