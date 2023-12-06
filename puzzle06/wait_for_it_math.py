import numpy as np
class Race():
    
    def __init__(self, time: int, distance_record: int) -> None:
        self.time = time
        self.distance_record = distance_record

    def calculate_number_ways_to_beat(self):
        delta = np.sqrt((self.time**2 - 4*self.distance_record))

        x1 = int(np.floor((time - delta) / 2))
        x2 = int(np.ceil((time + delta) / 2))

        return x2 - x1 - 1


if __name__ == "__main__":
    with open("input.txt") as fp:
        times = fp.readline().split(": ")[1].strip().split()
        times = list(map(int, times))
        distances = fp.readline().split(":")[1].strip().split()
        distances = list(map(int, distances))
        
        product_number_ways_to_beat = 1
        for time, distance in zip(times, distances):
            race = Race(time, distance)
            product_number_ways_to_beat *= race.calculate_number_ways_to_beat()
        print(f"Part 1 Result: {product_number_ways_to_beat}")
        
        actual_race_time = int(''.join(map(str, times)))
        actual_distance = int(''.join(map(str, distances)))
        actual_race = Race(actual_race_time, actual_distance)
        print(f"Part 2 Result: {actual_race.calculate_number_ways_to_beat()}")


        
