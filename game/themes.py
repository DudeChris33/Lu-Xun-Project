"""Theme definitions for the two game modes.

Each Theme is data only — no logic. The UI consumes themes to render
menu blurbs, gameplay glyphs, palettes, and the academic-text bookends.

Quote strings tagged "[QUOTE:" or "[ATTRIBUTION:" are placeholders to be
replaced once the syllabus translation is finalized in-game. See the
request file (planning/requests/snake_lu_xun.md, open question 3 —
deferred until after code is working).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Palette:
    bg: str
    grid: str
    snake: str
    prey: str
    text: str
    accent: str


@dataclass(frozen=True)
class Theme:
    key: str
    title: str
    subtitle: str
    menu_blurb: str
    palette: Palette
    snake_head_glyph: str
    snake_body_glyphs: Sequence[str]
    snake_glyph_fallback: str
    prey_glyph: str
    prey_glyph_fallback: str
    title_card_quote: str
    title_card_attribution: str
    game_over_quote: str
    game_over_attribution: str
    about_blurb: str


THEME_1918 = Theme(
    key="1918",
    title="1918",
    subtitle="The Madman's Village",
    menu_blurb="The villagers chase the only man who calls them what they are.",
    palette=Palette(
        bg="#1a1410",
        grid="#2e2520",
        snake="#a0392d",
        prey="#d4b88a",
        text="#e8d8b8",
        accent="#5e2e1f",
    ),
    snake_head_glyph="\U0001F464",       # bust in silhouette
    snake_body_glyphs=("\U0001F465",),   # busts in silhouette
    snake_glyph_fallback="V",            # villager
    prey_glyph="\U0001F4D3",             # notebook (the diary)
    prey_glyph_fallback="D",
    title_card_quote="[QUOTE: 1918 title card — TBD]",
    title_card_attribution="[ATTRIBUTION: Lu Xun, Yang & Yang trans.]",
    game_over_quote=(
        "[QUOTE: 1918 game-over — TBD; "
        "candidate: ‘Save the children…’]"
    ),
    game_over_attribution="[ATTRIBUTION: Lu Xun, Yang & Yang trans.]",
    about_blurb=(
        "1918 mode reskins the snake as a chain of villagers from Lu Xun's "
        "Diary of a Madman, who pursue the lone narrator who has realized "
        "the village is cannibalistic. Each diary you collect extends the "
        "chain — every truth-teller absorbed into the system that "
        "consumed them."
    ),
)


THEME_2018 = Theme(
    key="2018",
    title="2018",
    subtitle="Algorithms of Repression",
    menu_blurb="The watchers grow with every voice they catch.",
    palette=Palette(
        bg="#0a0e1a",
        grid="#1a1f30",
        snake="#22c8e8",
        prey="#ff3a6e",
        text="#a8d8f0",
        accent="#5a1530",
    ),
    snake_head_glyph="\U0001F4F7",       # camera
    snake_body_glyphs=(
        "\U0001F4F1",                    # mobile phone
        "\U0001F4F7",                    # camera
        "\U0001F6F0",                    # satellite
        "\U0001F4E1",                    # satellite antenna
    ),
    snake_glyph_fallback="C",            # camera
    prey_glyph="\U0001F4E2",             # public-address loudspeaker
    prey_glyph_fallback="!",
    title_card_quote="[QUOTE: 2018 title card — TBD]",
    title_card_attribution="[ATTRIBUTION: TBD]",
    game_over_quote="[QUOTE: 2018 game-over — TBD]",
    game_over_attribution="[ATTRIBUTION: TBD]",
    about_blurb=(
        "2018 mode reskins the snake as a chain of surveillance hardware "
        "operating across the modern PRC: phones, cameras, satellites, "
        "antennas. The prey is the voice the system seeks to silence. "
        "Each capture grows the network — the panopticon expands by "
        "absorbing everyone it tracks."
    ),
)


THEMES: dict[str, Theme] = {
    THEME_1918.key: THEME_1918,
    THEME_2018.key: THEME_2018,
}
