class GameMap:
    """Represents a rectangular map made of terrain squares."""

    VALID_TERRAINS = {
        "plains",
        "mountain",
        "desert",
        "swamp",
        "forest",
    }

    def __init__(self, width, height, default_terrain="plains"):
        """
        Create a map using the width and height supplied by the WSS file.
        """
        self.check_dimension(width, "width")
        self.check_dimension(height, "height")

        self.width = width
        self.height = height

        self._validate_terrain(default_terrain)

        self._squares = [
            [default_terrain for _ in range(width)]
            for _ in range(height)
        ]

    @staticmethod
    def check_dimension(value, name):
        """Check if the map dimension is correct."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")

        if value <= 0:
            raise ValueError(f"{name} must be greater than zero")

    @staticmethod
    def _validate_terrain(terrain):
        """Check if a terrain type is valid."""
        if terrain not in GameMap.VALID_TERRAINS:
            raise ValueError(f"Invalid terrain type: {terrain}")

    def populate(self, difficulty):
        """
        Populate the map based on the selected difficulty.

        Easy:
            Mostly plains with some forest.

        Medium:
            Uses plains, forest, desert, and mountain.

        Hard:
            Uses all available terrain types.
        """
        valid_difficulties = {"easy", "medium", "hard"}

        if difficulty not in valid_difficulties:
            raise ValueError(
                "Difficulty must be easy, medium, or hard"
            )

        for row in range(self.height):
            for column in range(self.width):

                if difficulty == "easy":
                    # Easy maps contain mostly plains.
                    if (row + column) % 7 == 0:
                        terrain = "forest"
                    else:
                        terrain = "plains"

                elif difficulty == "medium":
                    # Medium maps use four different terrain types.
                    terrain_pattern = [
                        "plains",
                        "forest",
                        "desert",
                        "mountain",
                    ]

                    terrain = terrain_pattern[
                        (row + column) % len(terrain_pattern)
                    ]

                else:
                    # Hard maps use every available terrain type.
                    terrain_pattern = [
                        "plains",
                        "mountain",
                        "desert",
                        "swamp",
                        "forest",
                        "water",
                    ]

                    terrain = terrain_pattern[
                        (row * self.width + column)
                        % len(terrain_pattern)
                    ]

                self._squares[row][column] = terrain

    def display(self, terrain_emojis):
        """Display the map using terrain emojis."""
        for row in self._squares:
            print(" ".join(terrain_emojis[terrain] for terrain in row))