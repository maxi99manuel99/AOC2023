from dataclasses import dataclass
import copy


@dataclass
class Part():
    x: int
    m: int
    a: int
    s: int

    def sum(self) -> int:
        """
        Returns the sum of all the variables of a part
        """
        return self.x + self.m + self.a + self.s


def process_instructions(part: Part, instructions: str) -> str:
    """
    Takes the instruction string of a workflow and iterates through its instructions
    until an instruction is found whichs condition is true. Returns the 
    name of the new workflow to be executed

    :param part: the part we are processing
    :param instructions: the instruction string of a worklow
    """
    instructions = instructions.split(",")
    for instruction in instructions:
        if not ":" in instruction:
            return instruction
        else:
            condition, next_workflow = instruction.split(":")
            if eval("part." + condition):
                return next_workflow


def sum_rating_accepted_parts(workflow_dict: dict[int, str], input_parts: list[Part]) -> int:
    """
    Passes each part through the workflows resulting in an acceptence of the part or 
    a rejection. Returns the sum of all variables of all parts that are accepted

    :param workflow_dict: holds all the workflows with name and instruction string
    :param input_parts: All the parts to be processed
    """
    sum = 0
    for part in input_parts:
        workflow_name = "in"
        while workflow_name != "A" and workflow_name != "R":
            workflow_name = process_instructions(
                part, workflow_dict[workflow_name])
        if workflow_name == "A":
            sum += part.sum()

    return sum


def possible_accepted(workflow_dict: dict, curr_workflow: str, curr_ranges: list[dict[str, tuple[int, int]]]) -> list[dict[str, tuple[int, int]]]:
    """
    Recursively calculates combinations of accepted ranges for all variables of parts (x, m, a, s)
    by recursing through the given worflows. Returns a list of all of these combinations

    :param workflow_dict: holds all the workflows with name and instruction string
    :param curr_workflow: the current workflow in the recursion
    :param curr_ranges: holds the current range for all variables in the recursion
    """
    if curr_workflow == "A":
        return [curr_ranges]
    elif curr_workflow == "R":
        return []

    accepted_ranges = []
    instructions = workflow_dict[curr_workflow].split(",")

    for instruction in instructions:
        if ":" not in instruction:
            accepted_ranges += possible_accepted(
                workflow_dict, instruction, curr_ranges)
        else:
            condition, next_workflow = instruction.split(":")
            var, comparator, count = condition[0], condition[1], int(
                condition[2:])
            new_ranges = copy.deepcopy(curr_ranges)
            if comparator == ">":
                if curr_ranges[var][1] <= count:
                    continue
                curr_ranges[var][1] = count
                new_ranges[var][0] = max(count+1, new_ranges[var][0])
                accepted_ranges += possible_accepted(
                    workflow_dict, next_workflow, new_ranges)
            else:
                if curr_ranges[var][0] >= count:
                    continue
                curr_ranges[var][0] = count
                new_ranges[var][1] = min(count-1, curr_ranges[var][1])
                accepted_ranges += possible_accepted(
                    workflow_dict, next_workflow, new_ranges)

    return accepted_ranges


def sum_possible_combinations(accepted_ranges: list[dict[str, tuple[int, int]]]) -> int:
    """
    Takes a list of possible combinations of ranges, that lead to accepted parts
    and returns the total count of possible combinations of variables based 
    on the ranges

    :param accepted_ranges: holds combinations of ranges that lead to an accepted part
    """
    total_possible_combinations = 0
    for ranges in accepted_ranges:
        possible_combinations = 1
        for var in ranges.keys():
            min, max = ranges[var]
            possible_combinations *= (max - min + 1)
        total_possible_combinations += possible_combinations

    return total_possible_combinations


if __name__ == "__main__":
    workflow_dict = {}
    input_parts = []

    with open("input.txt") as fp:
        is_input = False
        while line := fp.readline():
            if len(line.strip()) == 0:
                is_input = True
            elif not is_input:
                name, instructions = line.strip().split("{")
                instructions = instructions[:-1]
                workflow_dict[name] = instructions
            else:
                values = line.strip()[1:-1].split(",")
                values = [val[2:] for val in values]
                part = Part(x=int(values[0]), m=int(
                    values[1]), a=int(values[2]), s=int(values[3]))
                input_parts.append(part)

    print(
        f"Part 1 Result: {sum_rating_accepted_parts(workflow_dict, input_parts)}")
    curr_ranges = {"x": [1, 4000], "m": [
        1, 4000], "a": [1, 4000], "s": [1, 4000]}
    accepted_ranges = possible_accepted(workflow_dict, "in", curr_ranges)
    print(f"Part 2 Result: {sum_possible_combinations(accepted_ranges)}")
