import numpy as np
from PIL import Image
from typing import List, Tuple


class MapRenderer:
    floor: Tuple = (220, 220, 220)
    wall: Tuple = (47, 79, 79)
    corridor: Tuple = (119, 136, 153)

    def __init__(self, maptree: List):
        self.img_map: List = []
        for leaf in maptree:
            img_leaf = []
            for item in leaf:
                if item == "#":
                    img_leaf.append(self.wall)
                elif item == "c":
                    img_leaf.append(self.corridor)
                else:
                    img_leaf.append(self.floor)
            self.img_map.append(img_leaf)

    def render_map(self):
        array = np.array(self.img_map, dtype=np.uint8)
        img = Image.fromarray(array)
        img.save('map.png')

    def save_as_text(self):
        newtree: List = []
        for leaf in self.img_map:
            newtree.append([str(i) for i in leaf])
        with open("map.txt", "w+") as f:
            for leaf in newtree:
                for item in leaf:
                    f.write(item)
                f.write("\n")
