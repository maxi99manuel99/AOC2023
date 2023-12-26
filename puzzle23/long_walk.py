import numpy as np
import numpy.typing as npt


class HikingMap():
    def __init__(self, map: list[list[str]]) -> None:
        self.map = np.array(map)
        self.height, self.width = self.map.shape

    def get_reachable_neighbors(self, position: tuple[int, int], visited: npt.NDArray, ignore_slopes: bool = False) -> list[tuple[int, int]]:
        """
        Returns all neighbor positions that one could walk too

        :param position: The position to check the neighbors for
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

        if position[0]-1 >= 0 and self.map[position[0]-1][position[1]] != "#" and not visited[position[0]-1][position[1]]:
            neighbors.append((position[0]-1, position[1]))
        if position[0]+1 < self.height and self.map[position[0]+1][position[1]] != "#" and not visited[position[0]+1][position[1]]:
            neighbors.append((position[0]+1, position[1]))
        if position[1]-1 >= 0 and self.map[position[0]][position[1]-1] != "#" and not visited[position[0]][position[1]-1]:
            neighbors.append((position[0], position[1]-1))
        if position[1]+1 < self.width and self.map[position[0]][position[1]+1] != "#" and not visited[position[0]][position[1]+1]:
            neighbors.append((position[0], position[1]+1))

        return neighbors

    def get_possible_path_lengths(self, start: tuple[int, int], goal: tuple[int, int], visited: npt.NDArray, curr_length: int = 0, ignore_slopes: bool = False) -> list[int]:
        pos = start
        visited[pos] = True
        if pos == goal:
            return [curr_length]

        while True:
            neighbors = self.get_reachable_neighbors(pos, visited, ignore_slopes)
            if len(neighbors) == 0:  # dead path
                return []

            elif len(neighbors) == 1:
                pos = neighbors[0]
                curr_length += 1
                visited[pos] = True
                if pos == goal:
                    return [curr_length]

            else:
                path_lengths = []

                for neighbor in neighbors:
                    path_lengths += self.get_possible_path_lengths(
                        neighbor, goal, visited.copy(), curr_length+1, ignore_slopes)
                return path_lengths

    def find_longest_path(self, start: tuple[int, int], goal: tuple[int, int], ignore_slopes: bool = False) -> int:
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
