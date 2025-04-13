
class ShipType:
    def __init__(self, name, layout, max_hp, max_shield, max_heat, max_energy, energy_gen, speed, acceleration):
        self.name = name
        self.layout = layout
        self.max_hp = max_hp
        self.max_shield = max_shield
        self.max_energy = max_energy
        self.energy_gen = energy_gen
        self.max_heat = max_heat
        self.speed = speed

        self.acceleration = acceleration

    def get_cell_type(self, x, y):
        if 0 <= y < len(self.layout) and 0 <= x < len(self.layout[0]):
            return self.layout[y][x]
        return "X"  # Default to blocked if out of bounds

starter_ship = ShipType(
    name="Starburst",
    layout=[
        ["W2","X","W1","X","W2"],
        ["D", "X","D", "X","D"],
        ["X", "X","D", "X","X"],
    ],
    max_hp=1000,
    max_shield=200,
    max_energy=800,
    energy_gen=1,
    max_heat = 100,
    speed=4,
    acceleration=0.2,
)