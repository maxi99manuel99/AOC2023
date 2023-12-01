
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
    Iterates through list of calibration strings and replaces the second index of a string 
    of a digit with its actual digit (e.g. one -> o1e).

    :param calibration_strings: the list of calibration strings
    """

    for i, line in enumerate(calibration_strings):
        for digit_string in DIGIT_STRING_TO_INT.keys():
            while second_indx := line.find(digit_string)+1:
                if second_indx == 0:
                    break
                line = line[:second_indx] + DIGIT_STRING_TO_INT[digit_string] + line[second_indx + 1:]
        calibration_strings[i] = line
        


if __name__ == "__main__":
    sum = 0
    with open("input.txt") as fp:
        calibration_strings = fp.readlines()
        summed_calibration = sum_calibration_values(calibration_strings)
        print(f"Part1 result: {summed_calibration}")
        replace_digit_strings(calibration_strings)
        summed_calibration_after_replace = sum_calibration_values(calibration_strings)
        print(f"Part2 result: {summed_calibration_after_replace}")
