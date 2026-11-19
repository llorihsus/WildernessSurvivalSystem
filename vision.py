from __future__ import annotations
from typing import TYPE_CHECKING

from path import Path
from item import Food, Water, Gold
from trader import Trader

# Only used in type hints, so they are skipped at runtime to avoid a circular import
if TYPE_CHECKING:
    from map import GameMap
    from player import Player
    from terrain import Terrain

class Vision:
    neighboring_squares: tuple[int, int, int]               # number of squares visible to the [north, south, east]
    vision_path: Path                                       # a certain path from visible vision per brain's request (closest_food, closest_water, etc.)
    player_pos: tuple[int, int]                             # current position of player (x, y)
    vision_map: GameMap                                     # map stored for vision
    vision: list[list[Terrain]]                             # 2D array representation of current vision w/ visible terrain
    has_items: list[tuple[tuple[int, int], int]]            # [has_item square's x,y coords, distance]

    def __init__(self, neighboring_squares: tuple[int, int, int], game_map: GameMap, player: Player):
        self.neighboring_squares = neighboring_squares      # [north, south, east]
        self.player_pos = (player.curr_x, player.curr_y)
        self.vision_map = game_map
        self.vision = []
        self.has_items = []
        self.vision_path = Path(0, 0, 0, 0)

        self.update_vision(self.player_pos[0], self.player_pos[1])


    def update_vision(self, curr_x: int, curr_y: int) -> list[list[Terrain]]:
        """
        Rebuild the grid of terrain the player can currently see.

        The player sees range_north rows above them, range_south rows below
        them, and range_east columns to their right. Squares past the edge
        of the map are left out.

        Args:
            curr_x: The player's column on the map.
            curr_y: The player's row on the map.

        Returns:
            The visible terrain as a list of rows, top row first.
        """
        range_north, range_south, range_east = self.neighboring_squares

        # Keep the visible area inside the edges of the map
        top = max(curr_y - range_north, 0)
        bottom = min(curr_y + range_south, self.vision_map.height - 1)
        right = min(curr_x + range_east, self.vision_map.width - 1)

        # Start fresh so squares from an earlier position don't pile up
        self.vision = []
        for y in range(top, bottom + 1):
            col = [self.vision_map.get_terrain(x, y) for x in range(curr_x, right + 1)]
            self.vision.append(col)

        return self.vision

    def closest_food(self) -> Path:
        has_food = []
        for row_index, row in enumerate(self.vision):
            for col_index, terrain in enumerate(row):
                terrain_item = terrain.getItem()

                if isinstance(terrain_item, Food):
                    food_distance = abs(self.player_pos[0] - row_index) + abs(self.player_pos[1] - col_index)
                    has_food.append(((row_index, col_index), food_distance))

        self.has_items = has_food

        if not has_food:
            print("No food seen in the vicinity.")
            return self.vision_path

        closest = min(has_food, key=lambda x: x[1])

        food_x, food_y = closest[0]
        player_x, player_y = self.player_pos

        self.vision_path = Path(
            # max prevents movement direction from going negative
            max(player_x - food_x, 0),          # move north (player position - row index of closest food)
            max(food_x - player_x, 0),          # move south (row index of closest food - player position)
            max(food_y - player_y, 0),          # move east (col index of closest food - player position)
            max(player_y - food_y, 0)           # move west (player positon - col index of closest food)
        )

        return self.vision_path

    def second_closest_food(self) -> Path:
        self.closest_food()                             # updates has_items

        has_food = self.has_items.copy()

        if len(has_food) < 2:
            print("Food is only seen once (or not seen) in the vicinity")
            return self.vision_path

        closest = min(has_food, key=lambda x: x[1])
        has_food.remove(closest)
        second_closest = min(has_food, key=lambda x: x[1])

        food_x, food_y = second_closest[0]
        player_x, player_y = self.player_pos

        self.vision_path = Path(
            max(player_x - food_x, 0),
            max(food_x - player_x, 0),
            max(food_y - player_y, 0),
            max(player_y - food_y, 0)
        )

        return self.vision_path

    def closest_water(self) -> Path:
        has_water = []

        for row_index, row in enumerate(self.vision):
            for col_index, terrain in enumerate(row):
                terrain_item = terrain.getItem()

                if isinstance(terrain_item, Water):
                    water_distance = abs(self.player_pos[0] - row_index) + abs(self.player_pos[1] - col_index)
                    has_water.append(((row_index, col_index), water_distance))

        self.has_items = has_water

        if not has_water:
            print("No water seen in the vicinity.")
            return self.vision_path

        closest = min(has_water, key=lambda x: x[1])

        water_x, water_y = closest[0]
        player_x, player_y = self.player_pos

        self.vision_path = Path(
            # max prevents movement direction from going negative
            max(player_x - water_x, 0),         # move north (player position - row index of closest water)
            max(water_x - player_x, 0),         # move south (row index of closest water - player position)
            max(water_y - player_y, 0),         # move east (col index of closest water - player position)
            max(player_y - water_y, 0)          # move west (player positon - col index of closest water)
        )

        return self.vision_path

    def second_closest_water(self) -> Path:
        self.closest_water()                            # updates has_items

        has_water = self.has_items.copy()

        if len(has_water) < 2:
            print("Water is only seen once (or not seen) in the vicinity")
            return self.vision_path

        closest = min(has_water, key=lambda x: x[1])
        has_water.remove(closest)
        second_closest = min(has_water, key=lambda x: x[1])

        water_x, water_y = second_closest[0]
        player_x, player_y = self.player_pos

        self.vision_path = Path(
            max(player_x - water_x, 0),
            max(water_x - player_x, 0),
            max(water_y - player_y, 0),
            max(player_y - water_y, 0)
        )
        return self.vision_path

    def closest_gold(self) -> Path:
        has_gold = []

        for row_index, row in enumerate(self.vision):
            for col_index, terrain in enumerate(row):
                terrain_item = terrain.getItem()

                if isinstance(terrain_item, Gold):
                    gold_distance = abs(self.player_pos[0] - row_index) + abs(self.player_pos[1] - col_index)
                    has_gold.append(((row_index, col_index), gold_distance))

        self.has_items = has_gold

        if not has_gold:
            print("No gold seen in the vicinity.")
            return self.vision_path

        closest = min(has_gold, key=lambda x: x[1])

        gold_x, gold_y = closest[0]
        player_x, player_y = self.player_pos

        self.vision_path = Path(
            # max prevents movement direction from going negative
            max(player_x - gold_x, 0),          # move north (player position - row index of closest gold)
            max(gold_x - player_x, 0),          # move south (row index of closest gold - player position)
            max(gold_y - player_y, 0),          # move east (col index of closest gold - player position)
            max(player_y - gold_y, 0)           # move west (player positon - col index of closest gold)
        )

        return self.vision_path

    def second_closest_gold(self) -> Path:
        self.closest_gold()                             # updates has_items

        has_gold = self.has_items.copy()

        if len(has_gold) < 2:
            print("Gold is only seen once (or not seen) in the vicinity")
            return self.vision_path

        closest = min(has_gold, key=lambda x: x[1])
        has_gold.remove(closest)
        second_closest = min(has_gold, key=lambda x: x[1])

        gold_x, gold_y = second_closest[0]
        player_x, player_y = self.player_pos

        self.vision_path = Path(
            max(player_x - gold_x, 0),
            max(gold_x - player_x, 0),
            max(gold_y - player_y, 0),
            max(player_y - gold_y, 0)
        )
        return self.vision_path

    def closest_trader(self) -> Path:
        has_trader = []

        for row_index, row in enumerate(self.vision):
            for col_index, terrain in enumerate(row):
                terrain_item = terrain.getItem()

                if isinstance(terrain_item, Trader):
                    trader_distance = abs(self.player_pos[0] - row_index) + abs(self.player_pos[1] - col_index)
                    has_trader.append(((row_index, col_index), trader_distance))

        self.has_items = has_trader

        if not has_trader:
            print("No trader seen in the vicinity.")
            return self.vision_path

        closest = min(has_trader, key=lambda x: x[1])

        trader_x, trader_y = closest[0]
        player_x, player_y = self.player_pos

        self.vision_path = Path(
            # max prevents movement direction from going negative
            max(player_x - trader_x, 0),        # move north (player position - row index of closest trader)
            max(trader_x - player_x, 0),        # move south (row index of closest trader - player position)
            max(trader_y - player_y, 0),        # move east (col index of closest trader - player position)
            max(player_y - trader_y, 0)         # move west (player positon - col index of closest trader)
        )

        return self.vision_path

    def second_closest_trader(self) -> Path:
        self.closest_trader()                           # updates has_items

        has_trader = self.has_items.copy()

        if len(has_trader) < 2:
            print("Trader is only seen once (or not seen) in the vicinity")
            return self.vision_path

        closest = min(has_trader, key=lambda x: x[1])
        has_trader.remove(closest)
        second_closest = min(has_trader, key=lambda x: x[1])

        trader_x, trader_y = second_closest[0]
        player_x, player_y = self.player_pos

        self.vision_path = Path(
            max(player_x - trader_x, 0),
            max(trader_x - player_x, 0),
            max(trader_y - player_y, 0),
            max(player_y - trader_y, 0)
        )
        return self.vision_path

    def easiest_path(self) -> Path:
        least_move_cost = 10000                 # arbitary initial number to get least cost
        least_cost_square = ()

        for row_index, row in enumerate(self.vision):
                for col_index, terrain in enumerate(row):
                    terrain_move_cost = terrain.movement_cost
                    if terrain_move_cost < least_move_cost:
                        least_cost_square = (row_index, col_index)

        least_x, least_y = least_cost_square
        player_x, player_y = self.player_pos

        self.vision_path = Path(
                    max(player_x - least_x, 0),
                    max(least_x - player_x, 0),
                    max(least_y - player_y, 0),
                    max(player_y - least_y, 0)
                )
        return self.vision_path
