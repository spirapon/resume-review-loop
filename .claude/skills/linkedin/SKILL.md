---
name: linkedin
description: Build and audit my LinkedIn profile from master.yaml, positioned for AI / ML / Data Science roles. Headline, About, Experience, Skills, Featured — scored, fact-checked, paste-ready. Use /linkedin [current-profile.txt] [--mode build|audit|full].
---

# LinkedIn Profile — Orchestrator

Drafts and scores one LinkedIn profile from `0_master_resume/master.yaml`. **This skill never edits `master.yaml`, never writes a resume, and never touches `2_applications/`.** All output goes to gitignored `outputs/linkedin_<yyyymmdd>/`.

LinkedIn is **one profile for all recruiters** — it cannot be tailored per job like a resume. So there is no JD input here. The positioning is fixed: **AI + Machine Learning + Data Science**, with BI and IT infrastructure as supporting depth.

A public profile that contradicts my resume is worse than a weak one. Every claim traces to a `master.yaml` fact ID and passes the same honesty bar as the resume pipeline.

## Arguments

`/linkedin [current-profile.txt] [--mode build|audit|full]`

- `[current-profile.txt]` — optional. My current profile pasted into a text file (headline + About + experience entries; rough is fine).
- Mode defaults: no file → `build`. With a file → `full`.
  - `build` — draft the profile from `master.yaml`. No audit of a current profile.
  - `audit` — score the current profile only, draft nothing. Requires a file; if missing, ask for it and stop.
  - `full` — audit the current profile, then draft the replacement, then score both so the delta is visible.

## Step 0 — Work folder

1. Create `outputs/linkedin_<yyyymmdd>/reviews/` (today's date).
2. If a current-profile file was given: verify it exists (if not, say so and stop), copy it to `<work>/current_profile.txt`, and write its absolute path into `<work>/source.txt`. Never modify the original.

## Step 1 — Select facts by angle

Read `0_master_resume/master.yaml` and select what belongs on an AI/ML/DS profile.

- **Lead facts** — any bullet or skill whose `angles` contains **`ai`, `mle`, or `ds`**.
- **Supporting facts** — `bi`-only items. Keep them, but compressed: earlier roles get a short summary instead of full bullets, while the BI tool names stay in the Skills list. BI recruiters search those strings, and a certification recorded in `master.yaml` is real evidence — cutting either costs reach for nothing.
- **Optional** — items with `angles: []`: a hobby build, a side project, anything that reads as personality rather than role fit. Offer them at the end under Projects, my call. Never force them in.
- **Cross-cutting** — publications, certifications, languages, and education apply regardless of angle.

Write `<work>/facts_selected.md`: a table of fact ID → one-line summary → lead/supporting/optional. Every claim drafted in Step 2 must cite an ID from this file.

## Step 2 — Draft `<work>/draft_profile.md`

Skip in `audit` mode. Each section below is written paste-ready — I copy it straight into LinkedIn, so no commentary inside the section blocks. Put notes in a separate `NOTES` block after each section.

### Headline (limit 220 chars)

Three variants, each a different strategy:

- **A — Role-forward**: titles first, then the proof. Safest for recruiter keyword search.
- **B — Outcome-forward**: what I make happen, role second.
- **C — Niche**: the specific combination nobody else claims. Read it off `master.yaml` — years in the field, the current specialism, any study in progress — never off ambition.

Rules for all three:
- Must literally contain the recruiter-search strings **`AI`**, **`Machine Learning`**, and **`Data Scien`** (Scientist/Science). Recruiters search exact phrases; "ML" alone does not match a search for "Machine Learning".
- ≤ 220 characters, verified by counting, not by eye.
- No buzzwords (list below).
- No "Open to work" / "Looking for opportunities" as the headline — that wastes the highest-weight keyword field. The Open-to-Work badge is a separate setting.

After the three, name which to use first and why, in 2–3 sentences.

### About (target 1,500–2,000 chars, max 2,600)

Structure:

1. **Hook** (first ~300 chars — this is all that shows before "see more" on mobile, so it must stand alone and must already contain AI / Machine Learning / Data Science). Start with the claim, not "Hi, I am <name>".
2. **Credibility** — what kind of systems, what kind of organisations, which countries. Specific, not "13+ years of experience" alone.
3. **Proof** — real numbers only, copied exactly from `master.yaml` metrics fields. Where a metric does not exist, describe the scope instead and never estimate one.
4. **What I'm looking for** — AI / ML / Data Science roles, including international relocation and onsite (per `contact.location`).
5. **Keyword line** — a plain comma-separated run of the searchable terms.
6. **CTA** — one low-friction action with my real email from `contact.email`.

Constraints: no buzzwords; no self-applied adjectives ("passionate", "expert", "seasoned") without proof; write like a person, not a LinkedIn template.

### Experience

For each role in `master.yaml`, newest first. LinkedIn is not the resume — it can be longer and more conversational, and that is the point:

```
<Title>
<Company> · <employment type if known>
<start> – <end> · <location>

<2–3 sentence role summary — the context a bullet list can't give.>

• <achievement bullet>            [fact: exp1.b1]
• ...
```

- Lead roles: 4–6 bullets. Supporting/BI-era roles: role summary plus at most 2 bullets.
- Achievement-first, active verbs, a real number wherever `master.yaml` has one.
- Every bullet ends with its `[fact: <id>]` tag in the draft. These tags are stripped from what I paste — they exist so Step 3 can verify.
- Add LinkedIn's per-role "Skills" line (up to 5) drawn from the bullets' `tech` fields.

### Skills

- Up to 50, ordered by relevance to AI/ML/DS.
- Name the **top 3 to pin** — these show on the profile and carry the most search weight.
- Merge fragmented entries into clusters where LinkedIn has a canonical skill name; keep the individual tools too when recruiters search them by name (e.g. keep `PySpark` and `Apache Spark` both).
- Every skill must trace to a `master.yaml` skill entry or a bullet's `tech` field. No aspirational skills.

### Featured

List only URLs that already exist in `master.yaml`, each with the title and one-line description to enter:

Typical sources, roughly in the order they carry weight:

- a thesis or dissertation (`edu<n>.url`)
- a peer-reviewed publication (`pub<n>.url`, plus `pub<n>.doi` when present)
- a public project, dashboard, or repository (`proj<n>.url`)

Flag any `master.yaml` `url: ""` TODO as a gap in Step 5 — do not invent a link.

### Education

Write the exact text to enter, degree by degree, straight from `master.yaml`.

A conferred degree is listed normally. **A degree still in progress is never written as though it
were finished** — no bare "M.Sc. <field>", no "completed coursework". State the study and its real
status instead, in this shape:

> <Institution> — Master's studies, <field> (<start>–<end>)
> <what is genuinely done: thesis, credits earned, what remains> — degree not yet conferred.

If the education entry in `master.yaml` carries a status note, that note wins over any wording here.

## Step 3 — Honesty check

Skip in `audit` mode (nothing was drafted).

1. Write the draft's plain text to `<work>/resume_text.txt` — the `fact-checker` agent's `standalone` mode reads that filename.
2. Run agent **fact-checker**, mode `standalone`, on the work folder → `reviews/factcheck.md`.
3. Read its final line:
   - `PASS` → continue.
   - `FAIL: ...` → fix the named `MISMATCH`/`DRIFT` in `draft_profile.md` and re-run. **Cap: 3 attempts** (same as the pipeline's retry cap). If still failing, report best-so-far and say plainly which claim could not be verified.

`UNVERIFIED` findings never block — they surface in Step 5 as questions for me to confirm.

## Step 4 — Audit & score

Score each section 1–10 with one sentence of diagnosis:

| Section | Score /10 | Diagnosis |
|---|---|---|
| Headline | | |
| About | | |
| Experience | | |
| Skills | | |
| Featured | | |
| Overall fit for AI/ML/DS roles | | |

Bands: **1–3** working against the goal · **4–6** present but forgettable · **7–8** clear and functional · **9–10** genuinely remarkable. Do not hand out 9s and 10s. Score what is actually there, not what it could be. In `full` mode, score the current profile *and* the draft in two tables so the delta is visible.

**Buzzword scan** — flag every hit and give a specific replacement, not a note:

results-driven · results-oriented · passionate about · passion for · dynamic professional · synergy · leveraging (as a noun) · comprehensive · robust · visionary · thought leader (self-applied) · seasoned professional · proven track record · go-getter · strategic thinker (unsubstantiated) · detail-oriented · team player · excited to announce · in today's landscape · game-changing · revolutionary · cutting-edge

**Mechanical limit check** — count characters, do not estimate. Run per section and report actual counts:
```bash
awk '{ print length, $0 }' <file>     # per-line, for headline variants
wc -m <file>                          # total chars, for the About block
```
Headline ≤ 220 · About ≤ 2,600 (target 1,500–2,000) · hook ≤ 300.

**Three checks worth keeping from generic LinkedIn advice** (the rest is noise for a job seeker):
- *Entity clarity* — do the first 50 words say who I am and in which niche, unambiguously?
- *Recency* — is the current role present with accurate dates?
- *Custom URL* — set a custom URL that matches your name (`linkedin.com/in/<yourname>`).

## Step 5 — Report

Short and simple, in this order:

1. **Scores** — the table(s) from Step 4. In `full` mode, current → draft delta.
2. **Top fixes** — numbered, highest leverage first, one line each.
3. **Buzzword flags** — each with its replacement. Say "none" if none.
4. **Character counts** — headline variants, About, hook, each against its limit.
5. **Honesty flags** — `factcheck.md` findings. `UNVERIFIED` items are phrased as *questions to confirm*, never accusations.
6. **Gaps** — LinkedIn-worthy facts missing from `master.yaml` (missing URLs, missing metrics, a `# TODO` I should fill). These are **suggestions to me only** — never added to `master.yaml`, never written into the profile. Same rule as `gap_report.md`.
7. **File paths** — the work folder and `draft_profile.md`.

Then offer exactly two next moves: refine a named section, or paste it into LinkedIn as-is. Do not offer to post content, design a banner, or update `master.yaml`.

## Honesty (never break)

`master.yaml` is the single source of truth. If a fact is not in it, it does not exist. Tailoring = reorder + rephrase + re-emphasize only. Never invent, never round, never change a number.

Carry every inline guardrail in `master.yaml` across explicitly. A trailing `#` comment on a
`metrics` field, or a status note on an education entry, is a rule and not a hint — these are
exactly the places where a generic LinkedIn optimizer would produce a public lie.

Before drafting, read the guardrail comments out of `master.yaml` and restate them as a table, so
the draft can be checked line by line against it:

| Fact | Rule |
|---|---|
| `edu1` | Degree in progress → never write it as conferred. Use the Education wording in Step 2. |
| `exp1.b2` | Test server, availability never measured → **no uptime %**, no availability claim. |
| `exp2.b1` | POC with no formal evaluation → no accuracy, mAP, or precision number. |
| `exp2.b2` | Anything an employer marks confidential (hardware counts, headcount, client names) → never publish. |
| `proj1.b1` | Two different models → never merge them into a single improvement number. |
| `sum3` | Years in tech is not years in the specialism → never inflate one into the other. |

Those rows are the *shape* to follow, not the content — the real rules come from your own
`master.yaml`.

If any drafted line needs a fact I don't have, leave it out and list it under Gaps.
