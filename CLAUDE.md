# Lu Xun Project — Agent Contract

## Start Every Thread Here
1. Read this file in full
2. Read `memory.md`
3. Choose your mode — read the corresponding file in `prompts/`
   - Scoping new work → `prompts/planning.md`
   - Implementing approved work → `prompts/building.md`
   - Fixing a bug → `prompts/bug_fixer.md`
4. Read the relevant request or issue file from `planning/`

---

## Project Map

Academic Python project for Hist170E at UCSC, focused on Lu Xun (鲁迅), the seminal early 20th-century Chinese writer. The project is in its earliest phase — no source files exist yet. The gitignore targets Python, so all scripts and analysis will be in Python. Work is done on the `main` branch.

---

## Non-Negotiable Rules

> These will expand as the project takes shape. Only rules observed in actual code belong here.

- Python is the language — do not introduce other languages without explicit decision
- Keep academic output (essays, analysis) and code (scripts, data processing) in separate directories
- Commit message format: `type: description` (e.g., `feat: add text analysis script`)
- Branch names: `type/short-description` (e.g., `feat/sentiment-analysis`)
- Do not hardcode file paths — use `pathlib.Path` relative to the project root

---

## Layer Conventions

### Scripts / Analysis
_No scripts exist yet. When created, follow this pattern:_
- One script = one clearly named task (e.g., `analyze_word_frequency.py`)
- All scripts should be runnable from the project root
- Forbidden: mixing data loading, processing, and output in a single function

### Data / Sources
_No data files exist yet._
- Raw source texts go in `data/raw/`; processed outputs in `data/processed/`
- Forbidden: committing large binary files — use `.gitignore` or a manifest

### Tests
_No test framework established yet — fill in when first tests are written._

---

## Working with AI — What Works Here

- This is a pre-code project; all files are safe to generate wholesale
- High-risk area: academic integrity — generated analysis must be reviewed and cited properly
- No slow or flaky tests yet
- The root directory is flat and small — safe to `ls`

---

## Pre-Edit Checklist
Before modifying any file:
- [ ] Read the file in full, not just the target function
- [ ] Confirmed no other file imports the thing being changed
- [ ] Know what layer this belongs to
- [ ] Know what test covers it (or why none does)

---

## Done Criteria
A task is closed only when:
- [ ] All changed code follows conventions in this file
- [ ] Tests pass and cover the new behavior
- [ ] No new linter/type errors introduced
- [ ] `memory.md` updated if a decision was made
- [ ] Request/issue file moved to `planning/done/`
