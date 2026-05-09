"""Tkinter UI shell.

Frame-based screens swapped in a single container by App. Key bindings
live on the root window and are tracked centrally so they're cleared on
each frame swap — avoids stale handlers calling into destroyed frames.

GameFrame is a stub here; Unit 5 wires it to the engine.
"""

from __future__ import annotations

import tkinter as tk
from typing import Optional

from game.content import ABOUT_TEXT, PROJECT_SUBTITLE, PROJECT_TITLE
from game.engine import DEFAULT_HEIGHT, DEFAULT_WIDTH, Direction, GameState
from game.themes import THEME_1918, THEME_2018, Theme


MENU_BG = "#0c0c0c"
MENU_FG = "#e8e8e8"
MENU_FG_DIM = "#999999"

WINDOW_SIZE = 600
WINDOW_TITLE = "Snake — Lu Xun Edition"

CELL_SIZE = 18
GRID_W = DEFAULT_WIDTH
GRID_H = DEFAULT_HEIGHT
CANVAS_W = CELL_SIZE * GRID_W
CANVAS_H = CELL_SIZE * GRID_H
TICK_MS = 120
EMOJI_FONT_NAME = "Segoe UI Emoji"

_KEY_TO_DIRECTION = {
    "w": Direction.UP,
    "a": Direction.LEFT,
    "s": Direction.DOWN,
    "d": Direction.RIGHT,
}


class App:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")
        self.root.resizable(False, False)
        self.root.configure(bg=MENU_BG)

        self.container = tk.Frame(
            self.root, bg=MENU_BG, width=WINDOW_SIZE, height=WINDOW_SIZE
        )
        self.container.pack(fill="both", expand=True)
        self.container.pack_propagate(False)

        self.current_frame: tk.Frame | None = None
        self._key_bindings: list[tuple[str, str]] = []
        self.show_menu()

    def bind_key(self, sequence: str, callback) -> None:
        funcid = self.root.bind(sequence, callback)
        self._key_bindings.append((sequence, funcid))

    def _unbind_all_keys(self) -> None:
        for sequence, funcid in self._key_bindings:
            self.root.unbind(sequence, funcid)
        self._key_bindings.clear()

    def _swap(self, build_frame) -> None:
        self._unbind_all_keys()
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = build_frame(self.container)
        self.current_frame.pack(fill="both", expand=True)

    def show_menu(self) -> None:
        self._swap(lambda parent: MenuFrame(parent, self))

    def show_title_card(self, theme: Theme) -> None:
        self._swap(lambda parent: TitleCardFrame(parent, self, theme))

    def show_game(self, theme: Theme) -> None:
        self._swap(lambda parent: GameFrame(parent, self, theme))

    def show_about(self) -> None:
        self._swap(lambda parent: AboutFrame(parent, self))

    def run(self) -> None:
        self.root.mainloop()


class MenuFrame(tk.Frame):
    def __init__(self, parent: tk.Misc, app: App) -> None:
        super().__init__(parent, bg=MENU_BG)
        self.app = app

        tk.Label(
            self, text=PROJECT_TITLE, font=("Segoe UI", 26, "bold"),
            fg=MENU_FG, bg=MENU_BG,
        ).pack(pady=(34, 4))
        tk.Label(
            self, text=PROJECT_SUBTITLE, font=("Segoe UI", 11, "italic"),
            fg=MENU_FG_DIM, bg=MENU_BG,
        ).pack(pady=(0, 22))

        for theme in (THEME_1918, THEME_2018):
            self._build_mode_button(theme)

        tk.Button(
            self, text="About this project", command=app.show_about,
            font=("Segoe UI", 10),
            bg="#1a1a1a", fg=MENU_FG,
            activebackground="#2a2a2a", activeforeground=MENU_FG,
            relief="flat", borderwidth=0, cursor="hand2",
            padx=12, pady=4,
        ).pack(pady=(20, 0))

        tk.Label(
            self, text="Choose a year. WASD to move. Esc to back out.",
            font=("Segoe UI", 9), fg=MENU_FG_DIM, bg=MENU_BG,
        ).pack(side="bottom", pady=14)

    def _build_mode_button(self, theme: Theme) -> None:
        on_click = lambda _e=None: self.app.show_title_card(theme)

        container = tk.Frame(
            self, bg=theme.palette.bg, cursor="hand2",
            highlightthickness=2,
            highlightbackground=theme.palette.accent,
            highlightcolor=theme.palette.accent,
        )
        container.pack(pady=6, padx=40, fill="x")
        container.bind("<Button-1>", on_click)

        for label_kwargs in (
            dict(text=theme.title, font=("Segoe UI", 22, "bold")),
            dict(text=theme.subtitle, font=("Segoe UI", 11, "italic")),
            dict(text=theme.menu_blurb, font=("Segoe UI", 10), wraplength=440),
        ):
            label = tk.Label(
                container, fg=theme.palette.text, bg=theme.palette.bg,
                cursor="hand2", **label_kwargs,
            )
            label.pack(pady=2)
            label.bind("<Button-1>", on_click)


class TitleCardFrame(tk.Frame):
    def __init__(self, parent: tk.Misc, app: App, theme: Theme) -> None:
        super().__init__(parent, bg=theme.palette.bg)
        self.app = app
        self.theme = theme

        tk.Label(
            self, text=theme.title, font=("Segoe UI", 36, "bold"),
            fg=theme.palette.text, bg=theme.palette.bg,
        ).pack(pady=(70, 2))
        tk.Label(
            self, text=theme.subtitle, font=("Segoe UI", 13, "italic"),
            fg=theme.palette.text, bg=theme.palette.bg,
        ).pack(pady=(0, 50))

        tk.Label(
            self, text="“" + theme.title_card_quote + "”",
            font=("Georgia", 14, "italic"),
            fg=theme.palette.text, bg=theme.palette.bg,
            wraplength=500, justify="center",
        ).pack(pady=10, padx=30)
        tk.Label(
            self, text="— " + theme.title_card_attribution,
            font=("Segoe UI", 10),
            fg=theme.palette.text, bg=theme.palette.bg,
        ).pack()

        tk.Label(
            self, text="Press any key to begin · Esc to return",
            font=("Segoe UI", 9),
            fg=theme.palette.text, bg=theme.palette.bg,
        ).pack(side="bottom", pady=24)

        app.bind_key("<Key>", self._on_key)

    def _on_key(self, event) -> None:
        if event.keysym == "Escape":
            self.app.show_menu()
        else:
            self.app.show_game(self.theme)


class GameFrame(tk.Frame):
    """Active gameplay: engine + Canvas + WASD."""

    def __init__(self, parent: tk.Misc, app: App, theme: Theme) -> None:
        super().__init__(parent, bg=theme.palette.bg)
        self.app = app
        self.theme = theme
        self.state = GameState.new(width=GRID_W, height=GRID_H)
        self._after_id: Optional[str] = None

        self.hud = tk.Label(
            self, text=self._hud_text(),
            font=("Segoe UI", 12, "bold"),
            fg=theme.palette.text, bg=theme.palette.bg,
        )
        self.hud.pack(pady=(8, 4))

        self.canvas = tk.Canvas(
            self, width=CANVAS_W, height=CANVAS_H,
            bg=theme.palette.bg,
            highlightthickness=0, bd=0,
        )
        self.canvas.pack()

        tk.Label(
            self, text="WASD to move · Esc for menu",
            font=("Segoe UI", 9),
            fg=theme.palette.text, bg=theme.palette.bg,
        ).pack(pady=(6, 0))

        app.bind_key("<Key>", self._on_key)
        self.bind("<Destroy>", self._on_destroy)

        self._draw()
        self._after_id = app.root.after(TICK_MS, self._tick)

    def _hud_text(self) -> str:
        return (
            f"{self.theme.title} · {self.theme.subtitle}"
            f"    Score: {self.state.score}"
        )

    def _tick(self) -> None:
        if not self.winfo_exists():
            return
        self.state.tick()
        self._draw()
        self.hud.config(text=self._hud_text())
        if self.state.game_over or self.state.won:
            self._cancel_loop()
            self._on_end()
        else:
            self._after_id = self.app.root.after(TICK_MS, self._tick)

    def _draw(self) -> None:
        canvas = self.canvas
        palette = self.theme.palette
        canvas.delete("all")
        for x in range(0, CANVAS_W + 1, CELL_SIZE):
            canvas.create_line(x, 0, x, CANVAS_H, fill=palette.grid)
        for y in range(0, CANVAS_H + 1, CELL_SIZE):
            canvas.create_line(0, y, CANVAS_W, y, fill=palette.grid)

        for i, (gx, gy) in enumerate(self.state.snake):
            cx = gx * CELL_SIZE + CELL_SIZE // 2
            cy = gy * CELL_SIZE + CELL_SIZE // 2
            if i == 0:
                glyph = self.theme.snake_head_glyph
            else:
                glyphs = self.theme.snake_body_glyphs
                glyph = glyphs[(i - 1) % len(glyphs)]
            canvas.create_text(
                cx, cy, text=glyph,
                font=(EMOJI_FONT_NAME, CELL_SIZE - 4),
            )

        if self.state.prey is not None:
            gx, gy = self.state.prey
            cx = gx * CELL_SIZE + CELL_SIZE // 2
            cy = gy * CELL_SIZE + CELL_SIZE // 2
            canvas.create_text(
                cx, cy, text=self.theme.prey_glyph,
                font=(EMOJI_FONT_NAME, CELL_SIZE - 4),
            )

    def _on_key(self, event) -> None:
        if event.keysym == "Escape":
            self._cancel_loop()
            self.app.show_menu()
            return
        direction = _KEY_TO_DIRECTION.get(event.keysym.lower())
        if direction is not None:
            self.state.set_direction(direction)

    def _cancel_loop(self) -> None:
        if self._after_id is not None:
            try:
                self.app.root.after_cancel(self._after_id)
            except tk.TclError:
                pass
            self._after_id = None

    def _on_destroy(self, event) -> None:
        if event.widget is self:
            self._cancel_loop()

    def _on_end(self) -> None:
        # Unit 5: freeze on the final state with an inline message.
        # Unit 6 will route to a dedicated GameOverFrame.
        end_text = "WIN" if self.state.won else "GAME OVER"
        self.hud.config(
            text=(
                f"{end_text} · final score {self.state.score} · "
                "Esc for menu"
            )
        )


class AboutFrame(tk.Frame):
    def __init__(self, parent: tk.Misc, app: App) -> None:
        super().__init__(parent, bg=MENU_BG)
        self.app = app

        tk.Label(
            self, text=PROJECT_TITLE, font=("Segoe UI", 20, "bold"),
            fg=MENU_FG, bg=MENU_BG,
        ).pack(pady=(20, 0))
        tk.Label(
            self, text=PROJECT_SUBTITLE, font=("Segoe UI", 10, "italic"),
            fg=MENU_FG_DIM, bg=MENU_BG,
        ).pack(pady=(0, 14))

        text_frame = tk.Frame(self, bg=MENU_BG)
        text_frame.pack(fill="both", expand=True, padx=24, pady=4)
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        text = tk.Text(
            text_frame, wrap="word",
            bg=MENU_BG, fg=MENU_FG,
            font=("Georgia", 11), borderwidth=0,
            yscrollcommand=scrollbar.set,
            padx=12, pady=12, highlightthickness=0,
        )
        text.insert("1.0", ABOUT_TEXT)
        text.config(state="disabled")
        text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text.yview)

        tk.Button(
            self, text="Back to menu", command=app.show_menu,
            font=("Segoe UI", 10),
            bg="#1a1a1a", fg=MENU_FG,
            activebackground="#2a2a2a", activeforeground=MENU_FG,
            relief="flat", borderwidth=0, cursor="hand2",
            padx=12, pady=4,
        ).pack(pady=14)

        app.bind_key("<Escape>", lambda e: app.show_menu())


if __name__ == "__main__":
    App().run()
