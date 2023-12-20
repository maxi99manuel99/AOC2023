from dataclasses import dataclass


@dataclass
class VerticalEdgePoint():
    x: int
    is_edge_start: bool = False
    is_edge_end: bool = False
    turn_direction: str = None


def count_holes(edge_points_per_row: dict[int, VerticalEdgePoint]) -> int:
    """
    Returns the amount of holes that were digged by considering the edge points in 
    each row of our map

    :param edge_points_per_row: contains a row number as key and the edge points in that row as values
    """
    count = 0
    for row in edge_points_per_row.keys():
        edge_points = sorted(edge_points_per_row[row], key=lambda x: x.x)
        inside = True
        for i in range(len(edge_points)-1):
            if edge_points[i].is_edge_start and edge_points[i+1].is_edge_end:
                count += edge_points[i+1].x - edge_points[i].x - 1
                if edge_points[i].turn_direction == edge_points[i+1].turn_direction:
                    inside = not inside
            else:
                if inside:
                    count += edge_points[i+1].x - edge_points[i].x - 1
                inside = not inside
        count += len(edge_points)

    return count


if __name__ == "__main__":
    with open("input.txt") as fp:
        direction_with_colors = []
        while line := fp.readline():
            line = line.strip().split()
            direction_with_colors.append(
                ((line[0], int(line[1])), line[2][1:-1]))

        edge_points_per_row = {}
        curr_tile = (0, 0)
        (next_direction, next_steps), next_color = direction_with_colors[0]
        
        for i in range(1, len(direction_with_colors), 2):
            (prev_direction, prev_steps), prev_color = (
                next_direction, next_steps), next_color
            if i == len(direction_with_colors) - 1:
                (next_direction,
                 next_steps), next_color = direction_with_colors[0]
            else:
                (next_direction,
                 next_steps), next_color = direction_with_colors[i+1]
            
            (direction, steps), color = direction_with_colors[i]

            if prev_direction == "L":
                curr_tile = (curr_tile[0], curr_tile[1]-prev_steps)
            else:
                curr_tile = (curr_tile[0], curr_tile[1]+prev_steps)

            if direction == "U":
                prev_turn_direction = "L" if prev_direction == "R" else "R"
                if next_direction == "L":
                    edge_points_per_row.setdefault(curr_tile[0]-steps, []).append(VerticalEdgePoint(
                        x=curr_tile[1], is_edge_end=True, turn_direction=next_direction))
                else:
                    edge_points_per_row.setdefault(curr_tile[0]-steps, []).append(VerticalEdgePoint(
                        x=curr_tile[1], is_edge_start=True, turn_direction=next_direction))
                for y in range(curr_tile[0]-steps+1, curr_tile[0]):
                    edge_points_per_row.setdefault(y, []).append(
                        VerticalEdgePoint(x=curr_tile[1]))
                if prev_direction == "L":
                    edge_points_per_row.setdefault(curr_tile[0], []).append(VerticalEdgePoint(
                        x=curr_tile[1], is_edge_start=True, turn_direction=prev_turn_direction))
                else:
                    edge_points_per_row.setdefault(curr_tile[0], []).append(VerticalEdgePoint(
                        x=curr_tile[1], is_edge_end=True, turn_direction=prev_turn_direction))

                curr_tile = (curr_tile[0]-steps, curr_tile[1])
            else:
                next_turn_direction = "L" if next_direction == "R" else "R"
                if prev_direction == "L":
                    edge_points_per_row.setdefault(curr_tile[0], []).append(VerticalEdgePoint(
                        x=curr_tile[1], is_edge_start=True, turn_direction=prev_direction))
                else:
                    edge_points_per_row.setdefault(curr_tile[0], []).append(VerticalEdgePoint(
                        x=curr_tile[1], is_edge_end=True, turn_direction=prev_direction))
                for y in range(curr_tile[0]+1, curr_tile[0]+steps):
                    edge_points_per_row.setdefault(y, []).append(
                        VerticalEdgePoint(x=curr_tile[1]))
                if next_direction == "L":
                    edge_points_per_row.setdefault(curr_tile[0]+steps, []).append(VerticalEdgePoint(
                        x=curr_tile[1], is_edge_end=True, turn_direction=next_turn_direction))
                else:
                    edge_points_per_row.setdefault(curr_tile[0]+steps, []).append(VerticalEdgePoint(
                        x=curr_tile[1], is_edge_start=True, turn_direction=next_turn_direction))
                curr_tile = (curr_tile[0]+steps, curr_tile[1])

        print(f"Part 1 Result {count_holes(edge_points_per_row)}")
