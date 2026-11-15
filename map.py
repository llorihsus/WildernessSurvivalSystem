from terrain import Mountain, Desert, Swamp, Forest, Plains
import random

class GameMap:
    """Represents a rectangular map made of terrain squares."""

    # (plains cutoff, forest cutoff) for each difficulty.
    # A random value below the plains cutoff makes Plains, below the forest
    # cutoff makes Forest, and anything else makes Swamp, Desert, or Mountain.
    TERRAIN_WEIGHTS = {
        "easy": (0.6, 0.85),    # 60% Plains, 25% Forest, 15% Swamp/Desert/Mountain
        "medium": (0.35, 0.6),  # 35% Plains, 25% Forest, 40% Swamp/Desert/Mountain
        "hard": (0.15, 0.35),   # 15% Plains, 20% Forest, 65% Swamp/Desert/Mountain
    }

    def __init__(self, width, height, difficulty):
        """
        Create a map of the given width and height, filled with random
        terrain weighted by the selected difficulty.
        """

        self.width = width
        self.height = height
        self.difficulty = difficulty

        self._squares = self.populate(width, height, difficulty)

    def populate(self, width, height, difficulty):
        """
        Build and return a height x width grid of randomly chosen terrain.

        Each square is picked using the TERRAIN_WEIGHTS for the difficulty.
        Harder difficulties have fewer Plains and Forest squares and more
        Swamp, Desert, and Mountain squares.
        """
        squares = [[None for _ in range(width)] for _ in range(height)]

        plain_cutoff, forest_cutoff = self.TERRAIN_WEIGHTS[difficulty]
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
        """Display the map using terrain emojis."""
        for row in self._squares:
            print(" ".join(terrain_emojis[terrain.name] for terrain in row))