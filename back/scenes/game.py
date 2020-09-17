import back.sprites.component as c
import back.sprites.game as g
import back.sprites.game3 as g3
import back.sprites.replay as r
import back.sprites.saver as s


class Scene:
    def __init__(self, args, mode, file=None):
        self.args = args
        self.pos = (0, 0)
        self.background = c.Component(lambda ui: ui.show_div((0, 0), self.args.size, color=(60, 179, 113)))
        self.mode = None
        self.game = None
        if mode in ['1', '2', '3']:
            self.mode = mode
            self.game = (g3.Game3 if mode == '3' else g.Game)(self.args, self.mode)
            self.game.prepare()
        elif mode == 'save':
            self.mode = file.mode
            self.game = file
        elif mode == 'replay':
            self.mode = file.mode
            self.game = r.Replay(self.args, self.mode)
            self.game.prepare(log=file)
        self.saver = s.Saver(args, msg=self.game.name)
        self.buttons = {}

    def process_events(self, events):
        # save
        if self.saver.active:
            self.execute(self.saver.process(events))
        # game
        else:
            # key event
            for key in events['key-pressed']:
                if key == 'w':
                    self.game.move((0, 10))
                elif key == 'a':
                    self.game.move((10, 0))
                elif key == 's':
                    self.game.move((0, -10))
                elif key == 'd':
                    self.game.move((-10, 0))
            # mouse click event
            return self.execute(self.game.process(events))
        return [None]

    def execute(self, name):
        if name == 'save':
            self.saver.activate(self.game.name)
        elif type(name) == list and name[0] == 'save_game':
            self.save(name[1])
        elif name == 'quit':
            return ['menu']
        return [None]

    def save(self, file):
        self.saver.save(self.game, file)

    def show(self, ui):
        self.background.show(ui)
        self.game.show(ui)
        self.saver.show(ui)
