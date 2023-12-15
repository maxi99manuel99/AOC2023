def holiday_ASCII_string_helper(string: str) -> int:
    """
    Computes has values in the range of 0 to 255 for a given string

    :param string: the string to calculate the hash of
    """
    string_value = 0
    for c in string:
        string_value = (string_value + ord(c)) * 17 % 256
    return string_value


def sum_hashs(strings: list[str]) -> int:
    """
    sums up all the hashs of the given list of strings

    :param strings: contains all strings to be hashed and summed
    """
    return sum(holiday_ASCII_string_helper(string) for string in strings)


def sum_focusing_power(strings: list[str]) -> int:
    """
    Calculates the tocal focusing power of all lenses

    :param strings: Each string represents a label and a operation
    """
    HASHMAP = {}
    for string in strings:
        label = ""
        for i, c in enumerate(string):
            if c.isalpha():
                label += c
            else:
                label_end = i
                break

        operation = string[label_end:]
        key = holiday_ASCII_string_helper(label)

        box = HASHMAP.get(key, [])
        is_inside = False
        for i, lens in enumerate(box):
            if lens[0] == label:
                idx = i
                is_inside = True

        if operation[0] == "=":
            if is_inside:
                box[idx] = (label, int(operation[1]))
            else:
                box.append((label, int(operation[1])))
            HASHMAP[key] = box
        else:
            if is_inside:
                del box[idx]
                HASHMAP[key] = box

    sum_power = 0
    for box_num in HASHMAP.keys():
        box_power = box_num+1
        for pos, (lens, focal_length) in enumerate(HASHMAP[box_num]):
            sum_power += box_power * (pos+1) * focal_length
    return sum_power


if __name__ == "__main__":
    with open("input.txt") as fp:
        strings = fp.read().strip().split(",")
        print(f"Part 1 Result: {sum_hashs(strings)}")
        print(f"Part 2 Result: {sum_focusing_power(strings)}")
