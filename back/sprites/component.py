import os

import utils.functions as utils
import back.sprites.saver as s


# COMPONENT
class Component:
    def __init__(self, func):
        self.show = func

    def set_func(self, func):
        self.show = func


# BUTTON
class Button:
    def __init__(self, pos, size, text, *, font=('ttf', 'freesansbold.ttf', 25),
                 border=2, color=((0, 0, 0), (0, 0, 0)), align=(0, 0), background=None):
        self.pos = utils.top_left(pos, size, align=align)
        self.size = size
        self.text = text
        self.font = font
        self.border = border
        self.color = color
        self.align = align
        self.background = background

    def in_range(self, pos):
        return self.pos[0] < pos[0] < self.pos[0] + self.size[0] and self.pos[1] < pos[1] < self.pos[1] + self.size[1]

    def show(self, ui):
        if self.background is not None:
            ui.show_div(self.pos, self.size, border=0, color=self.background)
        ui.show_div(self.pos, self.size, border=self.border, color=self.color[0])
        center = self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2
        ui.show_text(center, self.text, self.font, color=self.color[1], align=(1, 1))


class SavedFile:
    def __init__(self, name, mode, size, *, color=(210, 210, 210)):
        # display
        self.name = name
        self.mode = mode
        self.size = size
        self.color = color
        # game
        self.game = None
        self.game_mode = None
        self.round = None
        self.side = None
        self.err = False
        try:
            if self.mode == 'save':
                self.game = s.Saver.load(self.name, self.mode)
                self.game.new_controls()
                self.game_mode = self.game.mode
                self.round = self.game.game_menu.round
                self.side = self.game.game_menu.side
            elif self.mode == 'replay':
                # game = log
                self.game = s.Saver.load(self.name, self.mode)
                self.game_mode = self.game.mode
                self.round = (len(self.game.record) + 1) // 2
                self.side = ['attack', 'defend'][len(self.game.record) % 2]
        except:
            print(f'ERROR loading saved file: {self.name}.ptk')
            self.err = True

    def in_range(self, b_pos, pos, *, align=(0, 0)):
        b_pos = utils.top_left(b_pos, self.size, align=align)
        return b_pos[0] < pos[0] < b_pos[0] + self.size[0] and b_pos[1] < pos[1] < b_pos[1] + self.size[1]

    def process(self, pos, mouse_pos, *, align=(0, 0)):
        pos = utils.top_left(pos, self.size, align=align)
        x0, x1, y0, y1, y2 = pos[0] + 650, pos[0] + 800, pos[1], pos[1] + self.size[1] // 2, pos[1] + self.size[1]
        if x0 < mouse_pos[0] < x1 and y0 < mouse_pos[1] < y1:
            return ['game', self.mode, self.game]
        elif x0 < mouse_pos[0] < x1 and y1 < mouse_pos[1] < y2:
            return ['delete', self.mode, self.name]
        return [None]

    def show(self, ui, pos, *, align=(0, 0), pan=(0, 0)):
        pos = utils.top_left(pos, self.size, align=align)
        # show box
        ui.show_div(pos, self.size, color=self.color, pan=pan)
        ui.show_div(pos, self.size, border=2, pan=pan)
        ui.show_line((pos[0] + 400, pos[1]), (pos[0] + 400, pos[1] + self.size[1]), width=2, pan=pan)
        ui.show_line((pos[0] + 650, pos[1]), (pos[0] + 650, pos[1] + self.size[1]), width=2, pan=pan)
        ui.show_line((pos[0] + 650, pos[1] + self.size[1] // 2), (pos[0] + 800, pos[1] + self.size[1] // 2), width=2, pan=pan)
        # show name
        ui.show_text((pos[0] + 50, pos[1] + self.size[1] // 2), self.name,
                     ('src', 'timesnewroman.ttf', 22), align=(0, 1), pan=pan)
        if not self.err:
            # show game info
            ui.show_text((pos[0] + 450, pos[1] + self.size[1] // 2 - 30), f'Version {self.game_mode}',
                         ('src', 'timesnewroman.ttf', 20), align=(0, 1), pan=pan)
            text = {
                'save': f'Round {self.round}',
                'replay': f'{self.round} round' if self.round == 1 else f'{self.round} rounds'
            }[self.mode]
            ui.show_text((pos[0] + 450, pos[1] + self.size[1] // 2), text,
                         ('src', 'timesnewroman.ttf', 20), align=(0, 1), pan=pan)
            text = {
                'save': f'{self.side.capitalize()}\'s turn',
                'replay': f'{self.side.capitalize()} wins'
            }[self.mode]
            ui.show_text((pos[0] + 450, pos[1] + self.size[1] // 2 + 30), text,
                         ('src', 'timesnewroman.ttf', 20), color={'defend': (255, 0, 0), 'attack': (0, 0, 255)}[self.side],
                         align=(0, 1), pan=pan)
        # show buttons
        ui.show_img((pos[0] + 725, pos[1] + self.size[1] // 4), os.path.join('others', 'play.png'), align=(1, 1), pan=pan)
        ui.show_img((pos[0] + 725, pos[1] + 3 * self.size[1] // 4), os.path.join('others', 'delete.png'), align=(1, 1), pan=pan)
