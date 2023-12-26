from __future__ import annotations
import numpy as np

class HailStone():
    def __init__(self, pos: tuple[int, int, int], velocity: tuple[int, int, int]) -> None:
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.vz = velocity[2]
    
    def get_intersect_pos_xy(self, other: HailStone):
        if self.vy*other.vx == other.vy*self.vx:
            return False
    
        t_self = (other.vy*(self.x-other.x) - other.vx*(self.y - other.y)) / (self.vy*other.vx - other.vy*self.vx)
        t_other = (self.vy*(other.x-self.x) - self.vx*(other.y - self.y)) / (other.vy*self.vx - self.vy*other.vx)

        if t_self <= 0 or t_other <= 0:
            return None 
        
        return (self.x + t_self * self.vx, self.y + t_self * self.vy)


def count_all_intersections_inside_area(hailstones: list[HailStone], boundaries_xy: tuple[tuple[int, int], tuple[int, int]]):
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
    
if __name__ == "__main__":
    hailstones = []
    with open("input.txt") as fp:
        while line:= fp.readline():
            pos, velocity = line.strip().split(" @ ")
            pos = pos.split(", ")
            pos = tuple(int(p) for p in pos)
            velocity = velocity.split(", ")
            velocity = tuple(int(v) for v in velocity)
            hailstones.append(HailStone(pos, velocity))
    print(f"Part 1 Result: {count_all_intersections_inside_area(hailstones, ((200000000000000, 400000000000000), (200000000000000, 400000000000000)))}")
            