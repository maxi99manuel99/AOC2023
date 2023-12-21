from __future__ import annotations
from enum import Enum


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

    def receive(self, received_from: Module, pulse: PULSE_TYPE):
        """
        The base class modules receive does nothing with the passed pulse.

        :param received_from: The module the pulse was sent by
        :param pulse: The pulse to receive
        """
        pass
