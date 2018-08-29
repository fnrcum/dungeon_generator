import random
from typing import List, Tuple, Any, Optional


class RoomList:
    rooms: List = []

    def add_room(self, room):
        self.rooms.append(room)

    def get_rooms(self) -> List:
        return self.rooms


class Rect:
    """
    Class that represents a rectangular room
    :x coordinate
    :y coordinate
    :w width
    :h height
    """
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w - 1
        self.y2 = y + h - 1

    def __getitem__(self, k: int):
        def iteritem(k, kmin, kmax):
            if isinstance(k, int):
                yield kmin + k if k >= 0 else kmax + k
            elif isinstance(k, slice):
                for i in range(k.start or kmin, k.stop or kmax, k.step or 1):
                    yield i

        if isinstance(k, tuple) and len(k) == 2:
            result = []
            for i in iteritem(k[0], self.x1, self.x2):
                for j in iteritem(k[1], self.y1, self.y2):
                    result.append((i, j))
            return result

    def center(self) -> Tuple:
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y

    def get_wall(self) -> Tuple:
        chance = random.random()
        if chance < 0.25:
            wall = self[:, 0]
            wall = random.choice(wall)
            wall_x, wall_y = wall[0], wall[1]
        elif 0.25 < chance < 0.5:
            wall = self[:, -1]
            wall = random.choice(wall)
            wall_x, wall_y = wall[0], wall[1]
        elif 0.5 < chance < 0.75:
            wall = self[0, :]
            wall = random.choice(wall)
            wall_x, wall_y = wall[0], wall[1]
        else:
            wall = self[-1, :]
            wall = random.choice(wall)
            wall_x, wall_y = wall[0], wall[1]

        return wall_x, wall_y

    def get_all_points_inside_room(self) -> List:
        point_coordinates: List = []
        for i in range(self.y1 - 1):
            coords = self[i, :]
            coords.pop(0)
            coords.pop(len(coords) - 1)
            point_coordinates.append(coords)
        return point_coordinates

    def get_random_point_in_room(self) -> Tuple:
        point_coordinates = self.get_all_points_inside_room()
        print(point_coordinates)
        choice = random.choice(point_coordinates)
        print(choice)
        return random.choice(choice)

    def intersect(self, other) -> bool:
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


class Leaf:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.MIN_LEAF_SIZE: int = 9
        self.child_1: Leaf = None
        self.child_2: Leaf = None
        self.room: Rect = None
        self.hall = None

    def split_leaf(self):
        # begin splitting the leaf into two children
        if (self.child_1 is not None) or (self.child_2 is not None):
            return False  # This leaf has already been split

        '''
        ==== Determine the direction of the split ====
        If the width of the leaf is >25% larger than the height,
        split the leaf vertically.
        If the height of the leaf is >25 larger than the width,
        split the leaf horizontally.
        Otherwise, choose the direction at random.
        '''
        split_horizontally = random.choice([True, False])
        if self.width / self.height >= 1.25:
            split_horizontally = False
        elif self.height / self.width >= 1.25:
            split_horizontally = True

        if split_horizontally:
            max = self.height - self.MIN_LEAF_SIZE
        else:
            max = self.width - self.MIN_LEAF_SIZE

        if max <= self.MIN_LEAF_SIZE:
            return False  # the leaf is too small to split further

        split = random.randint(self.MIN_LEAF_SIZE, max)  # determine where to split the leaf

        if split_horizontally:
            self.child_1 = Leaf(self.x, self.y, self.width, split)
            self.child_2 = Leaf(self.x, self.y + split, self.width, self.height - split)
        else:
            self.child_1 = Leaf(self.x, self.y, split, self.height)
            self.child_2 = Leaf(self.x + split, self.y, self.width - split, self.height)

        return True

    def createRooms(self, bspTree, room_list: RoomList):
        if self.child_1 or self.child_2:
            # recursively search for children until you hit the end of the branch
            if self.child_1:
                self.child_1.createRooms(bspTree, room_list)
            if self.child_2:
                self.child_2.createRooms(bspTree, room_list)

            if self.child_1 and self.child_2:
                bspTree.createHall(self.child_1.getRoom(),
                                   self.child_2.getRoom())

        else:
            # Create rooms in the end branches of the bsp tree
            w = random.randint(bspTree.ROOM_MIN_SIZE, min(bspTree.ROOM_MAX_SIZE, self.width - 1))
            h = random.randint(bspTree.ROOM_MIN_SIZE, min(bspTree.ROOM_MAX_SIZE, self.height - 1))
            x = random.randint(self.x, self.x + (self.width - 1) - w)
            y = random.randint(self.y, self.y + (self.height - 1) - h)
            self.room = Rect(x, y, w, h)
            room_list.add_room(self.room)
            bspTree.createRoom(self.room)

    def getRoom(self) -> Optional[Rect]:
        if self.room:
            return self.room
        else:
            if self.child_1:
                self.room_1 = self.child_1.getRoom()
            if self.child_2:
                self.room_2 = self.child_2.getRoom()

            if not self.child_1 and not self.child_2:
                # neither room_1 nor room_2
                return None

            elif not self.room_2:
                # room_1 and !room_2
                return self.room_1

            elif not self.room_1:
                # room_2 and !room_1
                return self.room_2

            # If both room_1 and room_2 exist, pick one
            elif random.random() < 0.5:
                return self.room_1
            else:
                return self.room_2


class Prefab(Rect):
    pass
