import random
from helpers import Leaf, Rect, RoomList
from renderer import MapRenderer
from typing import List, Any


class BSPTree:
    def __init__(self):
        self.level: List = []
        self.room: object = None
        self._leafs: List = []
        self.MAX_LEAF_SIZE: int = 32
        self.ROOM_MAX_SIZE: int = 20
        self.ROOM_MIN_SIZE: int = 6

    def generateLevel(self, map_width: int, map_height: int, room_list: RoomList):
        # Creates an empty 2D array or clears existing array
        self.level = [["#"
                       for y in range(map_height)]
                      for x in range(map_width)]

        rootLeaf = Leaf(0, 0, map_width, map_height)
        self._leafs.append(rootLeaf)

        split_successfully = True
        # loop through all leaves until they can no longer split successfully
        while split_successfully:
            split_successfully = False
            for l in self._leafs:
                if (l.child_1 is None) and (l.child_2 is None):
                    if (l.width > self.MAX_LEAF_SIZE or
                            (l.height > self.MAX_LEAF_SIZE) or
                            (random.random() > 0.7)):
                        if l.split_leaf():  # try to split the leaf
                            self._leafs.append(l.child_1)
                            self._leafs.append(l.child_2)
                            split_successfully = True

        rootLeaf.createRooms(self, room_list)

        return self.level

    def createRoom(self, room: Rect):
        # set all tiles within a rectangle to 0
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.level[x][y] = " "

    def createHall(self, room1: Rect, room2: Rect):
        # connect two rooms by hallways
        x1, y1 = room1.get_wall()
        x2, y2 = room2.get_wall()

        # 50% chance that a tunnel will start horizontally
        if random.randint(0, 1) == 1:
            self.createHorTunnel(x1, x2, y1)
            self.createVirTunnel(y1, y2, x2)

        else:  # else it starts virtically
            self.createVirTunnel(y1, y2, x1)
            self.createHorTunnel(x1, x2, y2)

    def createHorTunnel(self, x1: int, x2: int, y: int):
        _x1, _x2, _y = int(x1), int(x2), int(y)
        for x in range(min(_x1, _x2), max(_x1, _x2) + 1):
            if self.level[x][_y] is not " ":
                self.level[x][_y] = "c"
            # self.level[x][_y] = "c"

    def createVirTunnel(self, y1: int, y2: int, x: int):
        _y1, _y2, _x = int(y1), int(y2), int(x)
        for y in range(min(_y1, _y2), max(_y1, _y2) + 1):
            if self.level[_x][y] is not " ":
                self.level[_x][y] = "c"
            # self.level[_x][y] = "c"


room_list = RoomList()
tree = BSPTree().generateLevel(64, 128, room_list)

MapRenderer(tree).render_map()
print(room_list.get_rooms()[5].get_random_point_in_room())

