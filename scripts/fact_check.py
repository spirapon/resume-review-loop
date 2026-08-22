#!/usr/bin/env python3
"""Mechanical honesty gate: every claim in resume.yaml must trace to master.yaml.

Usage: fact_check.py <master.yaml> <resume.yaml>
Exit 1 on any FAIL, 0 on PASS/WARN.
"""
import re
import sys

import yaml

DIGIT_RUN = re.compile(r"\d+")


def build_master_index(master):
    """Map every fact ID (top-level and bullet) to its concatenated text."""
    index = {}

    def add(fid, node):
        parts = []

        def collect(x):
            if isinstance(x, str):
                parts.append(x)
            elif isinstance(x, dict):
                for v in x.values():
                    collect(v)
            elif isinstance(x, list):
                for v in x:
                    collect(v)
        collect(node)
        index[fid] = " | ".join(parts)

    def walk(node):
        if isinstance(node, dict):
            fid = node.get("id")
            if fid:
                add(fid, node)
                # bullets like exp1.b2
                for key in ("bullets", "details", "facts"):
                    for b in node.get(key) or []:
                        if isinstance(b, dict) and b.get("id"):
                            add(b["id"], b)
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(master)
    return index


def master_skill_ids_without_evidence(master):
    bad = set()
    for sk in master.get("skills") or []:
        if isinstance(sk, dict) and sk.get("id"):
            ev = sk.get("evidence")
            if ev in (None, "", []):
                bad.add(sk["id"])
    return bad


def sources_of(node):
    src = node.get("source") or node.get("sources")
    if src is None:
        return None
    if isinstance(src, str):
        return [s.strip() for s in re.split(r"[,;]", src) if s.strip()]
    return [str(s) for s in src]


def check(master, resume):
    """Return (fails, warns) lists of messages."""
    index = build_master_index(master)
    no_evidence = master_skill_ids_without_evidence(master)
    revision_notes = str((resume.get("meta") or {}).get("revision_notes", ""))
    fails, warns = [], []

    def report(msg, node_ids):
        # a violation is only a WARN if its node ID is user-authorized in revision_notes
        if any(i and i in revision_notes for i in node_ids):
            warns.append(msg)
        else:
            fails.append(msg)

    def walk(node, path):
        if isinstance(node, dict):
            text = node.get("text")
            if isinstance(text, str):
                srcs = sources_of(node)
                if srcs is None:
                    report(f"{path}: text has no source/sources", [None])
                else:
                    cited_text = ""
                    for s in srcs:
                        if s not in index:
                            report(f"{path}: cited ID '{s}' not in master", [s])
                        else:
                            cited_text += " " + index[s]
                        if s in no_evidence:
                            report(f"{path}: cited skill '{s}' has no evidence in master", [s])
                    for run in DIGIT_RUN.findall(text):
                        if run not in cited_text:
                            report(f"{path}: number '{run}' not found in cited facts {srcs}", srcs)
            for k, v in node.items():
                walk(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")

    for section, value in resume.items():
        if section in ("meta", "contact"):
            continue
        walk(value, section)

    # contact must match master verbatim
    m_contact = master.get("contact") or {}
    r_contact = resume.get("contact") or {}
    for field, mval in m_contact.items():
        if field in ("id", "source", "sources"):
            continue
        rval = r_contact.get(field)
        if rval is not None and str(rval) != str(mval):
            fails.append(f"contact.{field}: '{rval}' differs from master '{mval}'")

    return fails, warns


def main():
    if len(sys.argv) != 3:
        print("usage: fact_check.py <master.yaml> <resume.yaml>")
        sys.exit(2)
    master = yaml.safe_load(open(sys.argv[1]))
    resume = yaml.safe_load(open(sys.argv[2]))
    fails, warns = check(master, resume)
    for w in warns:
        print(f"WARN: {w}")
    for f in fails:
        print(f"FAIL: {f}")
    if fails:
        print(f"RESULT: FAIL ({len(fails)} failures, {len(warns)} warnings)")
        sys.exit(1)
    print(f"RESULT: PASS ({len(warns)} warnings)")


if __name__ == "__main__":
    main()
