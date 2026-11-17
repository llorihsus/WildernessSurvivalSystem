"""
    This file contains the Terrain class and its subclasses: Plains, Forest, Swamp,
    Mountain, and Desert. These classes represent different types of terrain that can
    be found in the game.
"""
from item import Item, Food, Gold, Water
from trader import Trader
from player import Player
import random

class Terrain:
    """
    Base class for a single tile of terrain on the game map.

    Each terrain charges the player water, food, and movement points to enter,
    holds a list of collectible resources, and has its own trader.
    """

    def __init__(self, name : str, waterCost : int, movementCost : int, foodCost : int):
        """
        Create a new terrain tile with no resources.
        """
        self.name = name
        self.waterCost = waterCost
        self.movementCost = movementCost
        self.foodCost = foodCost
        self.trader = Trader()
        self.resources = []  # Filled in by each subclass

    def hasSufficientCostToEnter(self, player: Player) -> bool:
        """
        Check whether the player has enough supplies to enter this terrain.
        """
        if player.currWater < self.waterCost:
            return False
        if player.currFood < self.foodCost:
            return False
        if player.movePts < self.movementCost:
            return False

        return True

    def hasSufficientCostToStay(self, player: Player) -> bool:
        """
        Check whether the player has enough supplies to rest in this terrain.

        Staying costs half the normal water and food cost and no movement points.
        """
        if player.currWater < self.waterCost * 1/2:
            return False
        if player.currFood < self.foodCost * 1/2:
            return False

        return True

    def displayResources(self):
        """Print the names of all resources the player can collect here."""
        if len(self.resources) == 0:
            print("No resources available in this terrain.")
        else:
            print(f"These are the items you can collect:")
            for resource in self.resources:
                print(f"- {resource.name} ")

    def getItem(self, index: int) -> Item:
        """
        Get a resource from this terrain by its position in the list.
        """
        return self.resources[index]

    def getTrader(self) -> Trader:
        """
        Get the trader located in this terrain.
        """
        return self.trader

    def collectAllItems(self, player: Player):
        """
        Add every resource in this terrain to the player's inventory.

        Items marked as a repeat bonus stay in the terrain so they can be
        collected again; all other items are removed.
        """
        newResources = []
        for i in range(len(self.resources)):
            player.inventory.append(self.resources[i])
            # Keep repeatable items in the terrain for later collection
            if self.resources[i].repeatBonus:
                newResources.append(self.resources[i])
        self.resources = newResources
        return None

    def terrainEntered(self, player: Player):
        """
        Charge the player the full cost of entering this terrain.
        """
        print(f"You have entered the {self.name}.")
        print(f"Water Cost: {self.waterCost}, Food Cost: {self.foodCost}, Movement Cost: {self.movementCost}")
        # Deduct the entry costs from the player's supplies
        player.currWater -= self.waterCost
        player.currFood -= self.foodCost
        player.movePts -= self.movementCost
        return None

    def stayedInTerrain(self, player: Player):
        """
        Let the player rest in this terrain for a turn.

        Resting costs half the normal water and food cost, restores 2
        movement points, and shows the resources still available.
        """
        print(f"You have decided to stay in the {self.name} to rest before travelling further.")
        print(f"Water Cost: {self.waterCost * 1/2}, Food Cost: {self.foodCost * 1/2}, Movement Cost: +2")
        # Resting costs half of the supplies (rounded down) and recovers movement
        player.currWater -= int(self.waterCost * 1/2)
        player.currFood -= int(self.foodCost * 1/2)
        player.movePts += 2
        self.displayResources()
        return None

class Plains(Terrain):
    """
    Open grassland with the lowest entry costs.

    Possible resources: River Water, Gold Nugget, and Rabbit.
    """

    # Resources that can appear in the plains
    riverWater = Water("River Water", 2, 3, True)
    goldNugget = Gold("Gold Nugget", 1)
    rabbit = Food("Rabbit", 3, 4, True)

    def __init__(self):
        """Create a plains tile; each resource has a 50% chance to appear."""
        super().__init__("plains", 1, 1, 1)
        # Randomly decide which resources spawn in this tile
        if random.randint(0, 1) == 0:
            self.resources.append(self.riverWater)
        if random.randint(0, 1) == 0:
            self.resources.append(self.goldNugget)
        if random.randint(0, 1) == 0:
            self.resources.append(self.rabbit)

    def terrainEntered(self, player: Player):
        """
        Charge the entry cost, then describe the plains and its resources.
        """
        super().terrainEntered(player)
        print("The plains are vast and open, with a gentle breeze blowing across the fields.")
        # Describe each resource that is present
        if self.riverWater in self.resources:
            print("You hear the sound of a river nearby, and you realize that there may be some fresh water available.")
        if self.goldNugget in self.resources:
            print("You notice a small glint of gold in the soil!")
        if self.rabbit in self.resources:
            print("You spot a colony of small rabbits nibbling on some grass.")
        self.displayResources()



class Forest(Terrain):
    """
    Dense woodland with moderate food and movement costs.

    Possible resources: Forest Stream, Gold Nugget, and Mushrooms.
    """

    # Resources that can appear in the forest
    forestStream = Water("Forest Stream", 2, 2, True)
    goldNugget = Gold("Gold Nugget", 2)
    mushrooms = Food("Mushrooms", 2, 3)

    def __init__(self):
        """Create a forest tile; each resource has a 50% chance to appear."""
        super().__init__("forest", 1, 2, 2)
        # Randomly decide which resources spawn in this tile
        if random.randint(0, 1) == 0:
            self.resources.append(self.forestStream)
        if random.randint(0, 1) == 0:
            self.resources.append(self.goldNugget)
        if random.randint(0, 1) == 0:
            self.resources.append(self.mushrooms)

    def terrainEntered(self, player: Player):
        """
        Charge the entry cost, then describe the forest and its resources.
        """
        super().terrainEntered(player)
        print("The forest is dense and full of life, with the sound of birds and rustling leaves all around you.")
        # Describe each resource that is present
        if self.forestStream in self.resources:
            print("You spot a small stream running through the forest.")
        if self.goldNugget in self.resources:
            print("You found a buried treasure chest with gold nuggets inside!")
        if self.mushrooms in self.resources:
            print("You spot some mushrooms growing on the forest floor.")
        self.displayResources()

class Swamp(Terrain):
    """
    Murky wetland with high food and movement costs.

    Possible resources: Swamp Water, Gold Nugget, and Cranberries.
    """

    # Resources that can appear in the swamp
    swampWater = Water("Swamp Water", 3, 5, True)
    goldNugget = Gold("Gold Nugget", 3)
    cranberries = Food("Cranberries", 1, 4)

    def __init__(self):
        """Create a swamp tile; each resource has a 50% chance to appear."""
        super().__init__("swamp", 1, 3, 3)
        # Randomly decide which resources spawn in this tile
        if random.randint(0, 1) == 0:
            self.resources.append(self.swampWater)
        if random.randint(0, 1) == 0:
            self.resources.append(self.goldNugget)
        if random.randint(0, 1) == 0:
            self.resources.append(self.cranberries)

    def terrainEntered(self, player: Player):
        """
        Charge the entry cost, then describe the swamp and its resources.
        """
        super().terrainEntered(player)
        print("The swamp is murky and humid, with the sound of insects and the smell of decay all around you.")
        # Describe each resource that is present
        if self.swampWater in self.resources:
            print("You see a large pond in the distance.")
        if self.goldNugget in self.resources:
            print("You find an abandoned hut with a small stash of gold inside the cabinets.")
        if self.cranberries in self.resources:
            print("You spot some cranberries growing on a bush. You inspect them and they are safe to eat.")
        self.displayResources()

class Mountain(Terrain):
    """
    Steep, rocky terrain with the highest entry costs and the most gold.

    Possible resources: Melted Snow, Gold Nugget, and Goat.
    """

    # Resources that can appear in the mountains
    meltedSnow = Water("Melted Snow", 1, 1, True)
    goldNugget = Gold("Gold Nugget", 10)
    goat = Food("Goat", 4, 6, True)

    def __init__(self):
        """Create a mountain tile; each resource has a 50% chance to appear."""
        super().__init__("mountain", 3, 4, 3)
        # Randomly decide which resources spawn in this tile
        if random.randint(0, 1) == 0:
            self.resources.append(self.meltedSnow)
        if random.randint(0, 1) == 0:
            self.resources.append(self.goldNugget)
        if random.randint(0, 1) == 0:
            self.resources.append(self.goat)

    def terrainEntered(self, player: Player):
        """
        Charge the entry cost, then describe the mountain and its resources.
        """
        super().terrainEntered(player)
        print("The mountain is steep and treacherous, with the sound of wind whistling through the peaks.")
        # Describe each resource that is present
        if self.meltedSnow in self.resources:
            print("You spot a patch of melted snow in the distance.")
        if self.goldNugget in self.resources:
            print("You find a mineshaft and at the entrance gold nuggets scattered on the ground.")
        if self.goat in self.resources:
            print("You spot a herd of goats grazing on the mountainside.")
        self.displayResources()

class Desert(Terrain):
    """
    Hot, dry terrain with a high water cost.

    Possible resources: Desert Spring, Gold Nugget, and Cacti.
    """

    # Resources that can appear in the desert
    desertSpring = Water("Desert Spring", 3, 3, True)
    goldNugget = Gold("Gold Nugget", 5)
    cacti = Food("Cacti", 2, 3, True)

    def __init__(self):
        """Create a desert tile; each resource has a 50% chance to appear."""
        super().__init__("desert", 3, 2, 2)
        # Randomly decide which resources spawn in this tile
        if random.randint(0, 1) == 0:
            self.resources.append(self.desertSpring)
        if random.randint(0, 1) == 0:
            self.resources.append(self.goldNugget)
        if random.randint(0, 1) == 0:
            self.resources.append(self.cacti)

    def terrainEntered(self, player: Player):
        """
        Charge the entry cost, then describe the desert and its resources.
        """
        super().terrainEntered(player)
        print("The desert is hot and dry, with the sound of sand blowing in the wind.")
        # Describe each resource that is present
        if self.desertSpring in self.resources:
            print("You found an oasis in the desert with a spring that could provide you with hydration.")
        if self.goldNugget in self.resources:
            print("You discover a chunks of gold through the sand as you shuffled your feet.")
        if self.cacti in self.resources:
            print("You spot cacti growing as far as you can see in the horizon.")
        self.displayResources()
