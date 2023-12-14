from enum import Enum
import numpy as np

class ReflectorDish():
    class TILE_DIRECTION(Enum):
        LEFT = 1
        RIGHT = 2
        TOP = 3
        BOT = 4

    def __init__(self, map: list[list[str]]) -> None:
        self.map = np.array(map)
        self.height, self.width = self.map.shape
        self.row_boundaries = self.get_row_boundaries()
        self.col_boundaries = self.get_col_boundaries()
        self.rock_positions = np.where(self.map == "O")
        self.rock_positions = tuple([((idx1, idx2)) for idx1, idx2 in zip(self.rock_positions[0], self.rock_positions[1])])
    
    def execute_tiling_and_get_loads(self) -> tuple[int, int]:
        """
        Executes tiling to the north and returns the resulting load on the north boundary,
        and executes 1000000000 spin cycles, again returning the respective load on the north boundary
        after these
        """
        new_rock_positions_p1 = self.tile(self.rock_positions, self.TILE_DIRECTION.TOP)
        load_north_p1 =  self.calc_load_on_north(new_rock_positions_p1)
        new_rock_positions_p2 = self.cycle_n_times(1000000000, self.rock_positions)
        load_north_p2 = self.calc_load_on_north(new_rock_positions_p2)
        
        return load_north_p1, load_north_p2
    
    def get_row_boundaries(self) -> list[list[int]]:
        """
        Returns a matrix where each row of the matrix represents the
        indices of the boundaries in that row. The boundaries
        are all "#" rocks and the west and east end of the platform
        """
        row_boundaries = []
        for row in self.map:
            boundary = [-1]
            boundary += list(np.where(row == "#")[0])
            boundary.append(self.width)
            row_boundaries.append(boundary)
        return row_boundaries
    
    def get_col_boundaries(self) -> list[list[int]]:
        """
        Returns a matrix where each row of the matrix represents the
        indices of the boundaries in the respective column. The boundaries
        are all "#" rocks and the west and east end of the platform
        """
        col_boundaries = []
        for col in self.map.transpose():
            boundary = [-1]
            boundary += list(np.where(col == "#")[0])
            boundary.append(self.height)
            col_boundaries.append(boundary)
        return col_boundaries
    
    def tile(self, rock_positions: tuple[tuple[int, int]], direction: TILE_DIRECTION) -> tuple[tuple[int, int]]:
        """
        Tiles the platform the Dish is on in a certain direction, which will cause all "O" rocks to move
        to the next "#" or the end of the platform in that direction. Returns the position of the rocks after 
        tiling

        :param rock_positions: The rock positions before tiling. Each position consits of (row, col)
        :param direction: Determines the direction to tile the platform
        """
        new_rock_positions = []
        
        if direction == self.TILE_DIRECTION.LEFT:
            boundaries = self.row_boundaries
            last_free_indices = [[1]*len(boundary) for boundary in boundaries] 
            for rock_pos in rock_positions:
                row, col = rock_pos

                for i, boundary_idx in enumerate(boundaries[row][::-1]):
                    if col > boundary_idx:
                        new_rock_positions.append((row, boundary_idx+last_free_indices[row][len(boundaries[row])-1-i]))
                        last_free_indices[row][len(boundaries[row])-1-i] += 1
                        break
    
        elif direction == self.TILE_DIRECTION.RIGHT:
            boundaries = self.row_boundaries
            last_free_indices = [[1]*len(boundary) for boundary in boundaries] 
            for rock_pos in rock_positions:
                row, col = rock_pos

                for i, boundary_idx in enumerate(boundaries[row]):
                    if col < boundary_idx:
                        new_rock_positions.append((row, boundary_idx-last_free_indices[row][i]))
                        last_free_indices[row][i] += 1
                        break

        elif direction == self.TILE_DIRECTION.TOP:
            boundaries = self.col_boundaries
            last_free_indices = [[1]*len(boundary) for boundary in boundaries] 
            for rock_pos in rock_positions:
                row, col = rock_pos

                for i, boundary_idx in enumerate(boundaries[col][::-1]):
                    if row > boundary_idx:
                        new_rock_positions.append((boundary_idx+last_free_indices[col][len(boundaries[col])-1-i], col))
                        last_free_indices[col][len(boundaries[col])-1-i] += 1
                        break

        elif direction == self.TILE_DIRECTION.BOT:
            boundaries = self.col_boundaries.copy()
            last_free_indices = [[1]*len(boundary) for boundary in boundaries] 
            for rock_pos in rock_positions:
                row, col = rock_pos

                for i, boundary_idx in enumerate(boundaries[col]):
                    if row < boundary_idx:
                        new_rock_positions.append((boundary_idx-last_free_indices[col][i], col))
                        last_free_indices[col][i] += 1
                        break
  
        return tuple(sorted(new_rock_positions))

    def cycle_n_times(self, n: int, rock_positions: tuple[tuple[int, int]]) -> tuple[tuple[int, int]]:
        """
        Repeats a cycle, meaning tiling the platform first to the north, then west, south, and east
        n times. Returns the positions of the rocks after these n times. Uses cycle detection to shorten
        runtime

        :param n: The amount of times to repeat the cycle
        :param rock_positions: The positions of the rocks before tiling. Each position consits of (row, col)
        """
        known_rock_positions = {}
        rock_positions = tuple(sorted((rock_positions)))
        cycle_start = 0
        cycle_start_rocks = None
        
        for i in range(n):
            if rock_positions in known_rock_positions:
                cycle_start_rocks = rock_positions
                cycle_start = i
                break
            else:
                new_rock_positions = self.tile(rock_positions, self.TILE_DIRECTION.TOP)
                new_rock_positions = self.tile(new_rock_positions, self.TILE_DIRECTION.LEFT)
                new_rock_positions = self.tile(new_rock_positions, self.TILE_DIRECTION.BOT)
                new_rock_positions = self.tile(new_rock_positions, self.TILE_DIRECTION.RIGHT)
                known_rock_positions[rock_positions] = new_rock_positions
                rock_positions = new_rock_positions
        
        if cycle_start_rocks:
            cycle_len = 1
            curr_rocks = known_rock_positions[cycle_start_rocks]
            while curr_rocks != cycle_start_rocks:
                curr_rocks = known_rock_positions[curr_rocks]
                cycle_len += 1
            
            remaining_steps = (n - cycle_start) % cycle_len
            for i in range(remaining_steps):
                rock_positions = known_rock_positions[rock_positions]
      
        return rock_positions

    def calc_load_on_north(self, rock_positions: tuple[tuple[int, int]]) -> int:
        """
        Returns the total load on the north boundary by summing up all the loads
        of the rocks, where the load of one rock is determined by its distance to the south boundary

        :param rock_positions: The positions of the rocks, that determine the total load.
                               Each position consits of (row, col)
        """
        load = 0
        for pos in rock_positions:
            load += (self.height - pos[0])  
        return load

if __name__ == "__main__":
    with open("input.txt") as fp:
        map = []
        while line := fp.readline():
            map.append(list(line.strip()))

        reflector_dish = ReflectorDish(map)
        p1_load, p2_load = reflector_dish.execute_tiling_and_get_loads()
        print(f"Part 1 Result: {p1_load}")
        print(f"Part 2 Result: {p2_load}")