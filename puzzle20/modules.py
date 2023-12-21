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
        self.destinations = destination_list

    def receive(self, received_from: Module, pulse: PULSE_TYPE):
        print(f"{received_from.name} -> {self.name}: {pulse}")
        pass

        
    
        
