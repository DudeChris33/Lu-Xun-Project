"""Engine unit tests. Stdlib unittest only — no tkinter, no pytest.

Run from project root:
    python -m unittest discover tests
"""

import unittest
from collections import deque

from game.engine import Direction, GameState


class TestInitialState(unittest.TestCase):
    def test_defaults(self):
        state = GameState.new(seed=0)
        self.assertEqual(state.width, 30)
        self.assertEqual(state.height, 30)
        self.assertEqual(len(state.snake), 1)
        self.assertEqual(state.direction, Direction.RIGHT)
        self.assertEqual(state.score, 0)
        self.assertFalse(state.game_over)
        self.assertFalse(state.won)
        self.assertIsNotNone(state.prey)

    def test_prey_not_on_snake_at_start(self):
        for seed in range(20):
            state = GameState.new(width=5, height=5, seed=seed)
            self.assertNotIn(state.prey, set(state.snake))


class TestMovement(unittest.TestCase):
    def test_tick_moves_head_in_direction(self):
        state = GameState.new(width=10, height=10, seed=0)
        state.prey = (0, 0)  # ensure no eating
        head_before = state.snake[0]
        state.tick()
        dx, dy = Direction.RIGHT.value
        self.assertEqual(state.snake[0], (head_before[0] + dx, head_before[1] + dy))

    def test_tick_preserves_length_when_not_eating(self):
        state = GameState.new(width=20, height=20, seed=1)
        state.prey = (0, 0)
        original_length = len(state.snake)
        state.tick()
        self.assertEqual(len(state.snake), original_length)


class TestEating(unittest.TestCase):
    def test_eating_grows_chain_and_increments_score(self):
        state = GameState.new(width=10, height=10, seed=0)
        head_x, head_y = state.snake[0]
        dx, dy = state.direction.value
        prey_pos = (head_x + dx, head_y + dy)
        state.prey = prey_pos
        len_before = len(state.snake)
        score_before = state.score
        state.tick()
        self.assertEqual(len(state.snake), len_before + 1)
        self.assertEqual(state.score, score_before + 1)
        self.assertNotEqual(state.prey, prey_pos)


class TestPreySpawn(unittest.TestCase):
    def test_prey_never_spawns_on_snake(self):
        state = GameState.new(width=5, height=5, seed=0)
        state.snake = deque([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1)])
        for _ in range(50):
            prey = state._spawn_prey()
            self.assertIsNotNone(prey)
            self.assertNotIn(prey, set(state.snake))


class TestCollisions(unittest.TestCase):
    def test_wall_collision_ends_game(self):
        state = GameState.new(width=10, height=10, seed=0)
        state.snake = deque([(9, 5)])
        state.direction = Direction.RIGHT
        state.prey = (0, 0)
        state.tick()
        self.assertTrue(state.game_over)

    def test_self_collision_ends_game(self):
        state = GameState.new(width=10, height=10, seed=0)
        # Five-segment snake; head moving LEFT crashes into the body cell at (4,5).
        state.snake = deque([(5, 5), (5, 4), (4, 4), (4, 5), (4, 6)])
        state.direction = Direction.LEFT
        state.prey = (0, 0)
        state.tick()
        self.assertTrue(state.game_over)

    def test_moving_into_old_tail_does_not_crash(self):
        # When not eating, the tail cell vacates — head may step into it.
        state = GameState.new(width=10, height=10, seed=0)
        state.snake = deque([(5, 5), (5, 4), (4, 4), (4, 5)])
        state.direction = Direction.LEFT  # head (5,5) -> (4,5), the current tail
        state.prey = (0, 0)
        state.tick()
        self.assertFalse(state.game_over)
        self.assertEqual(state.snake[0], (4, 5))


class TestDirectionBuffering(unittest.TestCase):
    def test_reverse_direction_rejected(self):
        state = GameState.new(width=10, height=10, seed=0)
        state.prey = (0, 0)
        state.set_direction(Direction.LEFT)  # opposite of default RIGHT
        head_before = state.snake[0]
        state.tick()
        self.assertEqual(state.direction, Direction.RIGHT)
        self.assertEqual(state.snake[0], (head_before[0] + 1, head_before[1]))

    def test_perpendicular_direction_applied_on_tick(self):
        state = GameState.new(width=10, height=10, seed=0)
        state.prey = (0, 0)
        state.set_direction(Direction.DOWN)
        head_before = state.snake[0]
        state.tick()
        self.assertEqual(state.direction, Direction.DOWN)
        self.assertEqual(state.snake[0], (head_before[0], head_before[1] + 1))


class TestWinAndPostGameOver(unittest.TestCase):
    def test_full_grid_triggers_win(self):
        state = GameState.new(width=2, height=2, seed=0)
        state.snake = deque([(1, 0), (0, 0), (0, 1)])
        state.direction = Direction.DOWN  # head (1,0) -> (1,1)
        state.prey = (1, 1)
        state.score = 0
        state.tick()
        self.assertTrue(state.won)
        self.assertFalse(state.game_over)
        self.assertEqual(state.score, 1)
        self.assertEqual(len(state.snake), 4)
        self.assertIsNone(state.prey)

    def test_tick_after_game_over_is_noop(self):
        state = GameState.new(width=10, height=10, seed=0)
        state.snake = deque([(9, 5)])
        state.direction = Direction.RIGHT
        state.prey = (0, 0)
        state.tick()
        self.assertTrue(state.game_over)
        snake_snapshot = list(state.snake)
        score_snapshot = state.score
        for _ in range(3):
            state.tick()
        self.assertEqual(list(state.snake), snake_snapshot)
        self.assertEqual(state.score, score_snapshot)


if __name__ == "__main__":
    unittest.main()
