from brain import Brain
from vision import Vision
from item import Item, Food, Water, Gold

class Player:
    def __init__(self, max_strength: int, max_water: int, max_food: int, brain: Brain, vision_scope: Vision):

        # using double underscore naming convention to show the variable is private
        self.__max_strength = max_strength
        self.__max_water = max_water
        self.__max_food = max_food

        self.__curr_strength = max_strength
        self.__curr_water = max_water
        self.__curr_food = max_food
        self.__curr_gold = 0

        self.__move_pts = 0
        self.__brain = brain
        self.__vision_scope = vision_scope

        self.__inventory: list[Item] = []

        self.curr_x = 0
        self.curr_y = 0

    # Read only access to max attributes
    @property
    def max_strength(self):
        return self.__max_strength

    @property
    def max_water(self):
        return self.__max_water

    @property
    def max_food(self):
        return self.__max_food

    # Read only access to private attributes
    @property
    def curr_strength(self):
        return self.__curr_strength

    @property
    def curr_water(self):
        return self.__curr_water

    @property
    def curr_food(self):
        return self.__curr_food

    @property
    def curr_gold(self):
        return self.__curr_gold

    @property
    def move_pts(self):
        return self.__move_pts

    @property
    def brain(self):
        return self.__brain

    @property
    def vision_scope(self):
        return self.__vision_scope

    @property
    def inventory(self):
        return list(self.__inventory)  # copy so callers can't edit it directly

    # setters for private attributes that can change with values checked against min and max
    @curr_strength.setter
    def curr_strength(self, value: int):
        self.__curr_strength = max(0, min(value, self.__max_strength))

    @curr_water.setter
    def curr_water(self, value: int):
        self.__curr_water = max(0, min(value, self.__max_water))

    @curr_food.setter
    def curr_food(self, value: int):
        self.__curr_food = max(0, min(value, self.__max_food))

    @curr_gold.setter
    def curr_gold(self, value: int):
        self.__curr_gold = max(0, value)

    # change methods
    def change_curr_strength(self, amount : int):
        self.curr_strength += amount

    def change_curr_water(self, amount : int):
        self.curr_water += amount

    def change_curr_food(self, amount : int):
        self.curr_food += amount

    def change_curr_gold(self, amount : int):
        self.curr_gold += amount

    def change_move_pts(self, amount : int):
        self.__move_pts += amount

    def set_max_stats(self):
        self.__curr_strength = self.__max_strength
        self.__curr_water = self.__max_water
        self.__curr_food = self.__max_food

    # changes player's position to new x, y and updates their vision scope
    def update_position(self, x: int, y: int):
        self.curr_x = x
        self.curr_y = y
        if self.__vision_scope is not None:
            self.__vision_scope.update_vision(x, y)

    # spawn method - places player on west edge of the map
    def spawn_player(self, start_y: int):
        self.update_position(0, start_y)
        self.set_max_stats()
        self.__curr_gold = 0

    # class methods

    def collect_item(self, item: Item):
        self.__inventory.append(item)

    def initiate_trade(self, item: Item):
        return None
    
    def accept_trade(self):
        return None

    def reject_trade(self):
        return None

    def get_curr_location(self):
        return None


    

            