import numpy as np
from enum import Enum
from concurrent.futures import ThreadPoolExecutor


class MOVING_DIRECTION(Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOT = 3


class ContraptionMap():
    def __init__(self, map: list[list[str]]) -> None:
        self.map = np.array(map)
        self.height, self.width = self.map.shape

    def get_energized_tiles(self) -> list[tuple[int, int]]:
        """
        Starts moving the beam through the map starting from the top left
        moving to the right. Returns a list of all energized fields of the map
        """
        return self.move_and_energize((0, 0), MOVING_DIRECTION.RIGHT, {})

    def get_largest_amount_of_energized_tiles(self) -> int:
        """
        Starts a beam from every tile on the boundary of the map away from the boundary
        and returns the number of energized tiles by that beam that energizes the most tiles
        """
        energized_tiles = []

        def calculate_energized_tiles(start_position, moving_direction):
            return len(self.move_and_energize(start_position, moving_direction, {}))

        with ThreadPoolExecutor() as executor:
            args_list = [
                ((0, x), MOVING_DIRECTION.BOT) for x in range(self.width)
            ] + [
                ((self.height-1, x), MOVING_DIRECTION.TOP) for x in range(self.width)
            ] + [
                ((y, 0), MOVING_DIRECTION.RIGHT) for y in range(self.height)
            ] + [
                ((y, self.width-1), MOVING_DIRECTION.LEFT) for y in range(self.height)
            ]

            futures = [executor.submit(
                calculate_energized_tiles, *args) for args in args_list]

            energized_tiles = [future.result() for future in futures]

        return max(energized_tiles)

    def move_and_energize(self, start_tile: tuple[int, int], direction: MOVING_DIRECTION, already_visited_in_direction: dict) -> list[tuple[int, int]]:
        """
        Recursively moves the beam through the map and returns all fields that are energized on the way

        :param start_tile: The tile to start moving from
        :param direction: The direction to move in
        :param already_visited_in_direction: Contains tuples of tiles and a direction
                                             from which they were encountered as keys and 
                                             a bool. Is used to not get stuck moving in a cycle
        """
        if already_visited_in_direction.get((start_tile, direction), False):
            return []

        energized_tiles = []
        curr_tile = start_tile

        if direction == MOVING_DIRECTION.LEFT:
            while True:
                if curr_tile[1] < 0:
                    return energized_tiles

                energized_tiles.append(curr_tile)
                already_visited_in_direction[(
                    curr_tile, direction)] = True
                tile_state = self.map[curr_tile]

                if tile_state == "|":
                    top_energized = self.move_and_energize(
                        (curr_tile[0]-1, curr_tile[1]), MOVING_DIRECTION.TOP, already_visited_in_direction)
                    bot_energized = self.move_and_energize(
                        (curr_tile[0]+1, curr_tile[1]), MOVING_DIRECTION.BOT, already_visited_in_direction)
                    return list(set(energized_tiles + top_energized + bot_energized))

                elif tile_state == "/":
                    bot_energized = self.move_and_energize(
                        (curr_tile[0]+1, curr_tile[1]), MOVING_DIRECTION.BOT, already_visited_in_direction)
                    return list(set(energized_tiles + bot_energized))

                elif tile_state == "\\":
                    top_energized = self.move_and_energize(
                        (curr_tile[0]-1, curr_tile[1]), MOVING_DIRECTION.TOP, already_visited_in_direction)
                    return list(set(energized_tiles + top_energized))

                else:
                    curr_tile = (curr_tile[0], curr_tile[1]-1)

        elif direction == MOVING_DIRECTION.RIGHT:
            while True:
                if curr_tile[1] >= self.width:
                    return energized_tiles

                energized_tiles.append(curr_tile)
                already_visited_in_direction[(
                    curr_tile, direction)] = True
                tile_state = self.map[curr_tile]

                if tile_state == "|":
                    top_energized = self.move_and_energize(
                        (curr_tile[0]-1, curr_tile[1]), MOVING_DIRECTION.TOP, already_visited_in_direction)
                    bot_energized = self.move_and_energize(
                        (curr_tile[0]+1, curr_tile[1]), MOVING_DIRECTION.BOT, already_visited_in_direction)
                    return list(set(energized_tiles + top_energized + bot_energized))

                elif tile_state == "/":
                    top_energized = self.move_and_energize(
                        (curr_tile[0]-1, curr_tile[1]), MOVING_DIRECTION.TOP, already_visited_in_direction)
                    return list(set(energized_tiles + top_energized))

                elif tile_state == "\\":
                    bot_energized = self.move_and_energize(
                        (curr_tile[0]+1, curr_tile[1]), MOVING_DIRECTION.BOT, already_visited_in_direction)
                    return list(set(energized_tiles + bot_energized))

                else:
                    curr_tile = (curr_tile[0], curr_tile[1]+1)

        elif direction == MOVING_DIRECTION.TOP:
            while True:
                if curr_tile[0] < 0:
                    return energized_tiles

                energized_tiles.append(curr_tile)
                already_visited_in_direction[(
                    curr_tile, direction)] = True
                tile_state = self.map[curr_tile]

                if tile_state == "-":
                    left_energized = self.move_and_energize(
                        (curr_tile[0], curr_tile[1]-1), MOVING_DIRECTION.LEFT, already_visited_in_direction)
                    right_energized = self.move_and_energize(
                        (curr_tile[0], curr_tile[1]+1), MOVING_DIRECTION.RIGHT, already_visited_in_direction)
                    return list(set(energized_tiles + left_energized + right_energized))

                elif tile_state == "/":
                    right_energized = self.move_and_energize(
                        (curr_tile[0], curr_tile[1]+1), MOVING_DIRECTION.RIGHT, already_visited_in_direction)
                    return list(set(energized_tiles + right_energized))

                elif tile_state == "\\":
                    left_energized = self.move_and_energize(
                        (curr_tile[0], curr_tile[1]-1), MOVING_DIRECTION.LEFT, already_visited_in_direction)
                    return list(set(energized_tiles + left_energized))

                else:
                    curr_tile = (curr_tile[0]-1, curr_tile[1])

        elif direction == MOVING_DIRECTION.BOT:
            while True:
                if curr_tile[0] >= self.height:
                    return energized_tiles

                energized_tiles.append(curr_tile)
                already_visited_in_direction[(
                    curr_tile, direction)] = True
                tile_state = self.map[curr_tile]

                if tile_state == "-":
                    left_energized = self.move_and_energize(
                        (curr_tile[0], curr_tile[1]-1), MOVING_DIRECTION.LEFT, already_visited_in_direction)
                    right_energized = self.move_and_energize(
                        (curr_tile[0], curr_tile[1]+1), MOVING_DIRECTION.RIGHT, already_visited_in_direction)
                    return list(set(energized_tiles + left_energized + right_energized))

                elif tile_state == "/":
                    left_energized = self.move_and_energize(
                        (curr_tile[0], curr_tile[1]-1), MOVING_DIRECTION.LEFT, already_visited_in_direction)
                    return list(set(energized_tiles + left_energized))

                elif tile_state == "\\":
                    right_energized = self.move_and_energize(
                        (curr_tile[0], curr_tile[1]+1), MOVING_DIRECTION.RIGHT, already_visited_in_direction)
                    return list(set(energized_tiles + right_energized))

                else:
                    curr_tile = (curr_tile[0]+1, curr_tile[1])


if __name__ == "__main__":
    with open("input.txt") as fp:
        map = []
        while line := fp.readline():
            line = list(line.strip())
            map.append(line)
        map = ContraptionMap(map)
        energized_tiles = map.get_energized_tiles()
        print(f"Part 1 Result: {len(energized_tiles)}")
        print(f"Part 2 Result: {map.get_largest_amount_of_energized_tiles()}")
