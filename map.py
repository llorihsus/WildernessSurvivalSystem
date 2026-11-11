class GameMap:
    """Represents a rectangular map made of terrain squares."""

    VALID_TERRAINS = {
        "plains",
        "mountain",
        "desert",
        "swamp",
        "forest",
        "water",
    }

    def __init__(self, width, height, default_terrain="plains"):
        """
        Create a map using the width and height supplied by the WSS file.
        """
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self._validate_terrain(default_terrain)

        self.width = width
        self.height = height

        self._squares = [
            [default_terrain for _ in range(width)]
            for _ in range(height)
        ]

    @staticmethod
    def _validate_dimension(value, name):
        """Validate one map dimension."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")

        if value <= 0:
            raise ValueError(f"{name} must be greater than zero")