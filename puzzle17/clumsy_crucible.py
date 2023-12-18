from enum import Enum
import numpy as np
import heapq


class DIRECTION(Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOT = 3
    UNDEFINED = 4


class QueueObject():
    def __init__(self, position: tuple[int, int], heat_loss: int, moving_direction: tuple[DIRECTION, int]) -> None:
        self.position = position
        self.heat_loss = heat_loss
        self.moving_direction = moving_direction

    def __lt__(self, other):
        return self.heat_loss < other.heat_loss


class HeatLossMap():
    def __init__(self, map: list[list[int]]) -> None:
        self.heat_map = np.array(map)
        self.height, self.width = self.heat_map.shape

    def find_route_with_min_heat_loss(self, start_block: tuple[int, int], goal_block: tuple[int, int], minimal_steps_in_direction: int, maximal_steps_in_direction: int) -> int:
        """
        Finds route of minimal heat loss from start_block to goal block using dijkstra

        :param start_block: the block to start on (the heat loss of this block is not considered)
        :param goal_block: the block to get to
        :param minimal_steps_in_direction: defines the minimum amount of steps we need to take in one direction before turning
        :param maximal_steps_in_direction: defines the maximum amount of steps we are allowed to move into one direction until turning
        """
        priority_queue = []
        visited = set()

        for neighbor_pos, (neighbor_direction, neighbor_streak) in self.get_neighbors(start_block, DIRECTION.UNDEFINED, 9999, minimal_steps_in_direction, maximal_steps_in_direction):
            neighbor_obj = QueueObject(
                neighbor_pos, self.heat_map[neighbor_pos], (neighbor_direction, neighbor_streak))
            heapq.heappush(priority_queue, neighbor_obj)
        

        while priority_queue:
            curr_obj = heapq.heappop(priority_queue)
            pos, heat_loss, (prev_direction,
                             direction_streak) = curr_obj.position, curr_obj.heat_loss, curr_obj.moving_direction
            if pos == goal_block:
                return heat_loss

            if (pos, prev_direction, direction_streak) in visited:
                continue

            visited.add((pos, prev_direction, direction_streak))

            for neighbor_pos, (neighbor_direction, neighbor_streak) in self.get_neighbors(pos, prev_direction, direction_streak, minimal_steps_in_direction, maximal_steps_in_direction):
                if (neighbor_pos, neighbor_direction, neighbor_streak) not in visited:
                    neighbor_obj = QueueObject(
                        neighbor_pos, heat_loss + self.heat_map[neighbor_pos], (neighbor_direction, neighbor_streak))
                    heapq.heappush(priority_queue, neighbor_obj)

    def get_neighbors(self, pos: tuple[int, int], prev_direction: DIRECTION, direction_streak: int, minimal_steps_in_direction: int, maximal_steps_in_direction: int) -> list[tuple[tuple[int, int], tuple[DIRECTION, int]]]:
        """
        Returns all neighbors for a given block but only if it is still viable to move to those neighbors
        (based on the previous direction and how many times we went straight in that direction)

        :param pos: the block to get the neighbors of
        :param prev_direction: the direction we were previously moving
        :param direction_streak: for how many times straight we already moved into that direction
        :param minimal_steps_in_direction: defines the minimum amount of steps we need to take in one direction before turning
        :param maximal_steps_in_direction: defines the maximum amount of steps we are allowed to move into one direction until turning
        """
        neighbors = []
        print(prev_direction)
        print(direction_streak)
        if (pos[0] - 1 >= 0) and not (prev_direction == DIRECTION.TOP and direction_streak == maximal_steps_in_direction) and not (prev_direction != DIRECTION.TOP and direction_streak < minimal_steps_in_direction) and not prev_direction == DIRECTION.BOT:
            top_pos = (pos[0] - 1, pos[1])
            new_direction_streak = direction_streak + \
                1 if prev_direction == DIRECTION.TOP else 1
            neighbors.append((top_pos, (DIRECTION.TOP, new_direction_streak)))

        if (pos[0] + 1 < self.height) and not (prev_direction == DIRECTION.BOT and direction_streak == maximal_steps_in_direction) and not (prev_direction != DIRECTION.BOT and direction_streak < minimal_steps_in_direction) and not prev_direction == DIRECTION.TOP:
            bot_pos = (pos[0] + 1, pos[1])
            new_direction_streak = direction_streak + \
                1 if prev_direction == DIRECTION.BOT else 1
            neighbors.append((bot_pos, (DIRECTION.BOT, new_direction_streak)))

        if (pos[1] - 1 >= 0) and not (prev_direction == DIRECTION.LEFT and direction_streak == maximal_steps_in_direction) and not (prev_direction != DIRECTION.LEFT and direction_streak < minimal_steps_in_direction) and not prev_direction == DIRECTION.RIGHT:
            left_pos = (pos[0], pos[1] - 1)
            new_direction_streak = direction_streak + \
                1 if prev_direction == DIRECTION.LEFT else 1
            neighbors.append(
                (left_pos, (DIRECTION.LEFT, new_direction_streak)))

        if (pos[1] + 1 < self.width) and not (prev_direction == DIRECTION.RIGHT and direction_streak == maximal_steps_in_direction) and not (prev_direction != DIRECTION.RIGHT and direction_streak < minimal_steps_in_direction) and not prev_direction == DIRECTION.LEFT:
            right_pos = (pos[0], pos[1] + 1)
            new_direction_streak = direction_streak + \
                1 if prev_direction == DIRECTION.RIGHT else 1
            neighbors.append(
                (right_pos, (DIRECTION.RIGHT, new_direction_streak)))
        print(neighbors)
        return neighbors


if __name__ == "__main__":
    with open("input.txt") as fp:
        map_data = []
        while line := fp.readline().strip():
            map_data.append([int(x) for x in line])
        heat_map = HeatLossMap(map_data)
        print(
            f"Part 1 Result: {heat_map.find_route_with_min_heat_loss((0, 0), (heat_map.height - 1, heat_map.width - 1), 1, 3)}")
        print(
            f"Part 2 Result: {heat_map.find_route_with_min_heat_loss((0, 0), (heat_map.height - 1, heat_map.width - 1), 4, 10)}")
