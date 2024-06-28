from player_p import Player


class Civilian(Player):
    def __init__(self, name, gender, age, cunning, eloquence):
        super().__init__(name, gender, age, cunning, eloquence)
        self.role = "Мирный житель"