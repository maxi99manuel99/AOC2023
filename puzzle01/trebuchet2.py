import numpy as np

DIGIT_STRING_TO_INT = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

DIGIT_STRING_TO_INT_REVERSED = {
    "eno": "1",
    "owt": "2",
    "eerht": "3",
    "ruof": "4",
    "evif": "5",
    "xis": "6",
    "neves": "7",
    "thgie": "8",
    "enin": "9",
}

def sum_calibration_values(calibration_strings: list[str]) -> int:
    """
    Extracts calibration value from each line in a list of calibration document strings
    and sums these values

    :param calibration_strings: the list of calibration strings
    :return: sum of all calibration values extracted from the strings
    """
    sum = 0
    for line in calibration_strings:
        extracted_digits = [x for x in line if x.isdigit()]
        calibration_value = int(extracted_digits[0] + extracted_digits[-1])
        sum += calibration_value

    return sum


def replace_digit_strings(calibration_strings: list[str]) -> None:
    """
    Iterates through list of calibration strings and replaces the first and last found
    string of a digit 

    :param calibration_strings: the list of calibration strings
    """

    for i, line in enumerate(calibration_strings):
        
        first_idx_string = np.inf
        first_digit_string = ""
        last_idx_string = -np.inf
        last_digit_string = ""
        
        first_idx_string, first_digit_string = min(((line.find(sub), sub) for sub in DIGIT_STRING_TO_INT.keys() if sub in line), default=(-1, None))
        last_idx_string, last_digit_string = max(((len(line) - line[::-1].find(sub) - len(sub), sub) for sub in DIGIT_STRING_TO_INT_REVERSED.keys() if sub in line[::-1]), default=(-1, None))
            
        if first_digit_string:
            calibration_strings[i] = line[:first_idx_string] + DIGIT_STRING_TO_INT[first_digit_string] + line[first_idx_string + 1: last_idx_string] + DIGIT_STRING_TO_INT_REVERSED[last_digit_string] + line[last_idx_string + 1:]

if __name__ == "__main__":
    sum = 0
    with open("input.txt") as fp:
        calibration_strings = fp.readlines()
        summed_calibration = sum_calibration_values(calibration_strings)
        print(f"Part1 result: {summed_calibration}")
        replace_digit_strings(calibration_strings)
        summed_calibration_after_replace = sum_calibration_values(calibration_strings)
        print(f"Part2 result: {summed_calibration_after_replace}")
