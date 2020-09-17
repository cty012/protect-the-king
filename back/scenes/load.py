import os

import back.sprites.component as c


class Scene:
    def __init__(self, args, mode):
        self.args = args
        self.bar_height = 100
        self.mode = mode
        self.margin = 40
        self.padding = 20
        self.background = c.Component(lambda ui: ui.show_div((0, 0), self.args.size, color=(60, 179, 113)))
        self.saves = [c.SavedFile(file[:file.index('.')], self.mode, (800, 120))
                      for file in os.listdir(os.path.join('.', self.mode))
                      if file.endswith('.ptk' if self.mode == 'save' else '.ptkr')]
        self.pan = 0
        self.button = c.Button((self.args.size[0] // 2, self.args.size[1] - self.bar_height // 2), (200, 50), 'back',
                               font=('src', 'timesnewroman.ttf', 22), align=(1, 1), background=(210, 210, 210))

    def process_events(self, events):
        total_height = len(self.saves) * (self.padding + 120) - self.padding + 2 * self.margin
        if events['mouse-left'] == 'down':
            m_pos = events['mouse-pos']
            # back button
            if m_pos[1] >= self.args.size[1] - self.bar_height:
                if self.button.in_range(m_pos):
                    return ['menu']
            # saved files
            else:
                for i, saved_file in enumerate(self.saves):
                    pos = (self.args.size[0] // 2, self.margin + i * (self.padding + saved_file.size[1]) + self.pan)
                    if saved_file.in_range(pos, m_pos, align=(1, 0)):
                        return saved_file.process(pos, m_pos, align=(1, 0))
        elif events['mouse-wheel'] == 'up':
            self.pan += 30
            self.pan = min(self.pan, 0)
        elif events['mouse-wheel'] == 'down' and total_height > self.args.size[1] - self.bar_height:
            self.pan -= 30
            self.pan = max(self.pan, self.args.size[1] - self.bar_height - total_height)
        return [None]

    def show(self, ui):
        # background
        self.background.show(ui)
        # saves
        for i, saved_file in enumerate(self.saves):
            saved_file.show(ui, (self.args.size[0] // 2, self.margin + i * (self.padding + saved_file.size[1])),
                            align=(1, 0), pan=(0, self.pan))
        # bar
        ui.show_div((0, self.args.size[1]), (self.args.size[0], self.bar_height), color=(46, 139, 87), align=(0, 2))
        ui.show_line((0, self.args.size[1] - self.bar_height), (self.args.size[0], self.args.size[1] - self.bar_height), width=2)
        # button
        self.button.show(ui)
