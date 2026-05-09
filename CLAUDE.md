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

Academic Python project for Hist170E at UCSC, focused on Lu Xun (鲁迅) and how *Diary of a Madman* (1918) parallels the modern PRC surveillance state. The first artifact is `game/`, a tkinter Snake game with two reskins — 1918 cannibal villagers and 2018 surveillance hardware — played through identical mechanics to argue that the system grows by absorbing the individual who tries to speak. Engine and UI are split so the engine can be tested in isolation. Feature branches `type/short-description` merged into `main`.

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

### Game package (`game/`)
- `engine.py` is pure data + state — **never imports tkinter**. UI consumes it.
- `themes.py` adds new modes as `Theme` dataclass instances, not subclasses.
- `ui.py` owns the `tk.Tk` root and uses an `App`-mediated frame swap; key bindings are tracked centrally so each swap clears them (no stale handlers calling into destroyed frames).
- Entry point: `python -m game` runs `game/__main__.py`.
- Forbidden: importing `tkinter` from `engine.py` or anything the engine imports.

### Tests (`tests/`)
- Stdlib `unittest`. Run from project root: `python -m unittest discover tests`.
- Engine logic covered exhaustively; UI rendering is not testable without a display, so only an import smoke test exists for `game.ui`.
- Forbidden: introducing pytest or any external test dep without a recorded decision in `memory.md`.

### Academic content
- Quoted passages live in `game/themes.py` and `game/content.py` strings, tagged with `[QUOTE: … — TBD]` placeholders until the final source key is locked in.
- Every quote that ships must trace to an entry in `CITATIONS.md`.

### Data / Sources
_No data files yet._
- Raw source texts go in `data/raw/`; processed outputs in `data/processed/`.
- Forbidden: committing large binary files — use `.gitignore` or a manifest.

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
