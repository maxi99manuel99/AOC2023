from __future__ import annotations
from z3 import IntVector, Solver


class HailStone():
    def __init__(self, pos: tuple[int, int, int], velocity: tuple[int, int, int]) -> None:
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.vz = velocity[2]

    def get_intersect_pos_xy(self, other: HailStone) -> tuple[int, int]:
        """
        Returns the "intersection" position of this hailstone with another one (disregarding z).
        They do not have to actually intersect at a given time t, but only their paths
        have to have a common position

        :param other: The hailstone to compute the intersection pos with
        """
        # full credit to https://www.reddit.com/r/adventofcode/comments/18pnycy/2023_day_24_solutions/ket7ajw/?context=3
        if self.vy*other.vx == other.vy*self.vx:
            return False

        t_self = (other.vy*(self.x-other.x) - other.vx *
                  (self.y - other.y)) / (self.vy*other.vx - other.vy*self.vx)
        t_other = (self.vy*(other.x-self.x) - self.vx*(other.y -
                   self.y)) / (other.vy*self.vx - self.vy*other.vx)

        if t_self <= 0 or t_other <= 0:
            return None

        return (self.x + t_self * self.vx, self.y + t_self * self.vy)


def count_all_intersections_inside_area(hailstones: list[HailStone], boundaries_xy: tuple[tuple[int, int], tuple[int, int]]) -> int:
    """
    Returns the number of intersections happening between hailstones inside a given boundary area

    :param hailstones: contains all hailstones to check for intersections
    :param boundaries_xy: contains the bounded area in which the hailstones should intersect
    """
    boundaries_x = boundaries_xy[0]
    boundaries_y = boundaries_xy[1]
    count = 0
    for i, hailstone in enumerate(hailstones[:-1]):
        for other_hailstone in hailstones[i+1:]:
            intersection = hailstone.get_intersect_pos_xy(other_hailstone)
            if intersection:
                if intersection[0] >= boundaries_x[0] and intersection[0] <= boundaries_x[1] and intersection[1] >= boundaries_y[0] and intersection[1] <= boundaries_y[1]:
                    count += 1
    return count


def get_all_intersect_hailstone(hailstones: list[HailStone]) -> HailStone:
    """
    Returns one hailstone that has an intersection on its path with all other given hailstones

    :param hailstones: Contains all other hailstones that our newly created hailstone should intersect.
    """
    # full credit to https://github.com/fuglede/adventofcode/blob/master/2023/day24/solutions.py
    x_sol, y_sol, z_sol, xv_sol, yv_sol, zv_sol = IntVector("sol", 6)
    intersect_times = IntVector("t", len(hailstones))
    z3_solver = Solver()

    for t, hailstone in zip(intersect_times, hailstones):
        z3_solver.add(x_sol + t * xv_sol == hailstone.x + t * hailstone.vx)
        z3_solver.add(y_sol + t * yv_sol == hailstone.y + t * hailstone.vy)
        z3_solver.add(z_sol + t * zv_sol == hailstone.z + t * hailstone.vz)

    z3_solver.check()
    model = z3_solver.model()

    return HailStone((model[x_sol].as_long(), model[y_sol].as_long(), model[z_sol].as_long()), (model[xv_sol].as_long(), model[yv_sol].as_long(), model[zv_sol].as_long()))


def sum_pos_all_intersect_hailstone(hailstones: list[HailStone]) -> int:
    """
    Returns the sum of the position values (x, y, z) for the hailstone that intesects all given hailstones

    :param hailstones: Contains all other hailstones that the created hailstone needs to intersect
    """
    all_intersect_hailstone = get_all_intersect_hailstone(hailstones)
    return all_intersect_hailstone.x + all_intersect_hailstone.y + all_intersect_hailstone.z


if __name__ == "__main__":
    hailstones = []
    with open("input.txt") as fp:
        while line := fp.readline():
            pos, velocity = line.strip().split(" @ ")
            pos = pos.split(", ")
            pos = tuple(int(p) for p in pos)
            velocity = velocity.split(", ")
            velocity = tuple(int(v) for v in velocity)
            hailstones.append(HailStone(pos, velocity))
            
    print(f"Part 1 Result: {count_all_intersections_inside_area(hailstones, ((200000000000000, 400000000000000), (200000000000000, 400000000000000)))}")
    print(f"Part 2 Result: {sum_pos_all_intersect_hailstone(hailstones)}")
