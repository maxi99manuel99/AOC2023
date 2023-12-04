import numpy as np

class Scratchcard(): 
    def __init__(self, card_string: str) -> None:
        winning_string, drawn_string = card_string.split("|")
        self.winning_numbers, self.drawn_numbers = np.array(winning_string.split(), int), np.array(drawn_string.split(), int)
    
    def calculate_num_winnings_and_points(self) -> (int, int):
        """
        Returns the count of winning numbers of this Scratchcard and the points
        it is worth
        """
        num_intersects = len(np.intersect1d(self.winning_numbers, self.drawn_numbers))
        return  num_intersects, int(2**(num_intersects-1))

if __name__ == "__main__":
    
    with open("input.txt") as fp:
        copies_per_card = {}
        point_sum = 0
        total_cards = 0
        card_idx = 0
        while line:= fp.readline():
            sratch_card = Scratchcard(line.split(":")[1])
            num_winnings, points = sratch_card.calculate_num_winnings_and_points()
            point_sum += points
            num_this_card = 1 + copies_per_card.get(card_idx, 0)
            for i in range(1, num_winnings+1):
                copies_per_card[card_idx+i] = copies_per_card.get(card_idx+i, 0) + num_this_card
            total_cards  += num_this_card
            card_idx += 1
        print(f"Part 1 Result: {point_sum}")
        print(f"Part 2 Resulst: {total_cards}")
            