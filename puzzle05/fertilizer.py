import sys


class SeedRange():

    def __init__(self, range_start: int, range_len: int) -> None:
        self.start = range_start
        self.end = range_start + (range_len - 1)


class ConvertionRange():

    def __init__(self, destination_range_start: int, source_range_start: int, range_len: int) -> None:
        self.dest_start = destination_range_start
        self.src_start = source_range_start
        self.dest_end = destination_range_start + (range_len - 1)
        self.src_end = source_range_start + (range_len - 1)


class ConvertionDict():

    def __init__(self, source: str, destination: str) -> None:
        self.source = source
        self.destination = destination
        self.possible_convertions: list[ConvertionRange] = []

    def initialize_convertion(self, convertion_strings: list[str]) -> None:
        """
        Initializes the possible conversions of this dict

        :param convertion_strings: The conversion rules as strings
        """
        for convertion_string in convertion_strings:
            split_conv = convertion_string.split()
            self.possible_convertions.append(ConvertionRange(
                int(split_conv[0]), int(split_conv[1]), int(split_conv[2])))


def get_new_rules_with_filled_gaps(convertion_dict: ConvertionDict, seed_range: SeedRange) -> list[ConvertionRange]:
    """
    Returns a new rule set based on the rule set of a given dict, that adds rules for the left out
    parts of the rulest and rules after and before the maximum and minimum source index of the ruleset
    if the SeedRange start index/end index is higher/smaller

    :param convertion_dict: The conversion dict, which's ruleset we want to append
    :param seed_range: SeedRange to add extra rules on the outer indices
    """
    convertion_rules: list[ConvertionRange] = sorted(
        convertion_dict.possible_convertions, key=lambda x: x.src_start)
    new_rules: list[ConvertionRange] = []
    if seed_range.start < convertion_rules[0].src_start:
        new_rules.append(ConvertionRange(seed_range.start, seed_range.start,
                         convertion_rules[0].src_start - seed_range.start))
    if seed_range.end > convertion_rules[-1].src_end:
        new_rules.append(ConvertionRange(
            convertion_rules[-1].src_end, convertion_rules[-1].src_end, seed_range.end - convertion_rules[-1].src_end))

    for i, rule in enumerate(convertion_rules[:-1]):
        if convertion_rules[i].src_end + 1 != convertion_rules[i+1].src_start:
            new_rules.append(ConvertionRange(convertion_rules[i].src_end + 1,
                                             convertion_rules[i].src_end + 1,
                                             convertion_rules[i+1].src_start - convertion_rules[i].src_end + 1))
    return convertion_rules + new_rules


def calculate_locations(initial_seeds: list[int], convertion_dicts: list[ConvertionDict]) -> list[int]:
    """
    Traverses a list of convertion dicts and performs every conversion until arriving at the location for each
    initial seed. Returns a list of these locations

    :param initial_seeds: The initial seeds that need to be converted
    :param convertion_dicts: List of ConvertionDict objects (which contain the rules)
    """
    locations: list[int] = []
    for source in initial_seeds:
        for convertion_dict in convertion_dicts:
            for posible_convertion in convertion_dict.possible_convertions:
                if posible_convertion.src_start <= source <= posible_convertion.src_end:
                    dest = posible_convertion.dest_start + \
                        (source - posible_convertion.src_start)
                    source = dest
                    break
        locations.append(source)
    return locations


def calculate_range_convertion(seed_range: SeedRange, convertion_rules: list[ConvertionRange]) -> list[SeedRange]:
    """
    Converts a given SeedRange into new SeedRanges based on the rules given

    :param seed_range: the SeedRange to be converted
    :param convertion_rules: the rules to be used for convertion
    """
    new_ranges = []
    for convertion_range in convertion_rules:

        if seed_range.end < convertion_range.src_start or seed_range.start > convertion_range.src_end:
            continue

        new_start = max(seed_range.start, convertion_range.src_start)
        new_end = min(seed_range.end, convertion_range.src_end)

        dest_start = convertion_range.dest_start + \
            (new_start - convertion_range.src_start)
        dest_end = convertion_range.dest_start + \
            (new_end - convertion_range.src_start)
        new_ranges.append(SeedRange(dest_start, dest_end - dest_start))

    return new_ranges


def calculate_locations_with_seed_pairs(seed_pairs: list[list[int]], convertion_dicts: list[ConvertionDict]) -> list[SeedRange]:
    """
    Takes a list of seed_pairs, converts them to SeedRanges and then 
    converts these into location ranges by iterating over  all ConvertionDicts and their rules.
    Returns a list of location ranges

    :param seed_pairs: seed range input, consisting of a list of seed start indices and the length of their range
    :param convertion_dicts: List of ConvertionDict objects (which contain the rules)
    """
    location_ranges = []
    source_seed_ranges = [SeedRange(pair[0], pair[1]) for pair in seed_pairs]
    for source in source_seed_ranges:
        current_ranges = [source]
        for convertion_dict in convertion_dicts:
            new_ranges = []
            for seed_range in current_ranges:
                updated_convertion_rules = get_new_rules_with_filled_gaps(
                    convertion_dict, seed_range)
                new_ranges += calculate_range_convertion(
                    seed_range, updated_convertion_rules)

            current_ranges = new_ranges
        location_ranges += current_ranges
    return location_ranges


if __name__ == "__main__":
    convertion_dicts: list[ConvertionDict] = []
    with open("input.txt") as fp:
        initial_seeds = fp.readline().split(":")[1].split()
        initial_seeds = [int(seed) for seed in initial_seeds]
        current_dict = None
        while line := fp.readline():
            if "map" in line:
                if current_dict:
                    current_dict.initialize_convertion(convertion_strings)
                    convertion_dicts.append(current_dict)
                split_source_dest = line.split("-")
                source, destination = split_source_dest[0], split_source_dest[2].split()[
                    0]
                current_dict = ConvertionDict(source, destination)
                convertion_strings = []
            elif line[0].isdigit():
                convertion_strings.append(line.strip())
        # append last dict
        current_dict.initialize_convertion(convertion_strings)
        convertion_dicts.append(current_dict)

    locations = calculate_locations(initial_seeds, convertion_dicts)
    min_location = min(locations)
    print(f"Part 1 Result: {min_location}")

    seed_pairs = [initial_seeds[x:x+2]
                  for x in range(0, len(initial_seeds), 2)]
    location_ranges = calculate_locations_with_seed_pairs(
        seed_pairs, convertion_dicts)
    min_location_pairs = min(location_ranges, key=lambda x: x.start).start
    print(f"Part 2 Result: {min_location_pairs}")
