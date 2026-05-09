"""Theme data sanity tests."""

import re
import unittest

from game.themes import THEME_1918, THEME_2018, THEMES


HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")


class TestThemes(unittest.TestCase):
    def test_themes_registered(self):
        self.assertIn("1918", THEMES)
        self.assertIn("2018", THEMES)
        self.assertIs(THEMES["1918"], THEME_1918)
        self.assertIs(THEMES["2018"], THEME_2018)

    def test_palette_colors_are_valid_hex(self):
        for theme in (THEME_1918, THEME_2018):
            for color_field in ("bg", "grid", "snake", "prey", "text", "accent"):
                color = getattr(theme.palette, color_field)
                self.assertRegex(
                    color, HEX_COLOR, f"{theme.key}.{color_field}={color!r}"
                )

    def test_glyphs_are_non_empty(self):
        for theme in (THEME_1918, THEME_2018):
            self.assertTrue(theme.snake_head_glyph)
            self.assertTrue(theme.snake_body_glyphs)
            self.assertTrue(theme.prey_glyph)
            self.assertTrue(theme.snake_glyph_fallback)
            self.assertTrue(theme.prey_glyph_fallback)

    def test_themes_have_distinct_visual_identity(self):
        # The point of the project is that the two reskins are visibly different.
        self.assertNotEqual(THEME_1918.palette, THEME_2018.palette)
        self.assertNotEqual(THEME_1918.snake_head_glyph, THEME_2018.snake_head_glyph)
        self.assertNotEqual(THEME_1918.prey_glyph, THEME_2018.prey_glyph)


if __name__ == "__main__":
    unittest.main()
