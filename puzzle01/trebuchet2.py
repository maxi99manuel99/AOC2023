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
        for char in line:
            if char.isdigit():
                first_digit = char
                break;
        for char in reversed(line):
            if char.isdigit():
                last_digit = char
                break;
        calibration_value = int(first_digit + last_digit)
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
        
        for digit_string in DIGIT_STRING_TO_INT.keys():
            first_appearance = line.find(digit_string)
            if first_appearance == -1:
                continue
            elif first_appearance < first_idx_string:
                first_idx_string = first_appearance
                first_digit_string = digit_string
            

        for digit_string in DIGIT_STRING_TO_INT_REVERSED.keys():
            reverse_first_idx = line[::-1].find(digit_string)
            if reverse_first_idx == -1:
                continue
            last_appearance = len(line) - reverse_first_idx - len(digit_string)
            if last_appearance > last_idx_string:
                last_digit_string = digit_string

        if first_digit_string:
            calibration_strings[i] = line[:first_idx_string] + DIGIT_STRING_TO_INT[first_digit_string] + line[first_idx_string + 1:]
            calibration_strings[i] = line[:last_idx_string] + DIGIT_STRING_TO_INT_REVERSED[last_digit_string] + line[last_idx_string + 1:]


if __name__ == "__main__":
    sum = 0
    with open("input.txt") as fp:
        calibration_strings = fp.readlines()
        summed_calibration = sum_calibration_values(calibration_strings)
        print(f"Part1 result: {summed_calibration}")
        replace_digit_strings(calibration_strings)
        summed_calibration_after_replace = sum_calibration_values(calibration_strings)
        print(f"Part2 result: {summed_calibration_after_replace}")
