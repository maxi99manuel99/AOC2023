from enum import Enum
class VerticalEdge():
    def __init__(self, top: tuple[int, int], bot: tuple[int, int]) -> None:
        self.top = top 
        self.bot = bot 
        self.next_y_index_to_check = top[0]

def count_number_holes(vertical_edges: list[VerticalEdge]):
    points_inside = set()
    vertical_edges.sort(key=lambda x: (x.top[1], x.top[0]))
    for idx, edge in enumerate(vertical_edges):
        while edge.next_y_index_to_check <= edge.bot[0]:
            for other_edge in vertical_edges[idx+1:]:
                if (edge.next_y_index_to_check >= other_edge.top[0]) and not (other_edge.bot[0] <= edge.next_y_index_to_check):
                    print(f"Edge: {edge.top} {edge.bot}")
                    print(f"y idx: {edge.next_y_index_to_check}")
                    print(f"Other Edge {other_edge.top} {other_edge.bot}")
                    horizontal_range = range(edge.top[1], other_edge.top[1]+1)
                    if other_edge.bot[0] < edge.bot[0]:
                        vertical_range = range(edge.next_y_index_to_check, other_edge.bot[0]+1)
                        edge.next_y_index_to_check = other_edge.bot[0]
                    else:
                        vertical_range = range(edge.next_y_index_to_check, edge.bot[0]+1)
                        edge.next_y_index_to_check = edge.bot[0]+1
                    other_edge.next_y_index_to_check = other_edge.bot[0]+1
                    
                    print(f"resulting Ranges: {(vertical_range.start, vertical_range.stop)}, {(horizontal_range.start, horizontal_range.stop)}")
                    for i in vertical_range:
                        for j in horizontal_range:
                            points_inside.add((i, j))
                    print()
                    break

    print(len(points_inside))                

if __name__ == "__main__":
    with open("input.txt") as fp:
        direction_with_colors = []
        while line:= fp.readline():
            line = line.strip().split()
            direction_with_colors.append(((line[0], int(line[1])), line[2][1:-1]))

        vertical_edges = []
        curr_tile = (0, 0)
        for i in range(1, len(direction_with_colors), 2):
            (prev_direction, prev_steps), prev_color =  direction_with_colors[i-1]
            (direction, steps), color = direction_with_colors[i]
            if prev_direction == "L":
                curr_tile = (curr_tile[0], curr_tile[1]-prev_steps)
            else:
                curr_tile = (curr_tile[0], curr_tile[1]+prev_steps)
            
            if direction == "U":
                start = curr_tile
                curr_tile = (curr_tile[0]-steps, curr_tile[1])
                end = curr_tile
                vertical_edges.append(VerticalEdge(end, start))
            else:
                start = curr_tile
                curr_tile = (curr_tile[0]+steps, curr_tile[1])
                end = curr_tile
                vertical_edges.append(VerticalEdge(start, end))
        
        count_number_holes(vertical_edges)