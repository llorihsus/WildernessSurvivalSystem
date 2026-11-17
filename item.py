"""
    This file contains the Item class and its subclasses: Food, Gold, and Water.
    These classes represent different types of items that can be found in the game.
"""
class Item:
    """
    Base class for every collectible item in the game.
    """

    def __init__(self, name: str, bonus: int, repeatBonus: bool = False):
        """
        Create a new item.
        """
        self.name = name
        self.bonus = bonus
        self.repeatBonus = repeatBonus

    def displayItem(self):
        """
        Build a readable summary of the item.
        """
        return f"Name: {self.name}\nBonus: {self.bonus}"


class Food(Item):
    """
    A food item that restores the player's food supply.
    """

    def __init__(self, name: str, cost : int, bonus: int, repeatBonus: bool = False):
        """
        Create a new food item.
        """
        super().__init__(name, bonus, repeatBonus)
        self.cost = cost

    def displayItem(self):
        """
        Build a readable summary of the food item.
        """
        return f"Name: {self.name}\nBonus: {self.bonus}\nCost: {self.cost}"


class Gold(Item):
    """
    A gold item that adds to the player's wealth.

    Gold is never a repeat bonus, so it disappears from the terrain once collected.
    """

    def __init__(self, name: str, bonus: int):
        """
        Create a new gold item.
        """
        # Gold can only be collected once, so repeatBonus is always False
        super().__init__(name, bonus, False)

class Water(Item):
    """
    A water item that restores the player's water supply.
    """

    def __init__(self, name: str, cost : int, bonus: int, repeatBonus: bool = False):
        """
        Create a new water item.
        """
        super().__init__(name, bonus, repeatBonus)
        self.cost = cost

    def displayItem(self):
        """
        Build a readable summary of the water item.
        """
        return f"Name: {self.name}\nBonus: {self.bonus}\nCost: {self.cost}"

