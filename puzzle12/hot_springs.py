from functools import cache


def get_remains_from_possible_positions(springs: str, group: int):
    """
    Finds possible positions for a group of given size and returns the remaining spring string
    if a group were to be placed at that position

    :param springs: The spring string in which we want to find possible positions for our group
    :param group: the size of the group we want to find positions for
    """
    remaining_springs = []
    i = 0
    while i < len(springs)-group:
        if "." not in springs[i:i+group] and springs[i+group] != "#":
            remaining_springs.append(springs[i+group+1:])
        if springs[i] == "#":
            break
        i += 1

    return remaining_springs


@cache
def count_valid_arrangements(springs: str, groups: tuple[int]) -> int:
    """
    For a given spring string and group sizes counts how many valid arrangements there are
    for the damaged strings by recursing over possible configurations

    :param springs: string of springs, of which we want to find out how many arramngements are possible
    :param groups: the group sizes of the contiguous damaged springs
    """
    if not groups:
        return "#" not in springs

    current_group = groups[0]
    sum = 0
    for remaining_spring in get_remains_from_possible_positions(springs, current_group):
        sum += count_valid_arrangements(remaining_spring, groups[1:])

    return sum


if __name__ == "__main__":
    with open("input.txt") as fp:
        total_arrangements = 0
        total_arrangements_unfolded = 0

        while line := fp.readline():
            springs, groups = line.split()
            springs_unfolded = springs + "?"
            springs_unfolded = springs_unfolded*5
            springs_unfolded = springs_unfolded[:-1] + "."
            springs = springs + "."
            groups = tuple(int(x) for x in groups.split(","))
            groups_unfolded = groups*5
            total_arrangements += count_valid_arrangements(springs, groups)
            total_arrangements_unfolded += count_valid_arrangements(
                springs_unfolded, groups_unfolded)

        print(f"Result Part 1: {total_arrangements}")
        print(f"Result Part 2: {total_arrangements_unfolded}")
