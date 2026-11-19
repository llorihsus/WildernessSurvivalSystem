"""
This file contains the GameMap class, which builds the grid of terrain the
player travels across and handles the player's interactions with each square.
"""
from terrain import Terrain, Mountain, Desert, Swamp, Forest, Plains
from player import Player
from item import Gold
import random

class GameMap:
    """
    A rectangular map made of terrain squares.

    The map builds a random grid of terrain weighted by difficulty, places
    the player on it, and handles everything that happens when the player
    enters, rests on, or collects items from a square.
    """

    # (plains cutoff, forest cutoff) for each difficulty.
    # A random value below the plains cutoff makes Plains, below the forest
    # cutoff makes Forest, and anything else makes Swamp, Desert, or Mountain.
    TERRAIN_WEIGHTS = {
        "easy": (0.6, 0.85),    # 60% Plains, 25% Forest, 15% Swamp/Desert/Mountain
        "medium": (0.35, 0.6),  # 35% Plains, 25% Forest, 40% Swamp/Desert/Mountain
        "hard": (0.15, 0.35),   # 15% Plains, 20% Forest, 65% Swamp/Desert/Mountain
    }

    def __init__(self, width : int, height : int, difficulty : str):
        """
        Create a map filled with random terrain weighted by difficulty.

        Args:
            width: Number of squares in each row.
            height: Number of rows.
            difficulty: "easy", "medium", or "hard".
        """

        # using double underscore naming convention to show the variable is private
        self.__width = width
        self.__height = height
        self.__difficulty = difficulty

        self.__squares : list[list[Terrain]] = GameMap.populate(width, height, difficulty)

    # Read only access to private attributes
    @property
    def width(self) -> int:
        """Number of squares in each row."""
        return self.__width

    @property
    def height(self) -> int:
        """Number of rows."""
        return self.__height

    @property
    def difficulty(self) -> str:
        """The difficulty the map was built with."""
        return self.__difficulty

    @staticmethod
    def populate(width, height, difficulty):
        """
        Build and return a height x width grid of randomly chosen terrain.

        Each square is picked using the TERRAIN_WEIGHTS for the difficulty.
        Harder difficulties have fewer Plains and Forest squares and more
        Swamp, Desert, and Mountain squares.

        Args:
            width: Number of squares in each row.
            height: Number of rows.
            difficulty: "easy", "medium", or "hard".

        Returns:
            A list of rows, where each row is a list of Terrain objects.
        """
        squares = [[None for _ in range(width)] for _ in range(height)]

        plain_cutoff, forest_cutoff = GameMap.TERRAIN_WEIGHTS[difficulty]
        for row in range(height):
            for column in range(width):
                random_value = random.random()
                if random_value < plain_cutoff:
                    terrain = Plains()
                elif random_value < forest_cutoff:
                    terrain = Forest()
                else:
                    terrain = random.choice([Swamp, Desert, Mountain])()

                squares[row][column] = terrain

        return squares

    def display(self, terrain_emojis):
        """
        Print the map, one row per line, using an emoji for each terrain.

        Args:
            terrain_emojis: A dictionary that maps each terrain name, such
                as "plains", to the emoji to print for it.
        """
        for row in self.__squares:
            print(" ".join(terrain_emojis[terrain.name] for terrain in row))

    def get_terrain(self, x, y):
        """
        Get the terrain at the given coordinates.

        Args:
            x: Column of the square, starting at 0 on the left.
            y: Row of the square, starting at 0 at the top.

        Returns:
            The Terrain object at (x, y).

        Raises:
            IndexError: If (x, y) is outside the map.
        """
        if 0 <= x < self.__width and 0 <= y < self.__height:
            return self.__squares[y][x]
        else:
            raise IndexError("Coordinates out of bounds")

    def can_enter_square(self, player: Player, new_x, new_y) -> bool:
        """
        Check whether the player has enough supplies to enter a square.

        Args:
            player: The player trying to move.
            new_x: Column of the square the player wants to enter.
            new_y: Row of the square the player wants to enter.

        Returns:
            True if the player has enough water, food, and movement points
            to pay that square's entry costs; otherwise False.
        """
        terrain = self.get_terrain(new_x, new_y)
        if player.curr_water < terrain.water_cost:
            return False
        if player.curr_food < terrain.food_cost:
            return False
        if player.move_pts < terrain.movement_cost:
            return False

        return True

    def can_stay_on_square(self, player: Player) -> bool:
        """
        Check whether the player has enough supplies to rest on their square.

        Staying costs half the normal water and food cost and no movement points.

        Args:
            player: The player who wants to rest.

        Returns:
            True if the player has enough water and food to rest; otherwise False.
        """
        terrain = self.get_terrain(player.curr_x, player.curr_y)
        if player.curr_water < terrain.water_cost * 1/2:
            return False
        if player.curr_food < terrain.food_cost * 1/2:
            return False

        return True

    def square_entered(self, player: Player):
        """
        Describe the player's current square and charge its full entry cost.

        Call this after the player's position has been updated to the new
        square.

        Args:
            player: The player who just entered the square.
        """
        terrain = self.get_terrain(player.curr_x, player.curr_y)
        terrain.terrain_entered()
        # Deduct the entry costs from the player's supplies
        player.change_curr_water(-terrain.water_cost)
        player.change_curr_food(-terrain.food_cost)
        player.change_move_pts(-terrain.movement_cost)

    def stayed_in_square(self, player: Player):
        """
        Let the player rest on their current square for a turn.

        Resting costs half the square's water and food cost (rounded down)
        and gives back 2 movement points.

        Args:
            player: The player who is resting.
        """
        terrain = self.get_terrain(player.curr_x, player.curr_y)
        terrain.stayed_in_terrain()
        # Resting costs half of the supplies (rounded down) and recovers movement
        player.change_curr_water(-int(terrain.water_cost * 1/2))
        player.change_curr_food(-int(terrain.food_cost * 1/2))
        player.change_move_pts(2)

    def spawn_player(self, player : Player):
        """
        Place the player in the middle of the map's left edge and enter
        that square.

        Args:
            player: The player to place on the map.
        """
        player.curr_x = 0
        player.curr_y = self.__height // 2
        self.square_entered(player)

    def collect_items(self, player : Player):
        """
        Give the player every resource on their current square.

        Gold is added straight to the player's gold; water and food go
        into the player's inventory. Repeat-bonus items stay on the square.

        Args:
            player: The player collecting the items.
        """
        terrain = self.get_terrain(player.curr_x, player.curr_y)
        for item in terrain.take_all_items():
            if isinstance(item, Gold):
                player.change_curr_gold(item.bonus)
            else:
                player.collect_item(item)
