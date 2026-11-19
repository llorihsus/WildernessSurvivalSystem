"""
This file contains the Item class and its subclasses: Food, Gold, and Water.
These classes represent the different types of items the player can collect
from the terrain on the game map.
"""
class Item:
    """
    Base class for every collectible item in the game.

    Every item has a name, a bonus amount it gives the player, and a flag
    saying whether it stays in the terrain after being collected.
    """

    def __init__(self, name: str, bonus: int, repeat_bonus: bool = False):
        """
        Create a new item.

        Args:
            name: The item's display name, such as "River Water".
            bonus: How much the item gives the player when collected.
            repeat_bonus: True if the item stays in the terrain so it can
                be collected again; False if it is removed once collected.
        """
        self._name = name
        self._bonus = bonus
        self._repeat_bonus = repeat_bonus

    @property
    def name(self) -> str:
        """The item's display name."""
        return self._name

    @property
    def bonus(self) -> int:
        """How much the item gives the player when collected."""
        return self._bonus

    @property
    def repeat_bonus(self) -> bool:
        """True if the item stays in the terrain after being collected."""
        return self._repeat_bonus

    def display_item(self) -> str:
        """
        Build a readable summary of the item.

        Returns:
            A string with the item's name and bonus, one per line.
        """
        return f"Name: {self._name}\nBonus: {self._bonus}"


class Food(Item):
    """
    A food item that restores the player's food supply.

    Food goes into the player's inventory when collected.
    """

    def __init__(self, name: str, cost : int, bonus: int, repeat_bonus: bool = False):
        """
        Create a new food item.

        Args:
            name: The food's display name, such as "Rabbit".
            cost: The food's cost.
            bonus: How much food the item restores.
            repeat_bonus: True if the food stays in the terrain so it can
                be collected again.
        """
        super().__init__(name, bonus, repeat_bonus)
        self._cost = cost

    @property
    def cost(self) -> int:
        """The food's cost."""
        return self._cost

    def display_item(self) -> str:
        """
        Build a readable summary of the food item.

        Returns:
            A string with the food's name, bonus, and cost, one per line.
        """
        return f"Name: {self._name}\nBonus: {self._bonus}\nCost: {self._cost}"


class Gold(Item):
    """
    A gold item that adds to the player's wealth.

    Collecting gold adds its bonus straight to the player's gold instead of
    going into the inventory. Gold is never a repeat bonus, so it disappears
    from the terrain once collected.
    """

    def __init__(self, name: str, bonus: int):
        """
        Create a new gold item.

        Args:
            name: The gold's display name, such as "Gold Nugget".
            bonus: How much gold the player gains when collecting it.
        """
        # Gold can only be collected once, so repeat_bonus is always False
        super().__init__(name, bonus, False)


class Water(Item):
    """
    A water item that restores the player's water supply.

    Water goes into the player's inventory when collected.
    """

    def __init__(self, name: str, cost : int, bonus: int, repeat_bonus: bool = False):
        """
        Create a new water item.

        Args:
            name: The water's display name, such as "River Water".
            cost: The water's cost.
            bonus: How much water the item restores.
            repeat_bonus: True if the water stays in the terrain so it can
                be collected again.
        """
        super().__init__(name, bonus, repeat_bonus)
        self._cost = cost

    @property
    def cost(self) -> int:
        """The water's cost."""
        return self._cost

    def display_item(self) -> str:
        """
        Build a readable summary of the water item.

        Returns:
            A string with the water's name, bonus, and cost, one per line.
        """
        return f"Name: {self._name}\nBonus: {self._bonus}\nCost: {self._cost}"
