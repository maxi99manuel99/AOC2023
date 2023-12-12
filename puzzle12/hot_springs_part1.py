import itertools
import numpy as np
import numpy.typing as npt

class HotSpringRow():
    def __init__(self, springs: list[str], damaged_groups: list[int]) -> None:
        springs = np.array(springs)
        self.damaged_indices = np.where(springs == "#")[0]
        self.unknown_indices = np.where(springs == "?")[0]
        self.damaged_groups = damaged_groups
        self.missing_damages = sum(damaged_groups) - len(self.damaged_indices) 
        self.count_valid_arrangements()
    
    def get_possible_arrangements(self) -> list[tuple[int]]:
        return itertools.combinations(self.unknown_indices, r=self.missing_damages)

    def check_valid_arrangement(self, new_damaged_indices: npt.NDArray) -> bool:
        next_idx = 0
        for n in self.damaged_groups:
            if next_idx + n > len(new_damaged_indices):
                return False
            for i in range(next_idx, next_idx+n):
                if i == next_idx + n - 1:
                    if next_idx + n < len(new_damaged_indices) and new_damaged_indices[i]+1 == new_damaged_indices[i+1]:
                        return False
                else:
                    if new_damaged_indices[i]+1 != new_damaged_indices[i+1]:
                        return False
            next_idx += n
        return True
    
    def count_valid_arrangements(self) -> int:
        count = 0
        for arrangement in self.get_possible_arrangements():
            new_damaged_indices = np.concatenate((self.damaged_indices, list(arrangement)))
            new_damaged_indices.sort()
            if self.check_valid_arrangement(new_damaged_indices):
                count += 1
        return count
        
if __name__ == "__main__":
    with open("input.txt") as fp:
        total_arrangements = 0
        while line := fp.readline():
            springs, groups = line.split()
            springs = list(springs)
            groups = [int(x) for x in groups.split(",")]
            row = HotSpringRow(springs, groups)
            total_arrangements += row.count_valid_arrangements()
        print(f"Result Part 1: {total_arrangements}")