from item import Item, Food, Gold, Water
from trader import Trader
import random
from player import Player

class Terrain:
    def __init__(self, name : str, waterCost : int, movementCost : int, foodCost : int):
        self.name = name
        self.waterCost = waterCost
        self.movementCost = movementCost
        self.foodCost = foodCost
        self.trader = Trader()
        self.resources = []

    def hasSufficientCostToEnter(self, player: Player) -> bool:
        if player.currWater < self.waterCost:
            return False
        if player.currFood < self.foodCost:
            return False
        if player.movePts < self.movementCost:
            return False

        return True

    def hasSufficientCostToStay(self, player: Player) -> bool:
        if player.currWater < self.waterCost * 1/2:
            return False
        if player.currFood < self.foodCost * 1/2:
            return False
        
        return True

    def displayResources(self):
        if len(self.resources) == 0:
            print("No resources available in this terrain.")
        else:
            print(f"These are the items you can collect:")
            for resource in self.resources:
                print(f"- {resource.name} ")

    def getItem(self, index: int) -> Item:
       return self.resources[index]

    def getTrader(self) -> Trader:
            return self.trader
    
    def collectAllItems(self, player: Player):
        newResources = []
        for i in range(len(self.resources)):
            player.inventory.append(self.resources[i])
            if self.resources[i].repeatBonus:
                newResources.append(self.resources[i])
        self.resources = newResources
        return None

    def terrainEntered(self, player: Player):
        print(f"You have entered the {self.name}.")
        print(f"Water Cost: {self.waterCost}, Food Cost: {self.foodCost}, Movement Cost: {self.movementCost}")
        player.currWater -= self.waterCost
        player.currFood -= self.foodCost    
        player.movePts -= self.movementCost
        return None

    def stayedInTerrain(self, player: Player):
        print(f"You have decided to stay in the {self.name} to rest before travelling further.")
        print(f"Water Cost: {self.waterCost * 1/2}, Food Cost: {self.foodCost * 1/2}, Movement Cost: +2")
        player.currWater -= int(self.waterCost * 1/2)
        player.currFood -= int(self.foodCost * 1/2)
        player.movePts += 2
        self.displayResources()
        return None

class Plains(Terrain):
    riverWater = Water("River Water", 2, 3, True)
    goldNugget = Gold("Gold Nugget", 1)
    rabbit = Food("Rabbit", 3, 4, True)

    def __init__(self):
        super().__init__("Plains", 1, 1, 1)
        if random.randint(0, 1) == 0:
            self.resources.append(self.riverWater)
        if random.randint(0, 1) == 0:
            self.resources.append(self.goldNugget)
        if random.randint(0, 1) == 0:
            self.resources.append(self.rabbit)

    def terrainEntered(self, player: Player):
        super().terrainEntered(player)
        print("The plains are vast and open, with a gentle breeze blowing across the fields.")
        if self.riverWater in self.resources:
            print("You hear the sound of a river nearby, and you realize that there may be some fresh water available.")
        if self.goldNugget in self.resources:
            print("You notice a small glint of gold in the soil!")
        if self.rabbit in self.resources:
            print("You spot a colony of small rabbits nibbling on some grass.")
        self.displayResources()



class Forest(Terrain):
    forestStream = Water("Forest Stream", 2, 2, True)
    goldNugget = Gold("Gold Nugget", 2)
    mushrooms = Food("Mushrooms", 2, 3)
    
    def __init__(self):
        super().__init__("Forest", 1, 2, 2)
        if random.randint(0, 1) == 0:
            self.resources.append(self.forestStream)
        if random.randint(0, 1) == 0:
            self.resources.append(self.goldNugget)
        if random.randint(0, 1) == 0:
            self.resources.append(self.mushrooms)

    def terrainEntered(self, player: Player):
        super().terrainEntered(player)
        print("The forest is dense and full of life, with the sound of birds and rustling leaves all around you.")
        if self.forestStream in self.resources:
            print("You spot a small stream running through the forest.")
        if self.goldNugget in self.resources:
            print("You found a buried treasure chest with gold nuggets inside!")
        if self.mushrooms in self.resources:
            print("You spot some mushrooms growing on the forest floor.")
        self.displayResources()

class Swamp(Terrain):
    swampWater = Water("Swamp Water", 3, 5, True)
    goldNugget = Gold("Gold Nugget", 3)
    cranberries = Food("Cranberries", 1, 4)

    def __init__(self):
        super().__init__("Swamp", 1, 3, 3)
        if random.randint(0, 1) == 0:
            self.resources.append(self.swampWater)
        if random.randint(0, 1) == 0:
            self.resources.append(self.goldNugget)
        if random.randint(0, 1) == 0:
            self.resources.append(self.cranberries)

    def terrainEntered(self, player: Player):
        super().terrainEntered(player)
        print("The swamp is murky and humid, with the sound of insects and the smell of decay all around you.")
        if self.swampWater in self.resources:
            print("You see a large pond in the distance.")
        if self.goldNugget in self.resources:
            print("You find an abandoned hut with a small stash of gold inside the cabinets.")
        if self.cranberries in self.resources:
            print("You spot some cranberries growing on a bush. You inspect them and they are safe to eat.")
        self.displayResources()

class Mountain(Terrain):
    meltedSnow = Water("Melted Snow", 1, 1, True)
    goldNugget = Gold("Gold Nugget", 10)
    goat = Food("Goat", 4, 6, True)

    def __init__(self):
        super().__init__("Mountain", 3, 4, 3)
        if random.randint(0, 1) == 0:
            self.resources.append(self.meltedSnow)
        if random.randint(0, 1) == 0:
            self.resources.append(self.goldNugget)
        if random.randint(0, 1) == 0:
            self.resources.append(self.goat)

    def terrainEntered(self, player: Player):
        super().terrainEntered(player)
        print("The mountain is steep and treacherous, with the sound of wind whistling through the peaks.")
        if self.meltedSnow in self.resources:
            print("You spot a patch of melted snow in the distance.")
        if self.goldNugget in self.resources:
            print("You find a mineshaft and at the entrance gold nuggets scattered on the ground.")
        if self.goat in self.resources:
            print("You spot a herd of goats grazing on the mountainside.")
        self.displayResources()

class Desert(Terrain): 
    desertSpring = Water("Desert Spring", 3, 3, True)
    goldNugget = Gold("Gold Nugget", 5)
    cacti = Food("Cacti", 2, 3, True)

    def __init__(self):
        super().__init__("Desert", 3, 2, 2)
        if random.randint(0, 1) == 0:
            self.resources.append(self.desertSpring)
        if random.randint(0, 1) == 0:
            self.resources.append(self.goldNugget)
        if random.randint(0, 1) == 0:
            self.resources.append(self.cacti)

    def terrainEntered(self, player: Player):
        super().terrainEntered(player)
        print("The desert is hot and dry, with the sound of sand blowing in the wind.")
        if self.desertSpring in self.resources:
            print("You found an oasis in the desert with a spring that could provide you with hydration.")
        if self.goldNugget in self.resources:
            print("You discover a chunks of gold through the sand as you shuffled your feet.")
        if self.cacti in self.resources:
            print("You spot cacti growing as far as you can see in the horizon.")
        self.displayResources()