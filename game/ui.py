"""Tkinter UI shell.

Frame-based screens swapped in a single container by App. Key bindings
live on the root window and are tracked centrally so they're cleared on
each frame swap — avoids stale handlers calling into destroyed frames.

GameFrame is a stub here; Unit 5 wires it to the engine.
"""

from __future__ import annotations

import tkinter as tk

from game.content import ABOUT_TEXT, PROJECT_SUBTITLE, PROJECT_TITLE
from game.themes import THEME_1918, THEME_2018, Theme


MENU_BG = "#0c0c0c"
MENU_FG = "#e8e8e8"
MENU_FG_DIM = "#999999"

WINDOW_SIZE = 600
WINDOW_TITLE = "Snake — Lu Xun Edition"


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
    """Stub for Unit 4. Gameplay wired in Unit 5."""

    def __init__(self, parent: tk.Misc, app: App, theme: Theme) -> None:
        super().__init__(parent, bg=theme.palette.bg)
        self.app = app
        self.theme = theme

        tk.Label(
            self,
            text=f"[Game canvas — {theme.title} — Unit 5 stub]",
            fg=theme.palette.text, bg=theme.palette.bg,
            font=("Segoe UI", 14),
        ).pack(expand=True)
        tk.Label(
            self, text="Esc to return to menu",
            fg=theme.palette.text, bg=theme.palette.bg,
            font=("Segoe UI", 10),
        ).pack(pady=20)

        app.bind_key("<Escape>", lambda e: app.show_menu())


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
