import math
import numpy as np

from modules import Module, Broadcaster, FlipFlop, Conjunction, Rx, PULSE_TYPE, SEND_QUEUE


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


def count_button_press_till_machine_on(start_module: Module, rx_predecessor: Module) -> int:
    """
    Returns the amount of button presses needed till a low pulse would be send to the Rx 
    module

    :param start_module: The module that the first low pulse after every button press is send to
    :param rx_predecessor: The predecessor module that sends pulses to the rx module
    """
    count = 0
    modules_to_rx_loops = {}
    for module in rx_predecessor.last_pulses.keys():
        modules_to_rx_loops[module] = 0

    while True:
        count += 1
        start_module.receive(PULSE_TYPE.LOW)
        while SEND_QUEUE:
            source, pulse, dest = SEND_QUEUE.pop(0)
            dest.receive(source, pulse)
            if dest == rx_predecessor and pulse == PULSE_TYPE.HIGH:
                if modules_to_rx_loops[source.name] == 0:
                    modules_to_rx_loops[source.name] = count
                    if np.all(np.array(list(modules_to_rx_loops.values())) != 0):
                        return math.lcm(*list(modules_to_rx_loops.values()))


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
                receiving_module = Rx(char)
                rx_predecessor = module
            else:
                receiving_module = modules_dict[char][0]
            destination_list.append(receiving_module)
            if isinstance(receiving_module, Conjunction):
                receiving_module.append_input_list(module)
        module.set_destinations(destination_list)

    print(f"Result Part 1: {push_button_n_times(start_module, 1000)}")
    for module, _ in modules_dict.values():
        module.reset_default()
    print(
        f"Result Part 2: {count_button_press_till_machine_on(start_module, rx_predecessor)}")
