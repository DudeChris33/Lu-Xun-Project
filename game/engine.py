"""Pure-Python game state for Snake. No tkinter, no I/O.

The engine is UI-agnostic: tick() advances state, set_direction() queues
a direction change for the next tick. The UI is responsible for rendering
the snake/prey positions and translating keypresses into set_direction().
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from random import Random
from typing import Optional


Cell = tuple[int, int]


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def opposite(self) -> "Direction":
        dx, dy = self.value
        return Direction((-dx, -dy))


DEFAULT_WIDTH = 30
DEFAULT_HEIGHT = 30


@dataclass
class GameState:
    width: int
    height: int
    snake: deque
    direction: Direction
    pending_direction: Optional[Direction]
    prey: Optional[Cell]
    score: int
    game_over: bool
    won: bool
    rng: Random

    @classmethod
    def new(
        cls,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        seed: Optional[int] = None,
    ) -> "GameState":
        rng = Random(seed)
        head = (width // 2, height // 2)
        state = cls(
            width=width,
            height=height,
            snake=deque([head]),
            direction=Direction.RIGHT,
            pending_direction=None,
            prey=None,
            score=0,
            game_over=False,
            won=False,
            rng=rng,
        )
        state.prey = state._spawn_prey()
        return state

    def set_direction(self, direction: Direction) -> None:
        if self.game_over or self.won:
            return
        if direction == self.direction.opposite:
            return
        self.pending_direction = direction

    def tick(self) -> None:
        if self.game_over or self.won:
            return

        if self.pending_direction is not None:
            self.direction = self.pending_direction
            self.pending_direction = None

        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)

        nx, ny = new_head
        if not (0 <= nx < self.width and 0 <= ny < self.height):
            self.game_over = True
            return

        eating = (new_head == self.prey)
        # When eating, tail stays — collision check includes full snake.
        # When moving, tail vacates — old tail cell is allowed.
        body = set(self.snake) if eating else set(list(self.snake)[:-1])
        if new_head in body:
            self.game_over = True
            return

        self.snake.appendleft(new_head)
        if eating:
            self.score += 1
            new_prey = self._spawn_prey()
            if new_prey is None:
                self.won = True
                self.prey = None
            else:
                self.prey = new_prey
        else:
            self.snake.pop()

    def _spawn_prey(self) -> Optional[Cell]:
        snake_set = set(self.snake)
        free = [
            (x, y)
            for x in range(self.width)
            for y in range(self.height)
            if (x, y) not in snake_set
        ]
        if not free:
            return None
        return self.rng.choice(free)
