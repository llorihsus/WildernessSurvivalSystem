"""Moves and paths that a player can take across the map."""

from collections import deque  # moves are added to the end of path and taken from the front
from enum import Enum

class Move(Enum):
    """A single step; the value is how it changes (x, y). y grows going south."""
    N = (0, -1)
    S = (0, 1)
    E = (1, 0)
    NE = (1, -1)
    SE = (1, 1)


class Path:
    """An ordered list of moves along with the total cost of taking them.

    Steps are added to the end with add_step, which also adds the movement,
    water, and food cost of the square each step enters, so the totals always
    match the steps in the path.
    """

    _path : deque[Move]

    _total_movement_cost : int
    _total_water_cost : int
    _total_food_cost : int

    def __init__(self):
        """Create an empty path with all costs set to zero."""
        self._path = deque()
        self._total_movement_cost = 0
        self._total_water_cost = 0
        self._total_food_cost = 0

    @property
    def path(self) -> list[Move]:
        """A copy of the moves in this path, in order."""
        return list(self._path)
    @property
    def total_movement_cost(self) -> int:
        """The total movement cost of every step in this path."""
        return self._total_movement_cost

    @property
    def total_water_cost(self) -> int:
        """The total water cost of every step in this path."""
        return self._total_water_cost

    @property
    def total_food_cost(self) -> int:
        """The total food cost of every step in this path."""
        return self._total_food_cost

    def add_step(self, move: Move, movement_cost : int, water_cost : int, food_cost : int) -> None:
        """Add a move to the end of the path and add its costs to the totals.

        Args:
            move: The step to take.
            movement_cost: The movement cost of the square the step enters.
            water_cost: The water cost of the square the step enters.
            food_cost: The food cost of the square the step enters.
        """
        self._path.append(move)
        self._total_movement_cost += movement_cost
        self._total_water_cost += water_cost
        self._total_food_cost += food_cost
