class WeaponBase:
    def __init__(self, img_dict):
        self.img_dict = img_dict

    def get_name(self):
        return self.__class__.__name__

    def get_energy_cost(self):
        return 20

    def fire(self, pos, direction, group):
        raise NotImplementedError("Each weapon must implement its own fire method.")