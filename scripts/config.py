#!/usr/bin/env python3
"""Shared settings for the pipeline scripts. Edit here, not in each script."""
import os
from pathlib import Path

import yaml

PROJECT = Path(__file__).resolve().parent.parent
MASTER = PROJECT / "0_master_resume" / "master.yaml"

# Headless Chrome renders the PDF.
# Override with:  export CHROME_PATH="/path/to/chrome"
CHROME = os.environ.get(
    "CHROME_PATH",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


def resume_prefix():
    """Your first name, read from master.yaml. Used to name output files."""
    default = "Candidate"
    if not MASTER.exists():
        return default
    contact = (yaml.safe_load(MASTER.read_text()) or {}).get("contact", {})
    name = str(contact.get("name", "")).strip()
    return name.split()[0] if name else default
