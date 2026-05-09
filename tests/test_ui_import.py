"""UI smoke test — verifies game.ui imports and exposes the expected classes.

Cannot test actual rendering without a display, so this is the only UI
test we have. Engine logic is covered separately by test_engine.py.
"""

import unittest


class TestUiImport(unittest.TestCase):
    def test_module_imports_and_exposes_classes(self):
        import game.ui

        for name in ("App", "MenuFrame", "TitleCardFrame", "GameFrame", "AboutFrame"):
            self.assertTrue(
                hasattr(game.ui, name), f"game.ui missing {name}"
            )


if __name__ == "__main__":
    unittest.main()
