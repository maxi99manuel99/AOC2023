class HistoryAnalyser():
    def __init__(self, start_sequence: list[int]) -> None:
        self.sequences = [start_sequence]

    def build_seuqence_tree(self) -> None:
        """
        creates new sequences in a tree like manner,
        by taking the difference of each neighboring pair in each sequence
        to create a new sequence until the all the leafs are zero
        (actual data structure is just a list of sequences)
        """
        curr_sequence = self.sequences[0]

        while not all(x == 0 for x in curr_sequence):
            curr_sequence = [(curr_sequence[i+1] - curr_sequence[i]) for i in range(len(curr_sequence)-1)]
            self.sequences.append(curr_sequence)

    def predict_next_value(self) -> int:
        """
        Extrapolates and returns the next value of the sequence 
        by adding the last values of each sequence in the sequence "tree"
        """
        return sum(seq[-1] for seq in self.sequences)
    
    def predict_previous_value(self) -> int:
        """
        Extrapolates and returns the previous value of the sequence 
        by substracting from the first value of each sequence in the
        sequence "tree" starting from the leaf sequence
        """
        current_sub = 0
        for seq in reversed(self.sequences):
            current_sub = seq[0] - current_sub
        return current_sub

if __name__ == "__main__":
    sum_pred_next_values = 0
    sum_pred_previous_values = 0
    
    with open("input.txt") as fp:
        while line:= fp.readline():
            sequence = [int(x) for x in line.split()]
            history_analyser = HistoryAnalyser(sequence)
            history_analyser.build_seuqence_tree()
            sum_pred_next_values += history_analyser.predict_next_value()
            sum_pred_previous_values += history_analyser.predict_previous_value()

    print(f"Part 1 Result: {sum_pred_next_values}")
    print(f"Part 2 Result: {sum_pred_previous_values}")