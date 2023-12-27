from random import choice


def kargers_until_min_cut(orig_edges: set[tuple[str, str]], num_unique_vertices: int, num_edges_to_cut: int):
    """
    Uses karges algorith to find cut sets of edges that split the graph into two connected components
    Repeats karges until a cut is found that cuts exactly num_edges_to_cut edges. Then returns 
    the product of the amount of elements in each of the two connected components

    :param orig_edges: Contains all edges in the graph
    :param num_unique_vertices: the number of vertices in the graph
    :param num_edges_to_cut: the number of edges our cut should have
    """
    cut_edge_count = 0

    while cut_edge_count != num_edges_to_cut:
        edges = list(orig_edges)
        contracted_nodes = {}

        for _ in range(num_unique_vertices-2):
            contract_from, contract_into = choice(edges)
            contracted_nodes.setdefault(
                contract_into, set()).add(contract_from)
            if contract_from in contracted_nodes:
                contracted_nodes[contract_into].update(
                    contracted_nodes.pop(contract_from))

            new_edges = []
            for node1, node2 in edges:
                new_edge = (node1, node2)
                if node1 == contract_from:
                    new_edge = (contract_into, node2)
                elif node2 == contract_from:
                    new_edge = (node1, contract_into)

                if new_edge[0] != new_edge[1]:
                    new_edges.append(new_edge)
            edges = new_edges

        cut_edge_count = len(edges) // 2

    result = 1
    for final_node in contracted_nodes.keys():
        result *= len(contracted_nodes[final_node])+1

    return result


if __name__ == "__main__":
    edges = set()
    unique_nodes = set()

    with open("input.txt") as fp:
        while line := fp.readline():
            key, connections = line.strip().split(": ")
            unique_nodes.add(key)
            connections = connections.split()
            for connection in connections:
                edges.add((key, connection))
                edges.add((connection, key))
                unique_nodes.add(connection)

    print(
        f"Part 1 Result: {kargers_until_min_cut(edges, len(unique_nodes), 3)}")
