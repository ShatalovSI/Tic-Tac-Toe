class Player:
    def __init__(self, name):
        self.name = name
        self.wins_count = 0
        self.player_positions = []

    def change_name(self, new_name):
        self.name = new_name

    def reset_count(self):
        self.wins_count = 0

    def reset_positions(self):
        self.player_positions = []
