from functools import cache
import numpy as np


class ReflectorDish():
    def __init__(self, map: list[list[str]]) -> None:
        self.map = np.array(map)
        self.height, self.width = self.map.shape
        self.row_boundaries = self.get_row_boundaries()
        self.col_boundaries = self.get_col_boundaries()
        self.rock_positions = np.where(self.map == "O")
        self.rock_positions = tuple([((idx1, idx2)) for idx1, idx2 in zip(self.rock_positions[0], self.rock_positions[1])])
        new_rock_positions_p1 = self.tile(self.rock_positions, "top")
        print(f"Part 1 Result: {self.calc_load_on_north(new_rock_positions_p1)}")
        new_rock_positions_p2 = self.cycle_n_times(1000000000, self.rock_positions)
        print(f"Part 2 Result: {self.calc_load_on_north(new_rock_positions_p2)}")

    def get_row_boundaries(self):
        row_boundaries = []
        for row in self.map:
            boundary = [-1]
            boundary += list(np.where(row == "#")[0])
            boundary.append(self.width)
            row_boundaries.append(boundary)
        return row_boundaries
    
    def get_col_boundaries(self):
        col_boundaries = []
        for col in self.map.transpose():
            boundary = [-1]
            boundary += list(np.where(col == "#")[0])
            boundary.append(self.height)
            col_boundaries.append(boundary)
        return col_boundaries

    @cache
    def tile(self, rock_positions: tuple[tuple[int, int]], direction: str) -> tuple[tuple[int, int]]:
        new_rock_positions = []
        
        if direction == "left":
            boundaries = self.row_boundaries
            last_free_indices = [[1]*len(boundary) for boundary in boundaries] 
            for rock_pos in rock_positions:
                row, col = rock_pos

                for i, boundary_idx in enumerate(boundaries[row][::-1]):
                    if col > boundary_idx:
                        new_rock_positions.append((row, boundary_idx+last_free_indices[row][len(boundaries[row])-1-i]))
                        last_free_indices[row][len(boundaries[row])-1-i] += 1
                        break
    
        elif direction == "right":
            boundaries = self.row_boundaries
            last_free_indices = [[1]*len(boundary) for boundary in boundaries] 
            for rock_pos in rock_positions:
                row, col = rock_pos

                for i, boundary_idx in enumerate(boundaries[row]):
                    if col < boundary_idx:
                        new_rock_positions.append((row, boundary_idx-last_free_indices[row][i]))
                        last_free_indices[row][i] += 1
                        break

        elif direction == "top":
            boundaries = self.col_boundaries
            last_free_indices = [[1]*len(boundary) for boundary in boundaries] 
            for rock_pos in rock_positions:
                row, col = rock_pos

                for i, boundary_idx in enumerate(boundaries[col][::-1]):
                    if row > boundary_idx:
                        new_rock_positions.append((boundary_idx+last_free_indices[col][len(boundaries[col])-1-i], col))
                        last_free_indices[col][len(boundaries[col])-1-i] += 1
                        break

        elif direction == "bot":
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
        known_rock_positions = {}
        rock_positions = tuple(sorted((rock_positions)))
        for i in range(n):
            if rock_positions in known_rock_positions:
                rock_positions = known_rock_positions[rock_positions]
            else:
                new_rock_positions = self.tile(rock_positions, "top")
                new_rock_positions = self.tile(new_rock_positions, "left")
                new_rock_positions = self.tile(new_rock_positions, "bot")
                new_rock_positions = self.tile(new_rock_positions, "right")
                known_rock_positions[rock_positions] = new_rock_positions
                rock_positions = new_rock_positions
        return rock_positions

    def calc_load_on_north(self, rock_positions: tuple[tuple[int, int]]) -> int:
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
    
