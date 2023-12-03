import numpy as np


SYMBOLS = ["*", "%", "/", "+", "=", "@", "#", "$", "-", "&"]

class Row():
    def __init__(self, row_string: str) -> None:
        self.previous_row: Row = None
        self.next_row: Row = None
        self.row_string: str = row_string
        self.numbers_with_postions: list[tuple[int, tuple[int, int]]] = []
        self.symbol_positions: list[int] = []
        self.star_positions: list[int] = []
        self.initialize_number_and_symbol_indices()

    def get_symbol_positions(self):
        return self.symbol_positions
    
    def get_numbers_with_positions(self): 
        return self.numbers_with_postions

    def initialize_number_and_symbol_indices(self) -> None:
        """
        Creates a list of indices of all symbols in this row as well as a list
        of tuples of all integers in this row with their start and end index
        """
        currently_int = False
        current_int_start = 0
        current_int_str = ""

        for idx, char in enumerate(self.row_string):
            if char.isdigit():
                current_int_str += char
                if not currently_int:
                    current_int_start = idx
                    currently_int = True

            elif currently_int:
                self.numbers_with_postions.append(
                    (int(current_int_str), (current_int_start, current_int_start+len(current_int_str))))
                currently_int = False
                current_int_start = 0
                current_int_str = ""

            if char in SYMBOLS:
                self.symbol_positions.append(idx)
                if char == "*":
                    self.star_positions.append(idx)

    def get_symbols_of_neighbors(self) -> list:
        """
        Returns a list of symbol positions of the rows neighbor rows
        """
        symbol_positions = []

        if self.next_row:
            symbol_positions += self.next_row.get_symbol_positions()
        if self.previous_row:
            symbol_positions += self.previous_row.get_symbol_positions()
        
        return symbol_positions
    
    def get_numbers_of_neighbors(self) -> list:
        """
        Returns a list of numbers with their position of the rows neighbor rows
        """
        numbers_with_positions = []

        if self.next_row:
            numbers_with_positions += self.next_row.get_numbers_with_positions()
        if self.previous_row:
            numbers_with_positions += self.previous_row.get_numbers_with_positions()
        
        return numbers_with_positions

    def sum_valid_numbers_of_row(self) -> int:
        """
        Returns the sum of all numbers in this row that are adjacent to a symbol
        """
        symbol_indices_to_check = self.symbol_positions.copy()
        symbol_indices_to_check += self.get_symbols_of_neighbors()

        sum = 0
        for number, (start_idx, end_idx) in self.numbers_with_postions:
            if len(np.intersect1d(np.arange(start_idx-1, end_idx+1), np.array(symbol_indices_to_check))) > 0:
                sum += number
        return sum
    
    def calculate_gear_ratio(self) -> int:
        """
        Returns the gear ratio of this row. This means: 
        For each "*" in the row with exactly two neighboring numbers
        calculates the product and sums these products.
        """
        numbers_to_check = self.numbers_with_postions.copy()
        numbers_to_check += self.get_numbers_of_neighbors()

        sum = 0
        for star_pos in self.star_positions:
            adjacent_numbers = []
            for number, (start_idx, end_idx) in numbers_to_check:
                if star_pos in np.arange(start_idx-1, end_idx+1):
                    adjacent_numbers.append(number)
                    if len(adjacent_numbers) > 2:
                        break

            if len(adjacent_numbers) == 2:
                sum += adjacent_numbers[0] * adjacent_numbers[1]
        
        return sum


def sum_over_valid_row_numbers(start_row: Row) -> int:
    """
    Iterates over all Row objects and returns a sum over all valid numbers of all rows
    """
    sum = start_row.sum_valid_numbers_of_row()
    row = start_row
    while row := row.next_row:
        sum += row.sum_valid_numbers_of_row()

    return sum

def sum_over_row_gear_ratios(start_row: Row) -> int:
    """
    Returns the sum of all gear ratios of all rows
    """
    sum = start_row.calculate_gear_ratio()
    row = start_row
    while row := row.next_row:
        sum += row.calculate_gear_ratio()

    return sum        

if __name__ == "__main__":
    previous_row = None
    with open("input.txt") as fp:
        first_line = fp.readline()
        first_row = Row(first_line)
        previous_row = first_row

        while line := fp.readline():
            row = Row(line)
            row.previous_row = previous_row
            previous_row.next_row = row
            previous_row = row

    print(f"Result Part 1: {sum_over_valid_row_numbers(first_row)}")
    print(f"Result Part 2: {sum_over_row_gear_ratios(first_row)}")
