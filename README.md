# Snake — Lu Xun Edition

History 170E project, UC Irvine. A tkinter Snake game with two thematic modes — **1918** (cannibal villagers from Lu Xun's *Diary of a Madman*) and **2018** (modern PRC surveillance state) — playing the same allegory through different reskins. The mechanic is identical because the claim is structural: the system grows by absorbing the individual who tries to speak.

## Run

```
python -m game
```

WASD to move. Esc returns from any screen.

## Tests

```
python -m unittest discover tests
```

Engine logic is covered exhaustively (collisions, growth, prey spawn, win state, direction buffering). UI rendering is not testable without a display — the only UI test is an import smoke test.

## Project layout

- `game/engine.py` — pure-Python game state; no tkinter import
- `game/themes.py` — `Theme` dataclasses for 1918 and 2018 (palette, glyphs, quotes)
- `game/content.py` — long-form About-screen text
- `game/ui.py` — tkinter shell: menu, title card, game canvas, game-over, About
- `game/__main__.py` — entry point
- `tests/` — stdlib unittest, no external dependencies

## Citations

Sources are listed in [`CITATIONS.md`](CITATIONS.md). In-game quote slots currently show placeholder strings (`[QUOTE: … — TBD]`) pending final translation lookup; the citations file already names the canonical primary text and the anchor secondary source.
