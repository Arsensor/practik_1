from civilian_p import Civilian


class Police(Civilian):
    def __init__(self, name, gender, age, cunning, eloquence):
        super().__init__(name, gender, age, cunning, eloquence)
        self.role = "Полицейский"