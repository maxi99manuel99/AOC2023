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
        "J": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "T": 10,
        "Q": 11,
        "K": 12,
        "A": 13
    }

    def __init__(self, hand: str, bid: int) -> None:
        self.hand = np.array([*hand])
        self.initialize_primary_score()
        self.initialize_secondary_score()
        self.bid = bid

    def replace_J_optimal(self, card_values: list[int], counts: list[int]) -> tuple[list[int], list[int]]:
        """
        Returns a list of card values and counts after replacing J with the maximum
        occuring card_value of all other values

        :param card_values: The card values before replacement
        :param counts: The counts before replacement
        """
        J_idx = card_values.index("J")
        J_count = counts[J_idx]

        del card_values[J_idx]
        del counts[J_idx]

        best_convertion_idx = max(
            enumerate(counts), key=lambda x: x[1])[0]

        counts[best_convertion_idx] += J_count
        return card_values, counts

    def initialize_primary_score(self):
        """
        Calculates the primary score of this hand by using the function replace_J_optimal to replace
        the Joker J and counting occurances of unique card types
        """
        before_card_values, before_counts = np.unique(
            self.hand, return_counts=True)

        if "J" in self.hand and len(before_counts) != 1:
            _, counts = self.replace_J_optimal(
                list(before_card_values), list(before_counts))
        else:
            _, counts = before_card_values, before_counts

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
        # by multiplying all values at their positions in the reversely
        # ordered list with 10^(*2) we ensure that a hand with a 
        # bigger value at pos 0 will always win over all hands with 
        # lower values at pos 0. Same goes for pos 1, 2, 3, 4
        score = 0
        for i, value in enumerate(hand[::-1]):
            score += value * pow(10, i*2)

        self.secondary_score = score


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

    print(f"Part 2 Result: {calculate_winnings_sum(all_hands)}")
