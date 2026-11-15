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



def main():
    """Run the Wilderness Survival System."""
    print("Welcome to the Wilderness Survival System")

    width = get_dimension("width")
    height = get_dimension("height")

    game_map = GameMap(width, height)


if __name__ == "__main__":
    main()