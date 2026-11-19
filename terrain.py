"""
This file contains the Terrain class and its subclasses: Plains, Forest, Swamp,
Mountain, and Desert. These classes represent the different types of terrain
that make up the squares of the game map.
"""
from item import Item, Food, Gold, Water
from trader import Trader
import random

class Terrain:
    """
    Base class for a single tile of terrain on the game map.

    Each terrain stores how much water, food, and movement it costs to enter,
    holds a list of collectible resources, and has its own trader. The
    GameMap uses these costs to charge the player; the terrain itself only
    stores them and prints descriptions.
    """

    def __init__(self, name : str, water_cost : int, movement_cost : int, food_cost : int):
        """
        Create a new terrain tile with no resources.

        Args:
            name: The terrain's name, such as "plains".
            water_cost: Water the player spends to enter this terrain.
            movement_cost: Movement points the player spends to enter.
            food_cost: Food the player spends to enter this terrain.
        """
        self._name = name
        self._water_cost = water_cost
        self._movement_cost = movement_cost
        self._food_cost = food_cost
        self._trader = Trader()
        self._resources = []  # Filled in by each subclass

    @property
    def name(self) -> str:
        """The terrain's name, such as "plains"."""
        return self._name

    @property
    def water_cost(self) -> int:
        """Water the player spends to enter this terrain."""
        return self._water_cost

    @property
    def movement_cost(self) -> int:
        """Movement points the player spends to enter this terrain."""
        return self._movement_cost

    @property
    def food_cost(self) -> int:
        """Food the player spends to enter this terrain."""
        return self._food_cost

    @property
    def trader(self) -> Trader:
        """The trader located in this terrain."""
        return self._trader

    @property
    def resources(self) -> list[Item]:
        """The items currently available to collect in this terrain."""
        return self._resources
    
    def display_resources(self):
        """Print the names of all resources the player can collect here."""
        if len(self._resources) == 0:
            print("No resources available in this terrain.")
        else:
            print(f"These are the items you can collect:")
            for resource in self._resources:
                print(f"- {resource.name} ")

    def get_item(self, index: int) -> Item:
        """
        Get a resource from this terrain by its position in the list.

        Args:
            index: The position of the item in the resources list.

        Returns:
            The item at that position. The item stays in the terrain.
        """
        return self._resources[index]

    def take_all_items(self) -> list[Item]:
        """
        Remove and return every resource in this terrain.

        Items marked as a repeat bonus stay in the terrain so they can be
        collected again; all other items are removed. The GameMap gives the
        returned items to the player.

        Returns:
            A list of every item that was in the terrain.
        """
        taken = list(self._resources)
        self._resources = [item for item in self._resources if item.repeat_bonus]
        return taken

    def terrain_entered(self):
        """
        Print a message that the player entered this terrain and its costs.

        Subclasses extend this to describe the terrain and its resources.
        The GameMap is responsible for charging the costs.
        """
        print(f"You have entered the {self._name}.")
        print(f"Water Cost: {self._water_cost}, Food Cost: {self._food_cost}, Movement Cost: {self._movement_cost}")

    def stayed_in_terrain(self):
        """
        Print a message that the player is resting here, then list the
        resources still available.

        Resting costs half the normal water and food cost (rounded down) and
        gives back 2 movement points. The GameMap is responsible for
        charging these costs.
        """
        print(f"You have decided to stay in the {self._name} to rest before travelling further.")
        print(f"Water Cost: {self._water_cost // 2}, Food Cost: {self._food_cost // 2}, Movement Cost: +2")
        self.display_resources()

class Plains(Terrain):
    """
    Open grassland with the lowest entry costs.

    Possible resources: River Water, Gold Nugget, and Rabbit.
    """

    # Resources that can appear in the plains
    _terrain_items = [
        Water("River Water", 2, 3, True),
        Gold("Gold Nugget", 1),
        Food("Rabbit", 3, 4, True)
    ]

    def __init__(self):
        """Create a plains tile; each resource has a 50% chance to appear."""
        super().__init__("plains", 1, 1, 1)
        # Randomly decide which resources spawn in this tile
        for item in self._terrain_items:
            if random.randint(0, 1) == 0:
                self._resources.append(item)
    
    def terrain_entered(self):
        """
        Print the entry message, then describe the plains and the resources found here.
        """
        super().terrain_entered()
        print("The plains are vast and open, with a gentle breeze blowing across the fields.")
        # Describe each resource that is present
        for item in self._resources:
            if isinstance(item, Water):
                print("You hear the sound of a river nearby, and you realize that there may be some fresh water available.")
            if isinstance(item, Gold):
                print("You notice a small glint of gold in the soil!")
            if isinstance(item, Food):
                print("You spot a colony of small rabbits nibbling on some grass.")
        self.display_resources()



class Forest(Terrain):
    """
    Dense woodland with moderate food and movement costs.

    Possible resources: Forest Stream, Gold Nugget, and Mushrooms.
    """

    # Resources that can appear in the forest
    _terrain_items = [
        Water("Forest Stream", 2, 2, True),
        Gold("Gold Nugget", 2),
        Food("Mushrooms", 2, 3)
    ]

    def __init__(self):
        """Create a forest tile; each resource has a 50% chance to appear."""
        super().__init__("forest", 1, 2, 2)
        # Randomly decide which resources spawn in this tile
        for item in self._terrain_items:
            if random.randint(0, 1) == 0:
                self._resources.append(item)

    def terrain_entered(self):
        """
        Print the entry message, then describe the forest and the resources found here.
        """
        super().terrain_entered()
        print("The forest is dense and full of life, with the sound of birds and rustling leaves all around you.")
        # Describe each resource that is present
        for item in self._resources:
            if isinstance(item, Water):
                print("You spot a small stream running through the forest.")
            if isinstance(item, Gold):
                print("You found a buried treasure chest with gold nuggets inside!")
            if isinstance(item, Food):
                print("You spot some mushrooms growing on the forest floor.")
        self.display_resources()

class Swamp(Terrain):
    """
    Murky wetland with high food and movement costs.

    Possible resources: Swamp Water, Gold Nugget, and Cranberries.
    """

    # Resources that can appear in the swamp
    _terrain_items = [
        Water("Swamp Water", 3, 5, True),
        Gold("Gold Nugget", 3),
        Food("Cranberries", 1, 4)
    ]

    def __init__(self):
        """Create a swamp tile; each resource has a 50% chance to appear."""
        super().__init__("swamp", 1, 3, 3)
        # Randomly decide which resources spawn in this tile
        for item in self._terrain_items:
            if random.randint(0, 1) == 0:
                self._resources.append(item)
        
    def terrain_entered(self):
        """
        Print the entry message, then describe the swamp and the resources found here.
        """
        super().terrain_entered()
        print("The swamp is murky and humid, with the sound of insects and the smell of decay all around you.")
        # Describe each resource that is present
        for item in self._resources:
            if isinstance(item, Water):
                print("You see a large pond in the distance.")
            if isinstance(item, Gold):
                print("You find an abandoned hut with a small stash of gold inside the cabinets.")
            if isinstance(item, Food):
                print("You spot some cranberries growing on a bush. You inspect them and they are safe to eat.")
        self.display_resources()

class Mountain(Terrain):
    """
    Steep, rocky terrain with the highest entry costs and the most gold.

    Possible resources: Melted Snow, Gold Nugget, and Goat.
    """

    # Resources that can appear in the mountains
    _terrain_items = [
        Water("Melted Snow", 1, 1, True),
        Gold("Gold Nugget", 10),
        Food("Goat", 4, 6, True)
    ]
  
    def __init__(self):
        """Create a mountain tile; each resource has a 50% chance to appear."""
        super().__init__("mountain", 3, 4, 3)
        # Randomly decide which resources spawn in this tile
        for item in self._terrain_items:
            if random.randint(0, 1) == 0:
                self._resources.append(item)

    def terrain_entered(self):
        """
        Print the entry message, then describe the mountain and the resources found here.
        """
        super().terrain_entered()
        print("The mountain is steep and treacherous, with the sound of wind whistling through the peaks.")
        # Describe each resource that is present
        for item in self._resources:
            if isinstance(item, Water):
                print("You spot a patch of melted snow in the distance.")
            if isinstance(item, Gold):
                print("You find a mineshaft and at the entrance gold nuggets scattered on the ground.")
            if isinstance(item, Food):
                print("You spot a herd of goats grazing on the mountainside.")
        self.display_resources()

class Desert(Terrain):
    """
    Hot, dry terrain with a high water cost.

    Possible resources: Desert Spring, Gold Nugget, and Cacti.
    """

    # Resources that can appear in the desert
    _terrain_items = [
        Water("Desert Spring", 3, 3, True),
        Gold("Gold Nugget", 5),
        Food("Cacti", 2, 3, True)
    ]

    def __init__(self):
        """Create a desert tile; each resource has a 50% chance to appear."""
        super().__init__("desert", 3, 2, 2)
        # Randomly decide which resources spawn in this tile
        for item in self._terrain_items:
            if random.randint(0, 1) == 0:
                self._resources.append(item)
        
    def terrain_entered(self):
        """
        Print the entry message, then describe the desert and the resources found here.
        """
        super().terrain_entered()
        print("The desert is hot and dry, with the sound of sand blowing in the wind.")
        # Describe each resource that is present
        for item in self._resources:
            if isinstance(item, Water):
                print("You found an oasis in the desert with a spring that could provide you with hydration.")
            if isinstance(item, Gold):
                print("You discover a chunks of gold through the sand as you shuffled your feet.")
            if isinstance(item, Food):
                print("You spot cacti growing as far as you can see in the horizon.")
        self.display_resources()
