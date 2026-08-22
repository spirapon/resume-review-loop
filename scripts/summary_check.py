#!/usr/bin/env python3
"""Fail if the resume summary opens with a job-title label.

The summary must lead with real work, not the JD's role title. A bare role
label ("Analytics and machine learning engineer:") is banned; the same words
inside a sentence ("...engineer who takes data work end to end") are fine.

Usage: summary_check.py <app_folder>
Exit 0 = PASS, exit 1 = FAIL.
"""
import re
import sys
from pathlib import Path

import yaml

ROLE_NOUNS = {
    "engineer", "scientist", "analyst", "developer", "architect",
    "consultant", "specialist", "manager", "researcher", "technician",
    "programmer", "administrator", "lead",
}

# If the clause contains any of these it is a sentence, not a label.
SENTENCE_MARKERS = {
    "who", "that", "which", "takes", "take", "builds", "build", "works",
    "work", "serves", "serve", "turns", "turn", "delivers", "deliver",
    "brings", "bring", "has", "have", "is", "was", "does", "do", "leads",
    "led", "built", "worked", "served",
}


def first_clause(text):
    """The opening phrase, up to the first clause-ending punctuation."""
    return re.split(r"[—–:;,.]", text.strip(), maxsplit=1)[0]


def words(clause):
    return [w.lower() for w in re.findall(r"[A-Za-z']+", clause)]


def check(text):
    """Return a failure reason, or None if the summary opening is fine."""
    clause = first_clause(text)
    ws = words(clause)
    if not ws:
        return None

    # An ALL-CAPS opening is a label no matter how it is worded.
    caps = re.findall(r"\b[A-Z][A-Z&]+\b", clause)
    if len(caps) >= 2:
        return f"summary opens with an ALL-CAPS role label: {clause.strip()!r}"

    if not any(w in ROLE_NOUNS for w in ws):
        return None
    if any(w in SENTENCE_MARKERS for w in ws):
        return None
    return f"summary opens with a bare job-title label: {clause.strip()!r}"


def main():
    folder = Path(sys.argv[1])
    resume = yaml.safe_load((folder / "resume.yaml").read_text())
    text = (resume.get("summary") or {}).get("text", "")

    reason = check(text)
    if reason:
        print(f"FAIL: {reason}")
        print("Rewrite the opening to lead with the work itself. Never echo the JD's job title.")
        sys.exit(1)
    print("PASS: summary does not open with a job-title label.")


if __name__ == "__main__":
    main()
