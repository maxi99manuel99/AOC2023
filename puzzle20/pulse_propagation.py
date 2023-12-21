import numpy as np

from modules import Module, PULSE_TYPE

SEND_QUEUE = []


class Broadcaster(Module):
    def receive(self, pulse: PULSE_TYPE):
        """
        The broadcast module sends the pulse it receives to all its 
        destinations

        :param pulse: the received pulse
        """
        for dest in self.destinations:
            SEND_QUEUE.append((self, pulse, dest))


class FlipFlop(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.on = False

    def receive(self, _: Module, pulse: PULSE_TYPE):
        """
        The flip flop module only sends to its destinations when
        it receives a low. It also has a flip that defines if it sends
        a high or low

        :param _: The module the pulse was sent by. Not relevant for this module
        :param pulse: The pulse it received
        """
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
        """
        This function appends new keys into the last pulses
        variable and defaults them to pulse type low.

        :param module: A module that sends pulses to this module
        """
        self.last_pulses[module.name] = PULSE_TYPE.LOW

    def receive(self, received_from: Module, pulse: PULSE_TYPE):
        """
        The Conjuction remembers all the pulses that were send by
        other modules and sends new pulses based on this memory

        :param received_from: The module the pulse was sent by
        :param pulse: the pulse to be received
        """
        self.last_pulses[received_from.name] = pulse
        if np.all(np.array(list(self.last_pulses.values())) == PULSE_TYPE.HIGH):
            for dest in self.destinations:
                SEND_QUEUE.append((self, PULSE_TYPE.LOW, dest))
        else:
            for dest in self.destinations:
                SEND_QUEUE.append((self, PULSE_TYPE.HIGH, dest))


def push_button_n_times(start_module: Module, n: int) -> int:
    """
    Pushs the main button n times consequently, which will send a low pulse
    to the start module. Returns the total count of high and low pulses that were 
    sent in the system

    :param start_module: The module to send the low pulse
    :param n: The amount of times to push the button
    """
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

    return counts[PULSE_TYPE.HIGH] * counts[PULSE_TYPE.LOW]


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

    for module, destination_str in modules_dict.values():
        destination_list = []
        for char in destination_str:
            if not char in modules_dict:
                receiving_module = Module(char)
            else:
                receiving_module = modules_dict[char][0]
            destination_list.append(receiving_module)
            if isinstance(receiving_module, Conjunction):
                receiving_module.append_input_list(module)
        module.set_destinations(destination_list)

    print(f"Result Part 1: {push_button_n_times(start_module, 1000)}")
