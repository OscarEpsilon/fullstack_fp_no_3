class Char:
    hp = 4 + (level * 2)
    def __init__(self, name, level):
        self.name = str(name)
        self.level = int(level)
