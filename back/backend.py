import os

import back.scenes as s


class BackEnd:
    def __init__(self, args):
        self.args = args
        self.scene = None

    def prepare(self):
        self.scene = s.menu.Scene(self.args)

    def process_events(self, events):
        command = self.scene.process_events(events)
        if command[0] == 'menu':
            self.scene = s.menu.Scene(self.args)
        elif command[0] == 'mode':
            self.scene = s.mode.Scene(self.args)
        elif command[0] == 'game':
            if command[1] in ['1', '2', '3']:
                self.scene = s.game.Scene(self.args, command[1])
            elif command[1] in ['save', 'replay']:
                self.scene = s.game.Scene(self.args, command[1], command[2])
        elif command[0] == 'load':
            self.scene = s.load.Scene(self.args, 'save')
        elif command[0] == 'replay':
            self.scene = s.load.Scene(self.args, 'replay')
        elif command[0] == 'delete':
            os.remove(os.path.join('.', command[1], command[2] + ('.ptk' if command[1] == 'save' else '.ptkr')))
            for i in range(len(self.scene.saves)):
                if self.scene.saves[i].name == command[2]:
                    self.scene.saves.pop(i)
                    break
        else:
            return command[0]

    def show(self, ui):
        self.scene.show(ui)

    def quit(self):
        self.scene = None
