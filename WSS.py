"""
World State System (WSS)

This file gets the map width and height from the user, creates the map,
displays terrain using emojis, and controls basic player movement.
"""

from map import GameMap


TERRAIN_EMOJIS = {
    "plains": "🌱",
    "mountain": "⛰️",
    "desert": "🏜️",
    "swamp": "🐊",
    "forest": "🌲",
}


def get_dimension(name):
    """Ask the user for a positive map dimension."""
    while True:
        try:
            value = int(input(f"Enter map {name}: "))

            if value > 0:
                return value

            print(f"{name.capitalize()} must be greater than zero.")

        except ValueError:
            print(f"Please enter a whole number for the map {name}.")


def get_difficulty():
    """Ask the user to select a map difficulty."""
    while True:
        difficulty = input(
            "Enter map difficulty (easy, medium, or hard): "
        ).lower()

        if difficulty in {"easy", "medium", "hard"}:
            return difficulty

        print("Please enter easy, medium, or hard.")


def main():
    """Run the Wilderness Survival System."""
    print("Welcome to the Wilderness Survival System")

    width = get_dimension("width")
    height = get_dimension("height")

    difficulty = get_difficulty()

    game_map = GameMap(width, height, difficulty)

    print(f"\nGenerated {difficulty} map:")
    game_map.display(TERRAIN_EMOJIS)


if __name__ == "__main__":
    main()