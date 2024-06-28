from civilian_p import Civilian


class Doctor(Civilian):
    def __init__(self, name, gender, age, cunning, eloquence):
        super().__init__(name, gender, age, cunning, eloquence)
        self.role = "Доктор"