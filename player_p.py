class Player:
    def __init__(self, name, gender, age, cunning, eloquence):
        self.name = name
        self.gender = gender
        self.age = age
        self.cunning = cunning
        self.eloquence = eloquence
        self.role = None
        self.alive = True
        self.is_killed = False