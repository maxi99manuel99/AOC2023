import numpy as np
import numpy.typing as npt


class HikingMap():
    def __init__(self, map: list[list[str]]) -> None:
        self.map = np.array(map)
        self.height, self.width = self.map.shape

    def get_reachable_neighbors(self, position: tuple[int, int], visited: npt.NDArray, ignore_slopes: bool = False) -> list[tuple[int, int]]:
        """
        Returns all neighbor positions that one could walk to

        :param position: The position to check the neighbors for
        :param visited: All positions that were already visited (we do not step on the same tile twice)
        :param ignore_slopes: If set to true slopes are treated as normal path points, defaults to False
        """
        if not ignore_slopes:
            if self.map[position] == "^":
                if visited[position[0]-1][position[1]]:
                    return []
                return [(position[0]-1, position[1])]
            elif self.map[position] == "v":
                if visited[position[0]+1][position[1]]:
                    return []
                return [(position[0]+1, position[1])]
            elif self.map[position] == ">":
                if visited[position[0]][position[1]+1]:
                    return []
                return [(position[0], position[1]+1)]
            elif self.map[position] == "<":
                if visited[position[0]][position[1]-1]:
                    return []
                return [(position[0], position[1]-1)]

        neighbors = []

        if position[0]-1 >= 0 and self.map[position[0]-1][position[1]] != "#" and not visited[position[0]-1][position[1]] and not (position[1] == 0 or position[1] == self.width-1):
            neighbors.append((position[0]-1, position[1]))
        if position[0]+1 < self.height and self.map[position[0]+1][position[1]] != "#" and not visited[position[0]+1][position[1]]:
            neighbors.append((position[0]+1, position[1]))
        if position[1]-1 >= 0 and self.map[position[0]][position[1]-1] != "#" and not visited[position[0]][position[1]-1]:
            neighbors.append((position[0], position[1]-1))
        if position[1]+1 < self.width and self.map[position[0]][position[1]+1] != "#" and not visited[position[0]][position[1]+1]:
            neighbors.append((position[0], position[1]+1))

        return neighbors

    def get_possible_path_lengths(self, start: tuple[int, int], goal: tuple[int, int], visited: npt.NDArray, curr_length: int = 0, ignore_slopes: bool = False) -> list[int]:
        """
        Returns a list containing all possible path lengths from start to goal, by recursively traversing the map

        :param start: the start point
        :param goal: the point we want to reach
        :param visited: all visited fields in the current recursion
        :param curr_length: the path length in the current recursion, defaults to 0
        :param ignore_slopes: If set to true slopes are treated as normal path points, defaults to False
        """
        pos = start
        visited[pos] = True
        visited_in_recursion_step = set([pos])
        if pos == goal:
            for x in visited_in_recursion_step:
                visited[x] = False
            return [curr_length]

        while True:
            neighbors = self.get_reachable_neighbors(pos, visited, ignore_slopes)
            if len(neighbors) == 0:  # dead path
                for x in visited_in_recursion_step:
                    visited[x] = False
                return []

            elif len(neighbors) == 1:
                pos = neighbors[0]
                curr_length += 1
                visited[pos] = True
                visited_in_recursion_step.add(pos)
                if pos == goal:
                    for x in visited_in_recursion_step:
                        visited[x] = False
                    return [curr_length]

            else:
                path_lengths = []

                for neighbor in neighbors:
                    path_lengths += self.get_possible_path_lengths(
                        neighbor, goal, visited, curr_length+1, ignore_slopes)
                for x in visited_in_recursion_step:
                    visited[x] = False
                return path_lengths

    def find_longest_path(self, start: tuple[int, int], goal: tuple[int, int], ignore_slopes: bool = False) -> int:
        """
        Returns the length of the longest path between start and goal

        :param start: the start point
        :param goal: the point we want to reach
        :param ignore_slopes: If set to true slopes are treated as normal path points, defaults to False
        """
        paths = self.get_possible_path_lengths(start, goal, np.zeros_like(
            self.map, dtype=bool), ignore_slopes=ignore_slopes)
        return max(paths)


if __name__ == "__main__":
    map = []
    with open("input.txt") as fp:
        row = 0
        while line := fp.readline():
            map.append(list(line.strip()))
            row += 1
        start = (0, map[0].index("."))
        goal = (len(map)-1, map[-1].index("."))

    map = HikingMap(map)
    print(f"Part 1 Result: {map.find_longest_path(start, goal)}")
    print(f"Part 2 Result: {map.find_longest_path(start, goal, ignore_slopes=True)}")
