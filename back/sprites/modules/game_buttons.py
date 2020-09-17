import back.sprites.component as c
import utils.functions as utils


class GameButtons:
    def __init__(self, pos, *, size=(200, 150), align=(0, 0)):
        # display
        self.pos = utils.top_left(pos, size, align=align)
        self.size = size
        # buttons
        self.buttons = {
            'next': c.Button((self.pos[0] + self.size[0] // 2, self.pos[1] + 25), (150, 40),
                          'confirm', font=('src', 'timesnewroman.ttf', 22), align=(1, 0)),
            'restore': c.Button((self.pos[0] + self.size[0] // 2, self.pos[1] + 85), (150, 40),
                          'undo', font=('src', 'timesnewroman.ttf', 22), align=(1, 0)),
        }

    def in_range(self, pos):
        return self.pos[0] < pos[0] < self.pos[0] + self.size[0] and self.pos[1] < pos[1] < self.pos[1] + self.size[1]

    def process(self, pos):
        # buttons
        for name in self.buttons:
            if self.buttons[name].in_range(pos):
                return name

    def show(self, ui, *, pan=(0, 0)):
        pos = self.pos[0] + pan[0], self.pos[1] + pan[1]
        # container
        ui.show_div(pos, self.size, color=(255, 255, 255))
        ui.show_div(pos, self.size, border=2)
        # buttons
        for name in self.buttons:
            self.buttons[name].show(ui)


class ReplaySpeed:
    def __init__(self, pos, *, size=(220, 100), align=(0, 0)):
        # display
        self.pos = utils.top_left(pos, size, align=align)
        self.size = size
        # buttons
        self.buttons = {
            'speed-': c.Button((self.pos[0] + self.size[0] // 2 - 75, self.pos[1] + 50), (30, 40), '', align=(1, 1)),
            '': c.Button((self.pos[0] + self.size[0] // 2, self.pos[1] + 50), (120, 40),
                          'speed×1', font=('src', 'timesnewroman.ttf', 22), align=(1, 1)),
            'speed+': c.Button((self.pos[0] + self.size[0] // 2 + 75, self.pos[1] + 50), (30, 40), '', align=(1, 1))
        }

    def in_range(self, pos):
        return self.pos[0] < pos[0] < self.pos[0] + self.size[0] and self.pos[1] < pos[1] < self.pos[1] + self.size[1]

    def process(self, pos):
        # buttons
        for name in self.buttons:
            if self.buttons[name].in_range(pos):
                return name

    def show(self, ui, *, pan=(0, 0)):
        pos = self.pos[0] + pan[0], self.pos[1] + pan[1]
        # container
        ui.show_div(pos, self.size, color=(255, 255, 255))
        ui.show_div(pos, self.size, border=2)
        # buttons
        for name in self.buttons:
            self.buttons[name].show(ui)
        # arrows
        color = (168, 168, 168) if self.buttons[''].text[-1:] == '1' else (0, 0, 0)
        ui.show_triangle((self.pos[0] + self.size[0] // 2 - 75, self.pos[1] + 50), 5, 'left', color=color)
        color = (168, 168, 168) if self.buttons[''].text[-1:] == '4' else (0, 0, 0)
        ui.show_triangle((self.pos[0] + self.size[0] // 2 + 75, self.pos[1] + 50), 5, 'right', color=color)
