# Snake — Lu Xun Edition (1918 / 2018)

**Status**: done
**Date opened**: 2026-05-09
**Opened by**: Chris

## What & Why
A tkinter Snake game with a menu offering two thematic modes — **1918** (cannibal villagers from *Diary of a Madman* chasing the madman) and **2018** (a chain of surveillance devices tracking a dissident in the modern PRC). Same Snake mechanics in both. The reskins are the academic argument: in both eras, a dominant system grows by consuming the individual who tries to speak.

This is the project's first piece of code, so it also establishes the multi-file Python layout, test conventions, and academic-citations pattern.

## Acceptance Criteria
- [ ] `python -m game` opens a menu window with two themed buttons + a one-line thesis under each, plus an "About" button
- [ ] Clicking a mode button shows a title card with a Lu Xun quote / framing line, then starts gameplay on keypress
- [ ] WASD controls; wall and self collisions end the game; eating prey grows the chain by one and respawns prey at a non-occupied cell
- [ ] 1918 theme: chain glyphs are villagers (👥/👤), prey is the madman (🧑), themed palette
- [ ] 2018 theme: chain glyphs are surveillance devices (📱📷🛰️), prey is a dissident (🚩 or 👤 with sign), themed palette
- [ ] Game-over screen shows score, a theme-specific quote, and "Play Again" / "Back to Menu" buttons
- [ ] About screen scrollable, lists sources from `CITATIONS.md`
- [ ] Engine tests pass via `python -m unittest discover tests` without opening a tkinter window
- [ ] No new linter/type errors; conventions in `CLAUDE.md` updated to reflect the new layout

## Design Notes

### Goal (one sentence)
Build a tkinter Snake game whose two modes — 1918 cannibal villagers and 2018 surveillance state — render Lu Xun's *Diary of a Madman* argument as gameplay.

### What exists
- `Diary of a Madman.pdf` at project root (source text — translation TBD; see Open Questions)
- `CLAUDE.md` conventions: Python only, `pathlib.Path` for paths, scripts runnable from project root, separate code/academic dirs, branch/commit prefixes
- Empty `memory.md` (Working Memory file, ready to record decisions made during this build)
- No prior code, tests, or dependency manifest

### What changes — files to create
| Path | Purpose |
|---|---|
| `game/__init__.py` | Package marker |
| `game/__main__.py` | Entry point so `python -m game` runs the menu |
| `game/engine.py` | Pure-Python game state: grid, snake (deque of cells), prey position, direction, tick(), collision, growth. **No tkinter import.** |
| `game/ui.py` | Tk root, menu screen, title cards, game canvas, key bindings, game-over screen, mode routing |
| `game/themes.py` | `Theme` dataclass: name, palette, snake-glyph cycle, prey glyph, menu blurb, title-card quote, game-over quote, about-blurb. Two instances: `THEME_1918`, `THEME_2018` |
| `game/content.py` | About-screen long text, organized for review/citation |
| `tests/__init__.py` | Test package marker |
| `tests/test_engine.py` | Engine unit tests using stdlib `unittest` |
| `CITATIONS.md` (project root) | Lu Xun edition cited for in-game quotes; secondary sources for the 2018 framing |
| `README.md` (update) | Add a "Run" section: `python -m game`, plus `pytest` for tests |
| `CLAUDE.md` (update) | Add `game/` package convention, `tests/` location, pytest decision |
| `memory.md` (update) | Record: package layout, pytest, content-citation rule |

### Design decisions
1. **Engine / UI separation.** `engine.py` is pure data; `ui.py` is the tkinter shell. Lets us write fast deterministic tests without spawning a window. This becomes the project's first layer convention.
2. **Themes as data, not subclasses.** `themes.py` holds `Theme` instances. Adding a third year later = one new dataclass instance. No inheritance.
3. **Unicode emoji glyphs on tkinter Canvas** (option A from clarification). No image assets, no Pillow. Rendered via `Canvas.create_text` with a font that supports emoji ("Segoe UI Emoji" on Windows). Fallback to ASCII glyphs if the OS font fails.
4. **Direction-change buffering.** A keypress sets a *pending* direction, applied at the next tick. Prevents reversing-into-self if the user double-taps within one tick. Engine-level concern, tested.
5. **Constant 120 ms tick.** No speed-up. Theme over twitch.
6. **Wall collision ends game** (no wrap). Fits the thesis: systems meet limits.
7. **Game-over flow:** themed screen with score + a Lu Xun quote + Play Again / Back to Menu.
8. **Window is fixed-size**, 600×600 px, 30×30 grid (20 px cells). Avoids resize-handling complexity.
9. **No dependency manifest yet.** Project uses only stdlib (`tkinter`, `unittest`). Per user preference: builtin libs where possible; introduce `requirements.txt` only if an external dep becomes necessary.
10. **Citations live in `CITATIONS.md` at project root.** Every in-game quote tagged with a source key (e.g., `[Lyell-1990]`) so the academic-integrity link from CLAUDE.md is enforced.

### Edge cases
- **Reverse-into-self via fast key combo** — handled by direction buffering (see decision 4)
- **Prey spawns inside the snake** — re-roll position until clear; if grid is fully occupied, treat as "win" and show a special end card
- **Multiple keypresses within one tick** — only the most recent valid direction wins
- **Window closed mid-game** — Tk teardown handler cancels the after-loop cleanly so the process exits
- **Emoji glyph not rendered** — themes carry an ASCII-fallback glyph string and a font preference list; if `Segoe UI Emoji` is missing, fall back
- **Holding a key** — Tk fires repeated KeyPress events; engine ignores duplicates of the current direction
- **Player presses non-WASD keys** — ignored (no error)

### Tests needed (engine only — no UI tests)
1. `test_initial_state` — snake length, head position, direction, prey placed
2. `test_tick_moves_head` — single tick advances head by direction vector; tail follows
3. `test_eating_prey_grows_chain` — head onto prey → length += 1, prey respawns
4. `test_prey_never_spawns_on_snake` — repeated spawn calls always land on empty cell
5. `test_wall_collision_ends_game` — head into boundary → `state.game_over is True`
6. `test_self_collision_ends_game` — chain longer than 4, doubles back, ends game
7. `test_reverse_direction_blocked_in_same_tick` — moving right, queue left → still moves right that tick
8. `test_full_grid_triggers_win_state` — synthesize a near-full grid, eat last prey → `state.won is True`
9. `test_tick_after_game_over_is_noop` — state frozen once over

### Docs affected
- New: `README.md` run section, `CITATIONS.md`
- Updated: `CLAUDE.md` (layer conventions for `game/` and `tests/`, `unittest` as test framework, no manifest), `memory.md` (decisions log)

### Open questions — resolved
1. ~~Translation~~ → **Yang & Yang**, the version included as `Diary of a Madman.pdf` at project root.
2. ~~Secondary source for 2018~~ → **Human Rights Watch, *China's Algorithms of Repression* (May 2019)** as the anchor, with room in `CITATIONS.md` to add more as the academic content grows.
3. ~~Specific quotes~~ → **Deferred.** Title-card and game-over strings will use clearly-marked placeholders (e.g., `"[QUOTE: 1918 title card — TBD]"`). Final selection happens after the code is working.

## Resolution
**Closed**: 2026-05-09
**Branch**: `feat/snake-lu-xun`
**Files changed**:
- new: `.gitignore`, `CITATIONS.md`
- new: `game/__init__.py`, `game/__main__.py`, `game/engine.py`, `game/themes.py`, `game/content.py`, `game/ui.py`
- new: `tests/__init__.py`, `tests/test_engine.py`, `tests/test_themes.py`, `tests/test_ui_import.py`
- modified: `README.md`, `CLAUDE.md`, `memory.md`

**Tests added**: 19 (13 engine cases, 4 theme sanity checks, 2 UI import smoke)

**Carry-over** (out of scope, recorded for follow-up):
- Title-card and game-over quote placeholders still in `game/themes.py` (open question 3 was deferred until the code worked end-to-end).
- The pre-existing `pip upgrade` commit on `main` tracks the local `.venv/` directory; `.gitignore` only stops new venv files. A separate `git rm -r --cached .venv` cleanup is recommended.
