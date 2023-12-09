class HistoryAnalyser():
    def __init__(self, start_sequence: list[int]) -> None:
        self.sequences = [start_sequence]

    def build_seuqence_tree(self):
        curr_sequence = self.sequences[0]

        while not all(x == 0 for x in curr_sequence):
            curr_sequence = [(curr_sequence[i+1] - curr_sequence[i]) for i in range(len(curr_sequence)-1)]
            self.sequences.append(curr_sequence)
        

    def predict_next_value(self) -> int:
        reversed_sequences = list(reversed(self.sequences))
        reversed_sequences[0].append(0)
        for i, seq in enumerate(reversed_sequences[1:]):
            reversed_sequences[i+1].append(seq[-1] + reversed_sequences[i][-1])

        return reversed_sequences[-1][-1]
    
    def predict_previous_value(self) -> int:
        reversed_sequences = list(reversed(self.sequences))
        reversed_sequences[0].append(0)
        for i, seq in enumerate(reversed_sequences[1:]):
            reversed_sequences[i+1].insert(0, seq[0] - reversed_sequences[i][0])
       
        return reversed_sequences[-1][0]

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