import back.sprites.component as c


class Scene:
    def __init__(self, args):
        self.args = args
        self.pos = (0, 0)
        self.background = c.Component(lambda ui: ui.show_div((0, 0), self.args.size, color=(60, 179, 113)))
        self.buttons = {
            '1': c.Button((self.args.size[0] // 2, 300), (600, 80), 'Version 1',
                          font=('src', 'timesnewroman.ttf', 25), align=(1, 1), background=(210, 210, 210)),
            '2': c.Button((self.args.size[0] // 2, 400), (600, 80), 'Version 2',
                          font=('src', 'timesnewroman.ttf', 25), align=(1, 1), background=(210, 210, 210)),
            '3': c.Button((self.args.size[0] // 2, 500), (600, 80), 'Version 3',
                          font=('src', 'timesnewroman.ttf', 25), align=(1, 1), background=(210, 210, 210)),
            'back': c.Button((self.args.size[0] // 2, 600), (600, 80), 'Back',
                             font=('src', 'timesnewroman.ttf', 25), align=(1, 1), background=(210, 210, 210))
        }

    def process_events(self, events):
        if events['mouse-left'] == 'down':
            for name in self.buttons:
                if self.buttons[name].in_range(events['mouse-pos']):
                    return self.execute(name)
        return [None]

    def execute(self, name):
        if name == '1':
            return ['game', '1']
        elif name == '2':
            return ['game', '2']
        elif name == '3':
            return ['game', '3']
        elif name == 'back':
            return ['menu']

    def show(self, ui):
        self.background.show(ui)
        ui.show_text((self.args.size[0] // 2, 150), "Select A Version", font=('src', 'cambria.ttf', 60), align=(1, 1))
        for name in self.buttons:
            self.buttons[name].show(ui)
