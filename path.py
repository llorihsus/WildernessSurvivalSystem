from collections import deque
from enum import Enum


class Move(Enum):
    """A single step; the value is how it changes (x, y). y grows going south."""
    N = (0, -1)
    S = (0, 1)
    E = (1, 0)
    NE = (1, -1)
    SE = (1, 1)


class Path:

    _path : deque[Move]
    
    _total_movement_cost : int
    _total_water_cost : int
    _total_food_cost : int

    def __init__(self):
        self._path = deque()
        self._total_movement_cost = 0
        self._total_water_cost = 0
        self._total_food_cost = 0

    @property
    def path(self) -> list[Move]:
        return list(self._path)
    @property
    def total_movement_cost(self) -> int:
        return self._total_movement_cost
    
    @property
    def total_water_cost(self) -> int:
        return self._total_water_cost

    @property
    def total_food_cost(self) -> int:
        return self._total_food_cost

    def add_step(self, move: Move, movement_cost : int, water_cost : int, food_cost : int) -> None:
        self._path.append(move)
        self._total_movement_cost += movement_cost
        self._total_water_cost += water_cost
        self._total_food_cost += food_cost
