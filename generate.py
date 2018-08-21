import random
from helpers import Leaf
from colors import RGBCOLORS
from PIL import Image
import numpy


class BSPTree:
    def __init__(self):
        self.level = []
        self.room = None
        self._leafs = []
        self.MAX_LEAF_SIZE = 32
        self.ROOM_MAX_SIZE = 20
        self.ROOM_MIN_SIZE = 6

    def generateLevel(self, map_width, map_height):
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

        rootLeaf.createRooms(self)

        return self.level

    def createRoom(self, room):
        # set all tiles within a rectangle to 0
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.level[x][y] = " "

    def createHall(self, room1, room2):
        # connect two rooms by hallways
        if random.randint(0, 1) == 1:
            x1, y1 = room1.get_wall()
        else:
            x1, y1 = room1.center()

        if random.randint(0, 1) == 1:
            x2, y2 = room2.center()
        else:
            x2, y2 = room2.get_wall()
        # coords = room1.get_wall("west")
        # 50% chance that a tunnel will start horizontally
        if random.randint(0, 1) == 1:
        # if coord1 == "horr":
            self.createHorTunnel(x1, x2, y1)
            self.createVirTunnel(y1, y2, x2)

        else:  # else it starts virtically
            self.createVirTunnel(y1, y2, x1)
            self.createHorTunnel(x1, x2, y2)

    def createHorTunnel(self, x1, x2, y):
        _x1, _x2, _y = int(x1), int(x2), int(y)
        for x in range(min(_x1, _x2), max(_x1, _x2) + 1):
            if self.level[x][_y] is not " ":
                self.level[x][_y] = "c"
            # self.level[x][_y] = "c"

    def createVirTunnel(self, y1, y2, x):
        _y1, _y2, _x = int(y1), int(y2), int(x)
        for y in range(min(_y1, _y2), max(_y1, _y2) + 1):
            if self.level[_x][y] is not " ":
                self.level[_x][y] = "c"
            # self.level[_x][y] = "c"


newtree = []
tree = BSPTree().generateLevel(64, 128)
for leaf in tree:
    newtree.append([str(i) for i in leaf])

img_map = []
for leaf in tree:
    img_leaf = []
    for item in leaf:
        if item == "#":
            img_leaf.append(RGBCOLORS.wall)
        elif item == "c":
            img_leaf.append(RGBCOLORS.corridor)
        else:
            img_leaf.append(RGBCOLORS.floor)
    img_map.append(img_leaf)

# for leaf in img_map:
#     print(leaf)
# with open("map.txt", "w+") as f:
#     for leaf in newtree:
#         for item in leaf:
#             f.write(item)
#         f.write("\n")

array = numpy.array(img_map, dtype=numpy.uint8)
img = Image.fromarray(array)
img.save('map.png')
