from dataclasses import dataclass

@dataclass
class Material:
    name: str
    conductivity: float
    density: float
    specific_heat_capacity: float
        