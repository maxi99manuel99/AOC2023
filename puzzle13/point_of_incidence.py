import math
class Pattern():
    def __init__(self, rows: list[str], cols: list[str]) -> None:
        self.rows = rows
        self.cols = cols

        self.is_row_reflection = True
        self.reflection_idx = self.get_reflection(self.cols)
        if not self.reflection_idx:
            self.is_row_reflection = False 
            self.reflection_idx = self.get_reflection(self.rows)[0]
        else:
            self.reflection_idx = self.reflection_idx[0]

        self.is_row_reflection_smudge = True
        self.reflection_idx_smudge = self.get_reflection_smudge(self.cols)
        if not self.reflection_idx_smudge:
            self.is_row_reflection_smudge = False 
            self.reflection_idx_smudge = self.get_reflection_smudge(self.rows)[0][0]
        else:
            self.reflection_idx_smudge = self.reflection_idx_smudge[0][0]
    
    def get_reflection(self, rows: list[str]) -> list[int]:
        """
        Returns the index of the point of perfect reflection for rows/cols if there is one
        else returns an empty list. (since the acutal point of reflection is always between two
        rows/col return the index of the latter row/col)

        :param rows: The rows/cols to find the point of perfect reflection for
        """
        possible_splits = []
        first_row = rows[0]

        for i in range(1, len(first_row)):
            split1, split2 = first_row[i:], first_row[:i]
            len_to_check = min(len(split1), len(split2))
            if split1[:len_to_check] == split2[-len_to_check:][::-1]:
                possible_splits.append(i)
       
        for other_row in rows[1:]:
            if not possible_splits:
                break
            for possible_split in possible_splits.copy():
                split1, split2 = other_row[possible_split:], other_row[:possible_split]
                len_to_check = min(len(split1), len(split2))
                if split1[:len_to_check] != split2[-len_to_check:][::-1]:
                    possible_splits.remove(possible_split)
        
        if len(possible_splits) > 1:
            print("There is more than 1 reflection possible, which can not be true")
        return possible_splits
    
    def get_reflection_smudge(self, rows: list[str]) -> list[int]:
        """
        Returns the index of the point of perfect reflection for rows/cols, after using exactly one smudge
        , if there is one else returns an empty list. (since the acutal point of reflection is always between two
        rows/col return the index of the latter row/col)

        :param rows: The rows/cols to find the point of perfect reflection for
        """
        possible_splits = []
        first_row = rows[0]

        for i in range(1, len(first_row)):
            split1, split2 = first_row[i:], first_row[:i]
            len_to_check = min(len(split1), len(split2))
            split1 = split1[:len_to_check]
            split2 = split2[-len_to_check:][::-1]
            
            if split1 == split2:
                possible_splits.append((i, False))
                continue

            if sum(split1[j] != split2[j] for j in range(len_to_check)) == 1:
                possible_splits.append((i, True))

        for other_row in rows[1:]:
            if not possible_splits:
                break

            for (possible_split, smudge_used) in possible_splits.copy():
                split1, split2 = other_row[possible_split:], other_row[:possible_split]
                len_to_check = min(len(split1), len(split2))
                split1 = split1[:len_to_check]
                split2 = split2[-len_to_check:][::-1]
                if split1 == split2:
                    continue
                
                possible_splits.remove((possible_split, smudge_used))
                if split1 != split2 and smudge_used:
                    continue
                
                if sum(split1[j] != split2[j] for j in range(len_to_check)) == 1:
                    possible_splits.append((possible_split, True))
        
        possible_splits = [possible_split for possible_split in possible_splits if possible_split[1]]
        if len(possible_splits) > 1:
            print("There is more than 1 reflection with smudge possible, which can not be true")
        return possible_splits


def reflections_sum(patterns: list[Pattern]) -> (int, int):
    """
    Returns a sum of the amount of rows/cols above/to the left of the reflection
    for all patterns. One sum for the version w/o smudges and one for the one with smudges

    :param patterns: contains all patterns from the input
    """
    sum = 0
    sum_smudge = 0
    for pattern in patterns:
        if pattern.is_row_reflection:
            sum += pattern.reflection_idx*100
        else:
            sum += pattern.reflection_idx
            
        if pattern.is_row_reflection_smudge:
            sum_smudge += pattern.reflection_idx_smudge*100
        else:
            sum_smudge += pattern.reflection_idx_smudge
    
    return sum, sum_smudge


if __name__ == "__main__":
    patterns = []
    with open("input.txt") as fp:
        rows = []
        while line:= fp.readline():
            if line in ['\n', '\r\n']:
                cols = list(map(list, zip(*rows)))
                cols = ["".join(col) for col in cols]
                patterns.append(Pattern(rows, cols))
                rows = []
            else:
                line = line.strip()
                rows.append(line)
        
        cols = list(map(list, zip(*rows)))
        cols = ["".join(col) for col in cols]
        patterns.append(Pattern(rows, cols))
        sum, sum_smudge = reflections_sum(patterns)
        print(f"Part 1 Result: {sum}")
        print(f"Part 2 Result: {sum_smudge}")


