class Item:
    def __init__(self, name: str, bonus: int, repeatBonus: bool = False):
        self.name = name
        self.bonus = bonus
        self.repeatBonus = repeatBonus

    def getBonus(self):
        return self.bonus

    def getName(self):
        return self.name

    def repeatBonus(self):
        return self.repeatBonus
    
    def displayItem(self):
        return f"Name: {self.name}\nBonus: {self.bonus}"


class Food(Item):
    def __init__(self, name: str, cost : int, bonus: int, repeatBonus: bool = False):
        super().__init__(name, bonus, repeatBonus)
        self.cost = cost

    def getCost(self):
        return self.cost

    def displayItem(self):
        return f"Name: {self.name}\nBonus: {self.bonus}\nCost: {self.cost}"


class Gold(Item):
    def __init__(self, name: str, bonus: int):
        super().__init__(name, bonus, False)

class Water(Item):
    def __init__(self, name: str, cost : int, bonus: int, repeatBonus: bool = False):
        super().__init__(name, bonus, repeatBonus)
        self.cost = cost

    def getCost(self):
        return self.cost

    def displayItem(self):
        return f"Name: {self.name}\nBonus: {self.bonus}\nCost: {self.cost}"
    