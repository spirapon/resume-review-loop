#!/usr/bin/env python3
"""Render an application's resume.yaml to HTML + PDF and print PAGES: n.

Usage: render.py <app_folder>
"""
import re
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

from config import CHROME, PROJECT, resume_prefix

TEMPLATES = PROJECT / "templates"


def sanitize(name):
    """Make a string safe for a filename: spaces -> _, drop slashes."""
    name = name.replace("/", "-").replace(" ", "_")
    return re.sub(r"[^A-Za-z0-9._-]", "", name)


def output_basename(folder):
    """Build <FirstName>_resume_<company>_<position> from analysis.yaml."""
    analysis = yaml.safe_load((folder / "analysis.yaml").read_text())
    company = sanitize(str(analysis.get("company", "company")))
    position = sanitize(str(analysis.get("position", "position")))
    return f"{resume_prefix()}_resume_{company}_{position}"


def count_pdf_pages(pdf_path):
    data = pdf_path.read_bytes()
    # count page objects; works for Chrome-generated PDFs
    n = len(re.findall(rb"/Type\s*/Page[^s]", data))
    if n == 0:
        m = re.search(rb"/Count\s+(\d+)", data)
        n = int(m.group(1)) if m else 0
    return n


def main():
    if len(sys.argv) != 2:
        print("usage: render.py <app_folder>")
        sys.exit(2)
    folder = Path(sys.argv[1]).resolve()
    resume_file = folder / "resume.yaml"
    if not resume_file.exists():
        print(f"ERROR: {resume_file} not found")
        sys.exit(1)

    resume = yaml.safe_load(resume_file.read_text())
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)))
    html = env.get_template("resume.html.j2").render(resume=resume)

    base = output_basename(folder)
    html_path = folder / f"{base}.html"
    pdf_path = folder / f"{base}.pdf"
    html_path.write_text(html)
    print(f"HTML: {html_path}")

    if not Path(CHROME).exists():
        print("ERROR: Google Chrome not found; PDF not generated")
        sys.exit(1)
    result = subprocess.run(
        [CHROME, "--headless", "--disable-gpu",
         f"--print-to-pdf={pdf_path}", "--no-pdf-header-footer",
         f"file://{html_path}"],
        capture_output=True, text=True, timeout=60)
    if not pdf_path.exists():
        print(f"ERROR: PDF generation failed\n{result.stderr}")
        sys.exit(1)
    print(f"PDF: {pdf_path}")
    print(f"PAGES: {count_pdf_pages(pdf_path)}")


if __name__ == "__main__":
    main()
