"""
    This file contains the Item class and its subclasses: Food, Gold, and Water. 
    These classes represent different types of items that can be found in the game.
"""
class Item:
    def __init__(self, name: str, bonus: int, repeatBonus: bool = False):
        self.name = name
        self.bonus = bonus
        self.repeatBonus = repeatBonus
    
    def displayItem(self):
        return f"Name: {self.name}\nBonus: {self.bonus}"


class Food(Item):
    def __init__(self, name: str, cost : int, bonus: int, repeatBonus: bool = False):
        super().__init__(name, bonus, repeatBonus)
        self.cost = cost

    def displayItem(self):
        return f"Name: {self.name}\nBonus: {self.bonus}\nCost: {self.cost}"


class Gold(Item):
    def __init__(self, name: str, bonus: int):
        super().__init__(name, bonus, False)

class Water(Item):
    def __init__(self, name: str, cost : int, bonus: int, repeatBonus: bool = False):
        super().__init__(name, bonus, repeatBonus)
        self.cost = cost

    def displayItem(self):
        return f"Name: {self.name}\nBonus: {self.bonus}\nCost: {self.cost}"
    