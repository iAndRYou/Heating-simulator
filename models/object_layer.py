class ObjectLayer:
    def __init__(self, thickness, conductivity, density, specific_heat_capacity):
        self.thickness : float = thickness  
        self.conductivity : float = conductivity  # Thermal conductivity coefficient (W/mK)
        self.density : float = density  # Material density (kg/m³)
        self.specific_heat_capacity : float = specific_heat_capacity  # Specific heat capacity of the material (J/(kgK))