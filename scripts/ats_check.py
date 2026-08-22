#!/usr/bin/env python3
"""ATS keyword coverage scorer. Prints COVERAGE: nn (overall %) and misses.

Usage: ats_check.py <keywords.txt> <resume.html> [--report <ats_report.txt>]
keywords.txt lines: "P1: python", "P2: airflow", "P3: stakeholder communication".
Unprefixed lines count as P2. Always exits 0 (the orchestrator applies the gate).
"""
import re
import sys
from pathlib import Path


def normalize(text):
    text = text.lower()
    text = re.sub(r"[-_/]", " ", text)
    text = re.sub(r"[^a-z0-9+#. ]", " ", text)
    return re.sub(r"\s+", " ", text)


def load_keywords(path):
    buckets = {"P1": [], "P2": [], "P3": []}
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"(?i)^(p[123])\s*:\s*(.+)$", line)
        if m:
            buckets[m.group(1).upper()].append(m.group(2).strip())
        else:
            buckets["P2"].append(line)
    return buckets


def main():
    if len(sys.argv) < 3:
        print("usage: ats_check.py <keywords.txt> <resume.html> [--report <file>]")
        sys.exit(2)
    keywords = load_keywords(sys.argv[1])
    html = Path(sys.argv[2]).read_text()
    text = normalize(re.sub(r"<[^>]+>", " ", html))

    lines = []
    total_hit, total_all = 0, 0
    bucket_cov = {}
    for bucket in ("P1", "P2", "P3"):
        words = keywords[bucket]
        if not words:
            continue
        hits = [w for w in words if normalize(w).strip() in text]
        misses = [w for w in words if w not in hits]
        pct = round(100 * len(hits) / len(words))
        bucket_cov[bucket] = pct
        total_hit += len(hits)
        total_all += len(words)
        lines.append(f"{bucket}: {len(hits)}/{len(words)} ({pct}%)")
        for w in misses:
            lines.append(f"  MISSING {bucket}: {w}")

    overall = round(100 * total_hit / total_all) if total_all else 100
    lines.append(f"P1_COVERAGE: {bucket_cov.get('P1', 100)}")
    lines.append(f"COVERAGE: {overall}")

    report = "\n".join(lines)
    print(report)
    if "--report" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--report") + 1])
        out.write_text(report + "\n")


if __name__ == "__main__":
    main()
