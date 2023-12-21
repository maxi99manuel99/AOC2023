import numpy as np
import heapq

class GardenMap():
    def __init__(self, map: list[list[str]]) -> None:
        self.map = np.array(map)
        self.height, self.width = self.map.shape
        rock_indices = np.where(self.map == "#")
        rock_indices = list(zip(rock_indices[0], rock_indices[1]))
        self.rock_map = np.zeros_like(self.map, dtype=bool)
        for idx in rock_indices:
            self.rock_map[idx] = True

    def get_reachable_neighbors(self, position: tuple[int, int], allow_overflow: bool=False) -> list[tuple[int, int]]:
        """
        Returns all neighbor positions that are not blocked by a rock

        :param position: The position to check the neighbors for
        """
        neighbors = []
        if allow_overflow:
            if not self.rock_map[self.position_translate((position[0]-1, position[1]))]:
                neighbors.append((position[0]-1, position[1]))
            if not self.rock_map[self.position_translate((position[0]+1, position[1]))]:
                neighbors.append((position[0]+1, position[1]))
            if not self.rock_map[self.position_translate((position[0], position[1]-1))]:
                neighbors.append((position[0], position[1]-1))
            if not self.rock_map[self.position_translate((position[0], position[1]+1))]:
                neighbors.append((position[0], position[1]+1))

        else:
            if position[0]-1 >= 0 and not self.rock_map[position[0]-1][position[1]]:
                neighbors.append((position[0]-1, position[1]))
            if position[0]+1 < self.height and not self.rock_map[position[0]+1][position[1]]:
                neighbors.append((position[0]+1, position[1]))
            if position[1]-1 >= 0 and not self.rock_map[position[0]][position[1]-1]:
                neighbors.append((position[0], position[1]-1))
            if position[1]+1 < self.width and not self.rock_map[position[0]][position[1]+1]:
                neighbors.append((position[0], position[1]+1))
        
        return neighbors       
    
    def position_translate(self, pos):
        return (pos[0] % self.height, pos[1] % self.width)
    
    def get_number_reachable_fields(self, start_pos: tuple[int, int], max_steps: int, allow_overflow: bool=False) -> int:
        """
        Returns the number of fields that can be reached from the start position by walking
        max_steps steps

        :param start_pos: The position that one starts at
        :param max_steps: The amount of steps that must be walked
        :param allow_overflow: if set than the map loops in every direction, defaults to False
        """
        possible_after_max_steps = set()
        visited = set()
        modulo_modifier = 0 if max_steps % 2 == 0 else 1
        if modulo_modifier == 0:
            possible_after_max_steps.add(start_pos)
            visited.add(start_pos)
    
        queue = []
        for neighbor_pos in self.get_reachable_neighbors(start_pos):
            heapq.heappush(queue, (1, neighbor_pos))
        
        while queue:
            walked_steps, pos = heapq.heappop(queue)
            if pos in visited:
                continue
            
            visited.add(pos)
            if (walked_steps - modulo_modifier) % 2 == 0:
                possible_after_max_steps.add(pos) 
            
            if not walked_steps == max_steps:
                for neighbor_pos in self.get_reachable_neighbors(pos, allow_overflow=allow_overflow):
                    if neighbor_pos not in visited:
                        heapq.heappush(queue, (walked_steps+1, neighbor_pos))

        return len(possible_after_max_steps)

if __name__ == "__main__":
    map = []
    with open("input.txt") as fp:
        row = 0
        while line := fp.readline():
            if "S" in line:
                start = (row, line.index("S"))
            map.append(list(line.strip()))
            row += 1

    map = GardenMap(map)
    print(f"Result Part 1: {map.get_number_reachable_fields(start, 64)}")
    print(f"Result Part 2: {map.get_number_reachable_fields(start, 1000, allow_overflow=True)}")