import numpy as np

SYMBOLS = ["*", "%", "/", "+", "=", "@", "#", "$", "-", "&"]


class Row():
    def __init__(self, row_string: str) -> None:
        self.previous_row = None
        self.next_row = None
        self.row_string = row_string
        self.numbers_with_postions = []
        self.symbol_positions = []
        self.initialize_number_and_symbol_indices()

    def get_symbol_positions(self):
        return self.symbol_positions

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

    def sum_valid_numbers_of_row(self) -> int:
        """
        Returns the sum of all numbers in this row that are adjacent to a symbol
        """
        symbol_indices_to_check = self.symbol_positions.copy()
        if self.next_row:
            symbol_indices_to_check += self.next_row.get_symbol_positions()
        if self.previous_row:
            symbol_indices_to_check += self.previous_row.get_symbol_positions()

        sum = 0
        for number, (start_idx, end_idx) in self.numbers_with_postions:
            if len(np.intersect1d(np.arange(start_idx-1, end_idx+1), np.array(symbol_indices_to_check))) > 0:
                sum += number
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
