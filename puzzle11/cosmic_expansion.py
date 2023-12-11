import numpy as np

class Map():
    def __init__(self, map: list[list[str]]) -> None:
        self.map = map
        self.galaxy_indices = list(zip(*np.where(np.array(map) == "#")))

    def expand(self, empty_multiplier: int) -> None:
        """
        Calculates the new indices of all galaxies, if the map were to be extended

        :param empty_multiplier: defines how many new rows/cols arise from an empty row/col
        """
        map = np.array(self.map)
        rows, cols = map.shape
        old_galaxies = self.galaxy_indices.copy()
        
        for i in range(rows):
            if not "#" in map[i]:
                for j, galaxy in enumerate(old_galaxies):
                    if galaxy[0] > i:
                        self.galaxy_indices[j] = (self.galaxy_indices[j][0]+(empty_multiplier-1), self.galaxy_indices[j][1])

        for i in range(cols):
            if not "#" in map[:, i]:
                for j, galaxy in enumerate(old_galaxies):
                    if galaxy[1] > i:
                        self.galaxy_indices[j] = (self.galaxy_indices[j][0], self.galaxy_indices[j][1]+(empty_multiplier-1))      
    
    def calculate_sum_shortest_paths(self) -> int:
        """
        Returns the sum of the manhattan distance of all pairs
        of galaxy indices (which is the distance of the shortest path between them)
        """
        sum = 0
        for i, (y, x) in enumerate(self.galaxy_indices[:-1]):
            for (y2, x2) in self.galaxy_indices[i+1:]:
                sum += abs(y - y2) + abs(x - x2)
        
        return sum


if __name__ == "__main__":
    map = []
    with open("input.txt") as fp:
        while line := fp.readline():
            map.append(list(line.strip()))

    map1 = Map(map)
    map1.expand(2)
    print(f"Part 1 Result: {map1.calculate_sum_shortest_paths()}")
    map2 = Map(map)
    map2.expand(1000000)
    print(f"Part 2 Result: {map2.calculate_sum_shortest_paths()}")
            