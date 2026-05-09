# Bootstrap AI Agent Workflow

Analyze this codebase and generate a minimal, accurate agent workflow.
Every file you create must reflect patterns you actually found — no boilerplate.

---

## Phase 1 — Codebase Reconnaissance

Read these files before writing anything:

1. Root directory listing
2. `README.md` or equivalent entry-point doc
3. One model/schema definition file
4. One route/controller/handler file
5. One test file
6. Any existing `CLAUDE.md`, `Agent.md`, `.cursorrules`, or similar

From these, determine and record:

| Question | Answer |
|---|---|
| Project type | (API / library / CLI / full-stack / etc.) |
| Primary language + version | |
| Framework(s) | |
| Test framework + test location | |
| How models are defined | |
| How routes/handlers are registered | |
| Where business logic lives | |
| Naming convention (files, classes, functions) | |
| Existing agent instruction files | |
| Git branching pattern (if detectable) | |

Do not proceed to Phase 2 until you can fill in this table from actual files.

---

## Phase 2 — Create Workflow Files

### `CLAUDE.md` — Master Agent Contract

This is the single source of truth for project conventions.
Claude Code auto-loads this file every session. Keep it under 150 lines.

Required sections (in order):

**1. Thread Start Sequence**
```markdown
## Start Every Thread Here
1. Read this file in full
2. Read `memory.md`
3. Choose your mode — read the corresponding file in `prompts/`
   - Scoping new work → `prompts/planning.md`
   - Implementing approved work → `prompts/building.md`  
   - Fixing a bug → `prompts/bug_fixer.md`
4. Read the relevant request or issue file from `planning/`
```

**2. Project Map**
3–5 sentences. What this project is, how it's structured, where things live.
Optimized for an agent who has never seen it. No fluff.

**3. Non-Negotiable Rules**
The 5–8 rules that, if violated, will break things or create bad patterns.
Derive these from what you observed. Examples of the *type* to include:
- "Never import X directly — always go through Y"
- "All DB writes go through the service layer, never in routes"
- "Use the custom base class, never the framework default"
- "Branch names: `type/short-description` (e.g., `feat/user-auth`)"
- "Commits: `type: description` — never skip the type prefix"

Do not include rules you didn't verify exist in the codebase.

**4. Layer Conventions**
One subsection per layer present in this project. For each:
- How things are structured (1–2 sentences)
- The pattern to follow (show a real example from the codebase, not invented)
- What's forbidden at this layer

Layers to cover if present: Models · Routes/Views · Services/Handlers · Tests · Auth/Permissions · Config/Settings

**5. Working with AI — What Works Here**
- Which files are safe to generate wholesale vs. must be written incrementally
- Which areas are high-risk (read surrounding code carefully first)
- Which tests are slow or flaky (avoid running in tight loops)
- Context cost signals (e.g., "migrations/ has 200 files — don't ls it")

**6. Pre-Edit Checklist**
```markdown
Before modifying any file:
- [ ] Read the file in full, not just the target function
- [ ] Confirmed no other file imports the thing being changed
- [ ] Know what layer this belongs to
- [ ] Know what test covers it (or why none does)
```

**7. Done Criteria**
```markdown
A task is closed only when:
- [ ] All changed code follows conventions in this file
- [ ] Tests pass and cover the new behavior
- [ ] No new linter/type errors introduced
- [ ] `memory.md` updated if a decision was made
- [ ] Request/issue file moved to `planning/done/`
```

---

### `memory.md` — Living Context
```markdown
# [Project Name] — Working Memory

_Hygiene: max 5 bullets per section. Outcomes over narrative. Archive when resolved._

## Current Focus
-

## Key Decisions
_Non-obvious choices made — why, not just what._
-

## Watch List
_Fragile areas, known debt, things to tread carefully._
-

## In Progress
-

## Archive
```

Start this file empty except the structure. Do not invent entries.

---

### `prompts/planning.md` — Planning Mode
```markdown
# Planning Mode

## Role
You are a senior engineer scoping work before any code is written.
Your job is to produce a complete, unambiguous plan — not to implement it.
Read `CLAUDE.md` for project conventions before starting.

## Workflow
1. Restate the request in your own words — confirm understanding
2. Explore the codebase: find what already exists that's relevant
3. Propose a plan using the output format below
4. Gate: get explicit user approval before this thread ends

## Output Format
- **Goal**: one sentence
- **What exists**: relevant files/functions already in place
- **What changes**: exact list of files to create or modify
- **Design decisions**: non-obvious choices and why
- **Edge cases**: what could go wrong
- **Tests needed**: what scenarios to cover
- **Docs affected**: what needs updating
- **Open questions**: anything unresolved that would block building

## Forbidden in This Mode
- Writing implementation code
- Making assumptions instead of asking
- Closing the thread without user sign-off on the plan
```

---

### `prompts/building.md` — Building Mode
```markdown
# Building Mode

## Role
You are a senior engineer executing an approved plan one task at a time.
You write minimal, correct, tested code that matches existing patterns.
Read `CLAUDE.md` for project conventions. Read the request file for scope.

## Workflow
1. State what you're about to build (one sentence)
2. Show your implementation plan — get confirmation before writing code
3. Implement — one logical unit at a time
4. Write tests immediately after implementation, not at the end
5. Update relevant docs
6. Move the request file to `planning/done/`
7. Update `memory.md` if any decision was made
8. State what's next

## Output Format Per Task
- **Request**: what you're doing
- **Plan**: confirmed approach
- **Implementation**: the code
- **Tests**: covering the new behavior
- **Docs**: what changed
- **Done**: checklist from `CLAUDE.md`
- **Next**: next task or "complete"

## Forbidden in This Mode
- Expanding scope beyond the current request file
- Writing code before confirming the plan
- Skipping tests ("I'll add them later")
- Touching files not in the plan without flagging it first
```

---

### `prompts/bug_fixer.md` — Bug Fix Mode
```markdown
# Bug Fix Mode

## Role
You are an engineer diagnosing and fixing one bug at a time with rigor.
A fix without a regression test didn't happen.
Read `CLAUDE.md` for project conventions. Read the issue file before starting.

## Workflow
1. Restate the bug and your hypothesis about root cause
2. Write a regression test that currently fails — confirm it fails
3. Propose the fix — get confirmation before implementing
4. Implement the fix
5. Confirm the regression test now passes, all other tests still pass
6. Move the issue file to `planning/done/` with root cause filled in
7. Update `memory.md` if this reveals a systemic pattern

## Output Format Per Issue
- **Issue**: restated in your own words
- **Hypothesis**: what you think is wrong and why
- **Regression test**: the test, confirmed failing
- **Fix plan**: confirmed approach
- **Fix**: the code change
- **Validation**: test output showing green
- **Done**: root cause, files changed, test added
- **Next**: next issue or "complete"

## Forbidden in This Mode
- Writing the fix before writing the regression test
- Marking an issue resolved without a passing regression test
- Fixing multiple bugs in one task
- Refactoring while fixing (open a separate request instead)
```

---

### `planning/` Folder Structure

Create:
```
planning/
  requests/
    _template.md
  issues/
    _template.md
  done/
    .gitkeep
```

**`planning/requests/_template.md`**
```markdown
# [Feature Title]

**Status**: open | in-progress | done
**Date opened**: YYYY-MM-DD
**Opened by**:

## What & Why
[What needs to exist. Why it matters now.]

## Acceptance Criteria
- [ ]
- [ ]

## Design Notes
[Constraints, prior decisions, open questions — fill in during planning]

## Resolution
**Closed**: YYYY-MM-DD
**Branch**:
**Files changed**:
**Tests added**:
```

**`planning/issues/_template.md`**
```markdown
# [Bug Title]

**Status**: open | in-progress | done
**Date opened**: YYYY-MM-DD
**Severity**: low | medium | high | critical

## Reproduction Steps
1.
2.

## Expected vs. Actual
- Expected:
- Actual:

## Hypothesis
[What you think is wrong before digging in]

## Resolution
**Closed**: YYYY-MM-DD
**Root cause**:
**Fix summary**:
**Regression test added**: yes | no — [why not if no]
```

---

## Phase 3 — Delivery Report

After creating all files, output this report:

### What I Found
- Project type and stack (specific — include version numbers if visible)
- Test framework and where tests live
- The 3 most important non-obvious conventions I encoded

### Files Created
| File | Purpose |
|---|---|
| `CLAUDE.md` | Master project conventions, rules, checklists |
| `memory.md` | Living context log for active work |
| `prompts/planning.md` | Planning mode persona and workflow |
| `prompts/building.md` | Building mode persona and workflow |
| `prompts/bug_fixer.md` | Bug fix mode persona and workflow |
| `planning/requests/_template.md` | Template for new feature requests |
| `planning/issues/_template.md` | Template for bug reports |
| `planning/done/.gitkeep` | Holds resolved items |

### Gaps — Fill These In Manually
Anything you couldn't determine from the codebase. Be specific about
what's missing and where in which file it belongs


### Recommended First Action
One concrete next step (e.g., "Create your first request file describing
the next feature, then start a building thread with CLAUDE.md in context").

---

## Constraints

- Read files before writing. Phase 1 is not optional.
- Every rule in `CLAUDE.md` must trace to something you observed.
- `CLAUDE.md` must stay under 150 lines. Concision is a feature.
- Do not create migration files, install packages, or run commands.
- Do not modify existing source files.
- Do not invent conventions. Gaps go in the report, not the files.
