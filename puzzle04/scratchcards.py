import numpy as np

class Scratchcard(): 
    def __init__(self, card_string: str) -> None:
        winning_string, drawn_string = card_string.split("|")
        self.winning_numbers, self.drawn_numbers = np.array(winning_string.split(), int), np.array(drawn_string.split(), int)
    
    def calculate_points(self) -> int:
        num_intersects = len(np.intersect1d(self.winning_numbers, self.drawn_numbers))
        return  int(2**(num_intersects-1))

if __name__ == "__main__":
    with open("input.txt") as fp:
        point_sum = 0
        while line:= fp.readline():
            sratch_card = Scratchcard(line.split(":")[1])
            point_sum += sratch_card.calculate_points()
        print(f"Part 1 Result: {point_sum}")
            