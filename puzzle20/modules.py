from __future__ import annotations
from enum import Enum
import numpy as np


SEND_QUEUE = []


class PULSE_TYPE(Enum):
    HIGH = 0
    LOW = 1


class Module():
    def __init__(self, name: str) -> None:
        self.destinations = None
        self.name = name

    def set_destinations(self, destination_list: list[Module]):
        """
        Sets the destionation modules of this module

        :param destination_list: Should contain all the modules this module should send to
        """
        self.destinations = destination_list

    def reset_default(self):
        """
        The reset_default function does nothing in the base class
        and should be overwritte if anything has to be reset
        """
        pass


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

    def reset_default(self):
        """
        Resets the flip flop to its original state, meaning that it should be off
        """
        self.on = False


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

    def reset_default(self):
        """
        Resets the conjunction to its original state, meaning that all the last pulses,
        that need to be remembered should be defaulted to low
        """
        for name in self.last_pulses.keys():
            self.last_pulses[name] = PULSE_TYPE.LOW


class Rx(Module):
    def receive(self, received_from: Module, pulse: PULSE_TYPE):
        """
        The Rx module should do nothing with the pulse it receives

        :param received_from: The module the pulse was sent by. Not relevant for this module
        :param pulse: The pulse to receive
        """
        pass
