from Brain import Brain
from Vision import Vision

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

        self.__inventory = []

        self.curr_x = 0
        self.curr_y = 0

    # player setup

    def spawn_player(self, game_map):
        # place the player in the middle of the left edge of the map
        self.curr_x = 0
        self.curr_y = game_map.height // 2

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
    def vision_scope(self):
        return self.__vision_scope

    @property
    def inventory(self):
        return list(self.__inventory)  # copy so callers can't edit it directly
    