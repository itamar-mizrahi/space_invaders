class BaseState:
    def __init__(self, game):
        self.game = game

    def get_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass
