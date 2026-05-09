# Lu Xun Project — Working Memory

_Hygiene: max 5 bullets per section. Outcomes over narrative. Archive when resolved._

## Current Focus
- Snake (Lu Xun edition) shipped on `feat/snake-lu-xun` (closed 2026-05-09). Next: pick the actual title-card and game-over quotes to replace placeholders in `game/themes.py`.

## Key Decisions
_Non-obvious choices made — why, not just what._
- **Translation**: Yang & Yang of *Diary of a Madman* (the PDF at project root) is the canonical text for in-game quotes and citations
- **2018 framing anchor source**: Human Rights Watch, *China's Algorithms of Repression* (May 2019); `CITATIONS.md` may grow to include more
- **Engine/UI split**: pure-Python `game/engine.py` (no tkinter import) so tests run without a window; `game/ui.py` is the tk shell. First multi-file pattern in the project
- **Themes as data**: `Theme` dataclass instances in `game/themes.py`, not subclasses — adding a third year = one new instance
- **Test framework**: `unittest` (stdlib); tests live under `tests/`, run via `python -m unittest discover tests`. No `pyproject.toml` or `requirements.txt` — user prefers builtin libs; manifest only if/when external deps become necessary

## Watch List
_Fragile areas, known debt, things to tread carefully._
- Emoji rendering on Windows tkinter is font-dependent — every theme must carry an ASCII fallback glyph

## In Progress
-

## Archive
- 2026-05-09 — Snake (Lu Xun edition) shipped: `game/` package (engine/themes/content/ui), `tests/` with 19 unittest cases, `CITATIONS.md`. Quotes still placeholders pending translation lookup. See `planning/done/snake_lu_xun.md`.
