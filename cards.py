import random

class Card:
    def __init__(self):
        self.color = ""

    def new_card(self):
        self.color = random.choice(["blue", "green", "cyan", "red", "purple", "yellow"])
        return print(self.color)

    def combine(self, base_card, additional):
        pass