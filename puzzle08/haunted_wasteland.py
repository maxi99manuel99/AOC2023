import math


class NodeNeighbors():
    def __init__(self, left: str, right: str) -> None:
        self.left = left
        self.right = right


def count_steps_to_goal(start: str, goal: str, instruction_string: str, node_dict: dict[str, NodeNeighbors]) -> int:
    """
    Returns the steps needed to traverse node_dict from start to goal, following the instructions from the 
    instruction_string

    :param start: The start node
    :param goal: Either has len 1, meaning that we want to search for any goal node
                ending with the goal str, or represents a whole node
    :param instruction_string: The steps that one should take to reach the goal. Only
                contains "L" for left and "R" for right
    :param node_dict: contains all nodes and their as keys and their neighbors als values
    """
    steps = 0
    current_node = start
    slice_goal = -1 if len(goal) == 1 else 0
    while True:
        for instruction in instruction_string:
            if current_node[slice_goal:] == goal:
                return steps
            if instruction == "L":
                current_node = node_dict[current_node].left
            else:
                current_node = node_dict[current_node].right
            steps += 1


if __name__ == "__main__":
    node_dict = {}
    nodes_ending_on_A = []
    with open("input.txt") as fp:
        instructions = fp.readline().strip()
        fp.readline()
        while line := fp.readline():
            current_node, next_nodes = line.split(" = (")
            if current_node[-1] == "A":
                nodes_ending_on_A.append(current_node)
            next_nodes = next_nodes.replace(")", "")
            left, right = next_nodes.strip().split(", ")

            next_nodes = NodeNeighbors(left, right)
            node_dict[current_node] = next_nodes

        print(
            f"Part 1 Result {count_steps_to_goal(start='AAA',goal='ZZZ', instruction_string=instructions, node_dict=node_dict)}")
        steps_for_all_a = [count_steps_to_goal(
            start=node, goal="Z", instruction_string=instructions, node_dict=node_dict) for node in nodes_ending_on_A]
        print(f"Part 2 Result {math.lcm(*steps_for_all_a)}")
