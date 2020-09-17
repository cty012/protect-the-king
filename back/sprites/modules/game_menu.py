import back.sprites.component as c
import utils.functions as utils


class GameMenu:
    def __init__(self, pos, *, buttons=('save', 'quit'), size=(200, 220), align=(0, 0)):
        # display
        self.pos = utils.top_left(pos, size, align=align)
        self.size = size
        # game
        self.round = 1
        self.side = 'defend'
        self.winner = None
        # buttons
        self.buttons = {
            buttons[0]: c.Button((self.pos[0] + self.size[0] // 2, self.pos[1] + 110), (150, 40),
                          buttons[0], font=('src', 'timesnewroman.ttf', 22), align=(1, 0)),
            buttons[1]: c.Button((self.pos[0] + self.size[0] // 2, self.pos[1] + 160), (150, 40),
                          buttons[1], font=('src', 'timesnewroman.ttf', 22), align=(1, 0)),
        }

    def in_range(self, pos):
        return self.pos[0] < pos[0] < self.pos[0] + self.size[0] and self.pos[1] < pos[1] < self.pos[1] + self.size[1]

    def process(self, pos):
        # buttons
        for name in self.buttons:
            if self.buttons[name].in_range(pos):
                return self.buttons[name].text

    def next(self):
        self.side = {'defend': 'attack', 'attack': 'defend'}[self.side]
        if self.side == 'defend':
            self.round += 1

    def victory(self, winner):
        self.winner = winner

    def show_deploy(self, ui, *, pan=(0, 0)):
        pos = self.pos[0] + pan[0], self.pos[1] + pan[1]
        # container
        ui.show_div(pos, self.size, color=(255, 255, 255))
        ui.show_div(pos, self.size, border=2)
        # round
        ui.show_text((self.size[0] // 2, 20), 'DEPLOYMENT',
                     ('src', 'timesnewroman.ttf', 25), align=(1, 0), pan=pos)
        ui.show_text((self.size[0] // 2, 65), f'{self.side.capitalize()}\'s turn', ('src', 'timesnewroman.ttf', 22),
                     color={'defend': (255, 0, 0), 'attack': (0, 0, 255)}[self.side], align=(1, 0), pan=pos)
        # buttons
        for name in self.buttons:
            self.buttons[name].show(ui)

    def show(self, ui, *, pan=(0, 0)):
        pos = self.pos[0] + pan[0], self.pos[1] + pan[1]
        # container
        ui.show_div(pos, self.size, color=(255, 255, 255))
        ui.show_div(pos, self.size, border=2)
        # round
        ui.show_text((self.size[0] // 2, 20), f'ROUND {self.round}',
                     ('src', 'timesnewroman.ttf', 25), align=(1, 0), pan=pos)
        if self.winner is None:
            ui.show_text((self.size[0] // 2, 65), f'{self.side.capitalize()}\'s turn', ('src', 'timesnewroman.ttf', 22),
                         color={'defend': (255, 0, 0), 'attack': (0, 0, 255)}[self.side], align=(1, 0), pan=pos)
        else:
            ui.show_text((self.size[0] // 2, 65), f'{self.winner.capitalize()} wins!', ('src', 'timesnewroman.ttf', 22),
                         color={'defend': (255, 0, 0), 'attack': (0, 0, 255)}[self.winner], align=(1, 0), pan=pos)
        # buttons
        for name in self.buttons:
            self.buttons[name].show(ui)
