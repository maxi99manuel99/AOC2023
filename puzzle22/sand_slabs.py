import numpy as np
import numpy.typing as npt
from dataclasses import dataclass
import copy


@dataclass
class BrickRange():
    expanding_dim: int
    start: tuple[int, int, int]
    end: tuple[int, int, int]


class BrickMap():
    def __init__(self, map: npt.NDArray, bricks: list[int, BrickRange]) -> None:
        self.map = map
        self.bricks = bricks

    def update_brick_map(self, brick_key: int, old_brick_start: tuple[int, int, int], old_brick_end: tuple[int, int, int], new_brick_start: tuple[int, int, int], new_brick_end: tuple[int, int, int], expanding_dim: int) -> None:
        """
        Resets map values at old positions to 0 and adds the key of the brick at the new positions

        :param brick_key: The brick_key of the brick we want to replace
        :param old_brick_start: the old starting position of the brick
        :param old_brick_end: the old ending position of the brick
        :param new_brick_start: the new starting position of the brick
        :param new_brick_end: the new ending position of the brick
        :param expanding_dim: the dim this brick is expanding to
        """
        if expanding_dim == 0:
            y = old_brick_start[1]
            z = old_brick_start[2]
            for x in range(old_brick_start[0], old_brick_end[0]+1):
                self.map[(x, y, z)] = 0
            y = new_brick_start[1]
            z = new_brick_start[2]
            for x in range(new_brick_start[0], new_brick_end[0]+1):
                self.map[(x, y, z)] = brick_key

        elif expanding_dim == 1:
            x = old_brick_start[0]
            z = old_brick_start[2]
            for y in range(old_brick_start[1], old_brick_end[1]+1):
                self.map[(x, y, z)] = 0
            x = new_brick_start[0]
            z = new_brick_start[2]
            for y in range(new_brick_start[1], new_brick_end[1]+1):
                self.map[(x, y, z)] = brick_key

        elif expanding_dim == 2:
            x = old_brick_start[0]
            y = old_brick_start[1]
            for z in range(old_brick_start[2], old_brick_end[2]+1):
                self.map[(x, y, z)] = 0
            x = new_brick_start[0]
            y = new_brick_start[1]
            for z in range(new_brick_start[2], new_brick_end[2]+1):
                self.map[(x, y, z)] = brick_key

        else:
            self.map[old_brick_start] = 0
            self.map[old_brick_end] = 0
            self.map[new_brick_start] = brick_key
            self.map[new_brick_end] = brick_key

    def bricks_fall(self) -> None:
        """
        Will cause all bricks to fall to the ground / fall as far as they can
        """
        self.bricks.sort(key=lambda x: x[1].start[2])
        for brick_key, brick in self.bricks:
            lowest_z_possible = brick.start[2]
            while True:
                if lowest_z_possible == 1:
                    break

                brick_below = False
                if brick.expanding_dim == 0:
                    y = brick.start[1]
                    for x in range(brick.start[0], brick.end[0]+1):
                        if self.map[(x, y, lowest_z_possible-1)] != 0:
                            brick_below = True
                            break

                elif brick.expanding_dim == 1:
                    x = brick.start[0]
                    for y in range(brick.start[1], brick.end[1]+1):
                        if self.map[(x, y, lowest_z_possible-1)] != 0:
                            brick_below = True
                            break
                else:
                    x = brick.start[0]
                    y = brick.start[1]
                    if self.map[(x, y, lowest_z_possible-1)] != 0:
                        brick_below = True

                if brick_below:
                    break

                lowest_z_possible -= 1

            old_brick_start = copy.deepcopy(brick.start)
            old_brick_end = copy.deepcopy(brick.end)
            brick.end = (brick.end[0], brick.end[1],
                         lowest_z_possible+(brick.end[2] - brick.start[2]))
            brick.start = (brick.start[0], brick.start[1], lowest_z_possible)

            self.update_brick_map(brick_key, old_brick_start, old_brick_end,
                                  brick.start, brick.end, brick.expanding_dim)

    def count_possible_disintegrations(self) -> int:
        """
        Returns the count of bricks can be disintegrated from the system
        without leading other bricks to fall further down
        """
        not_disintegratable = set()
        self.bricks.sort(key=lambda x: x[1].start[2])
        for _, brick in self.bricks:
            supporting_bricks = set()
            z = brick.start[2]

            if brick.expanding_dim == 0:
                y = brick.start[1]
                for x in range(brick.start[0], brick.end[0]+1):
                    if self.map[(x, y, z-1)] != 0:
                        supporting_bricks.add(self.map[(x, y, z-1)])

            elif brick.expanding_dim == 1:
                x = brick.start[0]
                for y in range(brick.start[1], brick.end[1]+1):
                    if self.map[(x, y, z-1)] != 0:
                        supporting_bricks.add(self.map[(x, y, z-1)])

            else:
                x = brick.start[0]
                y = brick.start[1]
                if self.map[(x, y, z-1)] != 0:
                    supporting_bricks.add(self.map[(x, y, z-1)])

            if len(supporting_bricks) == 1:
                not_disintegratable.add(list(supporting_bricks)[0])

        return len(self.bricks) - len(not_disintegratable)

    def count_disintegrations_caused_by(self, key: int) -> int:
        """
        For a given brick (given by key) returns the number of disintegrations that would
        happen if you were to disintegrate that brick

        :param key: the key of the brick to be disintegrated first
        """
        disintigrated = set([key])
        key_q = []
        count = 0
        key_q.append(key)
        while key_q:
            key = key_q.pop(0)
            if key not in self.support_dict:
                continue

            supported_keys = list(self.support_dict[key])
            for other_key in supported_keys:
                suported_by = self.supported_by_dict[other_key]
                all_supporters_broken = True
                for support in suported_by:
                    if support not in disintigrated:
                        all_supporters_broken = False
                        break
                if other_key not in disintigrated and all_supporters_broken:
                    key_q.append(other_key)
                    disintigrated.add(other_key)
                    count += 1

        return count

    def sum_disintegrations_per_brick(self) -> int:
        """
        For each brick calculates the number of other bricks that would disintegrate if that
        brick would disintegrate and sums up all the results from each brick
        """
        self.bricks.sort(key=lambda x: x[1].start[2])
        self.support_dict = {}
        self.supported_by_dict = {}
        for brick_key, brick in self.bricks:
            z = brick.start[2]

            if brick.expanding_dim == 0:
                y = brick.start[1]
                for x in range(brick.start[0], brick.end[0]+1):
                    if self.map[(x, y, z-1)] != 0:
                        self.supported_by_dict.setdefault(
                            brick_key, set()).add(self.map[(x, y, z-1)])
                        self.support_dict.setdefault(
                            self.map[(x, y, z-1)], set()).add(brick_key)

            elif brick.expanding_dim == 1:
                x = brick.start[0]
                for y in range(brick.start[1], brick.end[1]+1):
                    if self.map[(x, y, z-1)] != 0:
                        self.supported_by_dict.setdefault(
                            brick_key, set()).add(self.map[(x, y, z-1)])
                        self.support_dict.setdefault(
                            self.map[(x, y, z-1)], set()).add(brick_key)

            else:
                x = brick.start[0]
                y = brick.start[1]
                if self.map[(x, y, z-1)] != 0:
                    self.supported_by_dict.setdefault(
                        brick_key, set()).add(self.map[(x, y, z-1)])
                    self.support_dict.setdefault(
                        self.map[(x, y, z-1)], set()).add(brick_key)
        sum = 0

        for key in self.support_dict.keys():
            sum += self.count_disintegrations_caused_by(key)

        return sum


if __name__ == "__main__":
    bricks = {}
    with open("input.txt") as fp:
        max_x = 0
        max_y = 0
        max_z = 0
        bricks = []
        while line := fp.readline():
            brick_start, brick_end = line.split("~")
            brick_start = brick_start.split(",")
            brick_end = brick_end.split(",")
            brick_start = tuple(int(x) for x in brick_start)
            brick_end = tuple(int(x) for x in brick_end)
            bricks.append((brick_start, brick_end))

            if brick_end[0]+1 > max_x:
                max_x = brick_end[0]+1
            if brick_end[1]+1 > max_y:
                max_y = brick_end[1]+1
            if brick_end[2]+1 > max_z:
                max_z = brick_end[2]+1

        brick_map = np.zeros((max_x, max_y, max_z), dtype=int)
        for j, (brick_start, brick_end) in enumerate(bricks):
            expanding_dim = np.where(
                np.array(brick_start) != np.array(brick_end))[0]

            if len(expanding_dim) > 0:
                expanding_dim = expanding_dim[0]
                bricks[j] = (
                    j+1, BrickRange(expanding_dim=expanding_dim, start=brick_start, end=brick_end))
                for i in range(brick_start[expanding_dim], brick_end[expanding_dim]+1):
                    if expanding_dim == 0:
                        brick_map[(i, brick_start[1], brick_start[2])] = j+1
                    elif expanding_dim == 1:
                        brick_map[(brick_start[0], i, brick_start[2])] = j+1
                    else:
                        brick_map[(brick_start[0], brick_start[1], i)] = j+1

            else:
                bricks[j] = (j+1, BrickRange(expanding_dim=np.inf,
                             start=brick_start, end=brick_end))
                brick_map[brick_start] = j+1
                brick_map[brick_end] = j+1

        brick_map = BrickMap(brick_map, bricks)
        brick_map.bricks_fall()
        print(f"Part 1 Result: {brick_map.count_possible_disintegrations()}")
        print(f"Part 2 Result: {brick_map.sum_disintegrations_per_brick()}")
