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
	palette: Palette
	snake_head_glyph: str
	snake_body_glyph: str
	snake_glyph_fallback: str
	prey_glyph: str
	prey_glyph_fallback: str
	title_card_quote: str
	title_card_attribution: str
	game_over_quote: str
	game_over_attribution: str


THEME_1918 = Theme(
	key="1918",
	title="1918",
	subtitle="The Madman's Village",
	palette=Palette(
		bg="#1a1410",
		grid="#2e2520",
		snake="#a0392d",
		prey="#d4b88a",
		text="#e8d8b8",
		accent="#5e2e1f",
	),
	# snake_head_glyph="\U0001F464",			# bust in silhouette
	snake_head_glyph="\U0001F479",			# ogre
	# snake_body_glyph="\U0001F465",			# busts in silhouette
	snake_body_glyph="\U0001F60B",			# face savoring food
	snake_glyph_fallback="C",
	# prey_glyph="\U0001F4D3",				# notebook
	prey_glyph="\U0001F635\U0000200D\U0001F4AB",				# face with spiral eyes
	prey_glyph_fallback="!",
	title_card_quote="I refuse to discuss these things with you. Anyway, you shouldn't talk about it. Whoever talks about it is in the wrong!",
	title_card_attribution="[Lu Xun, Yang & Yang trans.]",
	game_over_quote="Perhaps there are still children who have not eaten men? Save the children...",
	game_over_attribution="[Lu Xun, Yang & Yang trans.]",
)


THEME_2018 = Theme(
	key="2018",
	title="2018",
	subtitle="The PRC's Panopticon",
	palette=Palette(
		bg="#1a2240",
		grid="#252d55",
		snake="#22c8e8",
		prey="#ff3a6e",
		text="#a8d8f0",
		accent="#5a1530",
	),
	# snake_head_glyph="\U0001F4F7",			# camera
	snake_head_glyph="\U0001F92B",			# shushing face
	# snake_body_glyph="\U0001F4F1",			# mobile phone
	# snake_body_glyph="\U0001F4F7",			# camera
	# snake_body_glyph="\U0001F6F0",			# satellite
	# snake_body_glyph="\U0001F4E1",			# satellite antenna
	snake_body_glyph="\U0001F910",			# zipper-mouth face
	# snake_body_glyph="\U0001F636",			# face without mouth
	# snake_body_glyph="\U0001FAE2",			# face with open eyes and hand over mouth
	# snake_body_glyph="\U0001F911",			# money-mouth face
	snake_glyph_fallback="C",
	# prey_glyph="\U0001F4E2",				# public-address loudspeaker
	# prey_glyph="\U0001F928",				# face with raised eyebrow
	prey_glyph="\U0001F914",				# thinking face
	prey_glyph_fallback="!",
	title_card_quote="I asked him \"Is it right to eat human beings?\"\n\"It may be so,\" he said, staring at me. \"It has always been like that...\"",
	title_card_attribution="[Lu Xun, Yang & Yang trans.]",
	game_over_quote="Wanting to eat men, at the same time afraid of being eaten themselves, they all look at each other with the deepest suspicion...\n\nHow comfortable life would be for them if they could rid themselves of such obsessions and go to work, walk, eat and sleep at ease. They have only this one step to take. Yet fathers and sons, husbands and wives, brothers, friends, teachers and students, sworn enemies and even strangers, have all joined in this conspiracy, discouraging and preventing each other from taking this step.",
	game_over_attribution="[Lu Xun, Yang & Yang trans.]",
)


THEMES: dict[str, Theme] = {
	THEME_1918.key: THEME_1918,
	THEME_2018.key: THEME_2018,
}
