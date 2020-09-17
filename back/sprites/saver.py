import os
import pickle
import re

import back.sprites.component as c
import utils.functions as utils


class Saver:
    def __init__(self, args, *, msg='', size=(600, 300), input_size=(500, 50), color=(192, 192, 192)):
        self.args = args
        self.size = size
        self.input_size = input_size
        self.color = color
        self.active = False
        self.msg = msg
        self.buttons = {
            'save': c.Button((self.args.size[0] // 2 - 100, self.args.size[1] // 2 + 100), (140, 40), 'save',
                             font=('src', 'timesnewroman.ttf', 22), border=1, align=(1, 1), background=(255, 255, 255)),
            'back': c.Button((self.args.size[0] // 2 + 100, self.args.size[1] // 2 + 100), (140, 40), 'back',
                             font=('src', 'timesnewroman.ttf', 22), border=1, align=(1, 1), background=(255, 255, 255))
        }

    def activate(self, name):
        self.active = True
        self.msg = name

    def deactivate(self):
        self.active = False

    def process(self, events):
        # key events
        for key in events['key-down']:
            regex = '^[a-zA-Z_\\-]$' if self.msg == '' else '^[a-zA-Z0-9_\\-]$'
            if len(self.msg) < 20 and re.match(regex, key):
                self.msg += self.shift(key, events['key-pressed'])
            elif key == 'backspace':
                self.msg = self.msg[:-1]
            elif key == 'escape':
                self.deactivate()
            elif key == 'return' and len(self.msg) > 0:
                msg = self.msg
                self.deactivate()
                return ['save_game', msg]
        # mouse click events
        if events['mouse-left'] == 'down':
            for name in self.buttons:
                if self.buttons[name].in_range(events['mouse-pos']):
                    return self.execute(name)

    def execute(self, name):
        if name == 'save':
            msg = self.msg
            self.deactivate()
            return ['save_game', msg]
        elif name == 'back':
            self.deactivate()

    def save(self, game, file):
        game.name = file
        # get new pos and controls
        pos, controls = game.map.pos, game.controls
        game.controls = None
        center = (self.args.size[0] // 2, self.args.size[1] // 2)
        size = (game.map.size[0] * game.map.block_size, game.map.size[1] * game.map.block_size)
        game.map.pos = utils.top_left(center, size, align=(1, 1))
        # save
        if game.game_menu.winner is None:
            with open(os.path.join('.', 'save', file + '.ptk'), 'wb') as f:
                pickle.dump(game, f)
        else:
            with open(os.path.join('.', 'replay', file + '.ptkr'), 'wb') as f:
                pickle.dump(game.log, f)
        # return to original pos and controls
        game.map.pos, game.controls = pos, controls

    @classmethod
    def load(cls, file, mode):
        with open(os.path.join('.', mode, file + ('.ptk' if mode == 'save' else '.ptkr')), 'rb') as f:
            content = pickle.load(f)
        return content

    def shift(self, key, pressed):
        if 'left shift' in pressed or 'right shift' in pressed:
            return '_' if key == '-' else key.capitalize()
        return key

    def show(self, ui):
        if self.active:
            center = (self.args.size[0] // 2, self.args.size[1] // 2)
            # show container
            ui.show_div(center, self.size, color=self.color, align=(1, 1))
            ui.show_div(center, self.size, border=1, align=(1, 1))
            # show title
            ui.show_text((center[0], center[1] - 100), 'SAVE', font=('src', 'timesnewroman.ttf', 30), align=(1, 1))
            # show input area
            ui.show_div((center[0], center[1] - 15), self.input_size, color=(255, 255, 255), align=(1, 1))
            ui.show_div((center[0], center[1] - 15), self.input_size, border=1, align=(1, 1))
            corner = utils.top_left((center[0], center[1] - 15), self.input_size, align=(1, 1))
            ui.show_text((corner[0] + 20, corner[1] + 14), self.msg, font=('src', 'timesnewroman.ttf', 22))
            # show buttons
            for name in self.buttons:
                self.buttons[name].show(ui)
