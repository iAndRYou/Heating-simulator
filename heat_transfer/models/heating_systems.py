from ..generic import *
class Radiator(HeatingSystem):
    def __init__(self, power, temperature):
        HeatingSystem.__init__(self, 'Radiator', power, temperature)
