class Player:
    def __init__(self, name: str):
        self.name = name
        self.inventory = []
        self.health = 100
        self.hunger = 0
        self.thirst = 0