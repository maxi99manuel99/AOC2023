from enum import Enum
import numpy as np


class PipeMap():

    char_to_pipe = {
        "J": ("top", "left"),
        "F": ("bot", "right"),
        "7": ("bot", "left"),
        "L": ("top", "right"),
        "-": ("left", "right"),
        "|": ("top", "bot"),
    }

    direction_to_idx_change = {
        "top": (-1, 0),
        "bot": (+1, 0),
        "right": (0, 1),
        "left": (0, -1)
    }

    opposites = {
        "left": "right",
        "right": "left",
        "top": "bot",
        "bot": "top",
    }

    def __init__(self, map: list, start_point: tuple[int, int]) -> None:
        self.map = np.array(map)
        self.start = start_point
        self.loop = None

    def get_valid_next_directions(self, tile_position: tuple[int, int]) -> list[str]:
        """
        For a give tile checks what neighboring tiles connect to this tile and returns all
        directions that can be traveled from this tile

        :param tile_position: the position of the tile that we want to check
        """
        height, width = self.map.shape
        row, col = tile_position[0], tile_position[1]
        valid_directions = []

        if not row+1 >= height:
            if self.map[row+1][col] in ["J", "L", "|"]:
                valid_directions.append("bot")

        if not row-1 < 0:
            if self.map[row-1][col] in ["F", "7", "|"]:
                valid_directions.append("top")

        if not col-1 < 0:
            if self.map[row][col-1] in ["F", "L", "-"]:
                valid_directions.append("left")

        if not col+1 >= width:
            if self.map[row][col+1] in ["J", "7", "-"]:
                valid_directions.append("right")

        return valid_directions

    def get_loop(self) -> None:
        """
        Saves all positions on the loop from start to start in this
        PipeMap in the loop variable of this class
        """
        valid_directions = self.get_valid_next_directions(self.start)
        self.map[self.start[0], self.start[1]] = list(self.char_to_pipe.keys())[list(
            self.char_to_pipe.values()).index(tuple(valid_directions))]
        last_direction = valid_directions[0]
        idx_plus = self.direction_to_idx_change[last_direction]

        pos = (self.start[0] + idx_plus[0], self.start[1] + idx_plus[1])
        self.loop = [self.start, pos]

        while pos != self.start:
            pipe = self.char_to_pipe[self.map[pos[0]][pos[1]]]

            if pipe[0] != self.opposites[last_direction]:
                next_direction = pipe[0]
            else:
                next_direction = pipe[1]

            idx_plus = self.direction_to_idx_change[next_direction]
            pos = (pos[0] + idx_plus[0], pos[1] + idx_plus[1])

            self.loop.append(pos)
            last_direction = next_direction

    def is_tile_inside_loop(self, tile_position: tuple[int, int]) -> bool:
        """
        Checks if a tile is enclosed by the loop of this PipeMap

        :param tile: The position of the tile that we want to check
        """
        curr_pos = (tile_position[0], tile_position[1]-1)
        intersections = 0
        currently_on_edge = False

        while curr_pos[1] >= 0:
            pipe = self.map[curr_pos[0], curr_pos[1]]

            if currently_on_edge:
                if pipe == "F" or pipe == "L":
                    currently_on_edge = False
                    if edge_start == "7" and pipe == "L":
                        intersections += 1
                    elif edge_start == "J" and pipe == "F":
                        intersections += 1

            elif pipe == "|" and (curr_pos in self.loop):
                intersections += 1

            if (pipe == "7" or pipe == "J") and (curr_pos in self.loop):
                edge_start = pipe
                currently_on_edge = True

            curr_pos = (curr_pos[0], curr_pos[1]-1)

        return intersections % 2 != 0

    def calculate_num_tiles_inside_loop(self) -> int:
        """
        Returns the number of tiles in this PipeMap that are enclosed 
        in the loop of this PipeMap
        """
        min_row, max_row = min(self.loop, key=lambda x: x[0])[
            0], max(self.loop, key=lambda x: x[0])[0]
        min_col, max_col = min(self.loop, key=lambda x: x[1])[
            1], max(self.loop, key=lambda x: x[1])[1]
        points_to_test = [(row, col) for row in range(min_row+1, max_row)
                          for col in range(min_col+1, max_col)]

        return sum(self.is_tile_inside_loop(point) for point in points_to_test if point not in self.loop)


if __name__ == "__main__":
    map = []
    with open("input.txt") as fp:
        row = 0
        while line := fp.readline().strip():
            map.append(list(line))
            if "S" in line:
                col = line.index("S")
                start_point = (row, col)
            row += 1

        map = PipeMap(map, start_point)
        loop = map.get_loop()
        print(f"Part 1 Result: {(len(map.loop)) // 2}")
        print(f"Part 2 Result: {map.calculate_num_tiles_inside_loop()}")
