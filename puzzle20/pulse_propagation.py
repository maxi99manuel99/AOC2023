import numpy as np

from modules import Module, PULSE_TYPE

SEND_QUEUE = []

class Broadcaster(Module):
    def receive(self, pulse: PULSE_TYPE):
        for dest in self.destinations:
            SEND_QUEUE.append((self, pulse, dest))


class FlipFlop(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.on = False

    def receive(self, received_from: Module, pulse: PULSE_TYPE):
        print(f"{received_from.name} -> {self.name}: {pulse}")
        if pulse == PULSE_TYPE.LOW:
            if not self.on:
                for dest in self.destinations:
                    SEND_QUEUE.append((self, PULSE_TYPE.HIGH, dest))
            else:
                for dest in self.destinations:
                    SEND_QUEUE.append((self, PULSE_TYPE.LOW, dest))
            self.on = not self.on


class Conjunction(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.last_pulses = {}
        
    def append_input_list(self, module: Module):
        self.last_pulses[module.name] = PULSE_TYPE.LOW

    def receive(self, received_from: Module, pulse: PULSE_TYPE):
        print(f"{received_from.name} -> {self.name}: {pulse}")
        self.last_pulses[received_from.name] = pulse
        if np.all(np.array(list(self.last_pulses.values())) == PULSE_TYPE.HIGH):
            for dest in self.destinations:
                SEND_QUEUE.append((self, PULSE_TYPE.LOW, dest))
        else:
            for dest in self.destinations:
                SEND_QUEUE.append((self, PULSE_TYPE.HIGH, dest))

def push_button_n_times(start_module: Module, n: int):
    counts = {
        PULSE_TYPE.LOW: n,
        PULSE_TYPE.HIGH: 0
    }
    for _ in range(n):
        start_module.receive(PULSE_TYPE.LOW)
        while SEND_QUEUE:
            source, pulse, dest = SEND_QUEUE.pop(0)
            counts[pulse] += 1
            dest.receive(source, pulse)
        print()
    print(counts[PULSE_TYPE.HIGH]* counts[PULSE_TYPE.LOW])

if __name__ == "__main__":
    modules_dict = {}
    start_module = None
    with open("input.txt") as fp:
        while line := fp.readline():
            name, destinations = line.strip().split(" -> ")
            destinations = destinations.split(", ")
            if name == "broadcaster":
                start_module = Broadcaster(name)
                modules_dict[name] = (start_module, destinations)
            elif name[0] == "%":
                modules_dict[name[1:]] = (FlipFlop(name[1:]), destinations)
            elif name[0] == "&":
                modules_dict[name[1:]] = (Conjunction(name[1:]), destinations)
            else:
                modules_dict[name] = (Module(name), destinations)
    
    for module, destination_str in modules_dict.values():
        destination_list = []
        for char in destination_str:
            if not char in modules_dict:
                continue
            receiving_module = modules_dict[char][0]
            destination_list.append(receiving_module)
            if isinstance(receiving_module, Conjunction):
                receiving_module.append_input_list(module)
        module.set_destinations(destination_list)
    
    push_button_n_times(start_module, 1000)
    
    


