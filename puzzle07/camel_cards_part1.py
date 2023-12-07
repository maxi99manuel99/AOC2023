from enum import Enum
import numpy as np


class CamelHand():
    class SCORES(Enum):
        FIVE_OF_A_KIND = 7
        FOUR_OF_A_KIND = 6
        FULL_HOUSE = 5
        THREE_OF_A_KIND = 4
        TWO_PAIR = 3
        ONE_PAIR = 2
        HIGH_CARD = 1

    char_to_int = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14
    }

    def __init__(self, hand: str, bid: int) -> None:
        self.hand = np.array([*hand])
        self.initialize_primary_score()
        self.initialize_secondary_score()
        self.bid = bid

    def initialize_primary_score(self):
        """
        Calculates the primary score of this hand by counting occurances of 
        unique card types
        """
        _, counts = np.unique(self.hand, return_counts=True)
        n_unique_cards = len(counts)

        if n_unique_cards == 1:
            self.primary_score = self.SCORES.FIVE_OF_A_KIND

        elif n_unique_cards == 2:
            if 1 in counts:
                self.primary_score = self.SCORES.FOUR_OF_A_KIND
            else:
                self.primary_score = self.SCORES.FULL_HOUSE

        elif n_unique_cards == 3:
            if 3 in counts:
                self.primary_score = self.SCORES.THREE_OF_A_KIND
            else:
                self.primary_score = self.SCORES.TWO_PAIR

        elif n_unique_cards == 4:
            self.primary_score = self.SCORES.ONE_PAIR
        
        else:
            self.primary_score = self.SCORES.HIGH_CARD

    def initialize_secondary_score(self):
        """
        Initializes the secondary score of this hand which is based on the 
        card value at every position of this hand
        """
        hand = [self.char_to_int[card] for card in self.hand]
        # use weights that ensure that a hand with a bigger value at pos 0
        # will always win over all hands with lower values at pos 0
        # same goes for pos 1, 2, 3, 4
        weights = [100000, 1000, 10, 0.1, 0.001, 0.00001]
        self.secondary_score = sum(
            val * weight for val, weight in zip(hand, weights))


def calculate_winnings_sum(hands: list[CamelHand]) -> int:
    """
    Sorts all hands by scores and then calculates the winnings for each
    card and returns a sum of all winnings

    :param hands: contains the hands to determine the winnings of
    """
    sorted_hands = sorted(hands, key=lambda x: (
        x.primary_score.value, x.secondary_score))
    bid_sum = 0
    for i, hand in enumerate(sorted_hands):
        bid_sum += (i+1)*hand.bid
    
    return bid_sum


if __name__ == "__main__":
    all_hands: list[CamelHand] = []
    
    with open("input.txt") as fp:
        while line := fp.readline():
            hand, bid = line.split()
            bid = int(bid)
            all_hands.append(CamelHand(hand, bid))
    
    print(f"Part 1 Result: {calculate_winnings_sum(all_hands)}")
