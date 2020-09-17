import back.sprites.component as c
import utils.functions as utils


class Info:
    def __init__(self, pos, *, size=(200, 300), align=(0, 0)):
        self.pos = utils.top_left(pos, size, align=align)
        self.size = size
        self.button = c.Button((pos[0] + self.size[0] // 2, pos[1] + 240), (150, 40), 'deploy',
                                      font=('src', 'timesnewroman.ttf', 22), align=(1, 0))
        self.cursor = None
        self.expl = {
            'ranged': 'attacks without moving to target\'s position',
            'armored': 'immune to ranged attacks',
            'aoe': 'deal damage to all opponents',
            'profitable': 'yield $0.5 every two rounds'
        }

    def in_range(self, pos):
        return self.pos[0] < pos[0] < self.pos[0] + self.size[0] and self.pos[1] < pos[1] < self.pos[1] + self.size[1]

    def process(self, pos):
        if self.button.in_range(pos):
            return self.button.text

    def get_hover(self, pos, block):
        self.cursor = None
        if block.piece is not None:
            cur_pos = (20, 65)
            for prop in sorted(block.piece.props):
                cur_pos = (cur_pos[0], cur_pos[1] + 30)
                if cur_pos[0] + self.pos[0] < pos[0] < cur_pos[0] + self.pos[1] + 80 and \
                        cur_pos[1] + self.pos[0] - 2 < pos[1] < cur_pos[1] + self.pos[1] + 25:
                    self.cursor = prop

    def show(self, ui, block, pan=(0, 0), can_deploy=False, can_buy=False, can_remove=False):
        pos = self.pos[0] + pan[0], self.pos[1] + pan[1]
        # container
        ui.show_div(pos, self.size, color=(255, 255, 255))
        ui.show_div(pos, self.size, border=2)
        # title
        ui.show_text(
            (15, 20),
            'Empty' if block.empty() else ' '.join(map(lambda x: x.capitalize(), block.piece.name.split('_'))),
            font=('src', 'timesnewroman.ttf', 20),
            pan=self.pos
        )
        if not block.empty() and len(block.piece.props) > 0:
            ui.show_text((15, 60), 'properties:', font=('src', 'timesnewroman.ttf', 20), pan=self.pos)
            cur_pos = (20, 65)
            for prop in sorted(block.piece.props):
                cur_pos = (cur_pos[0], cur_pos[1] + 30)
                text = f'{prop}: {self.expl[prop]}' if self.cursor == prop else prop
                background = (255, 255, 255) if self.cursor == prop else None
                ui.show_text(cur_pos, text, font=('src', 'timesnewroman.ttf', 20), pan=self.pos, background=background)
        # deploy button
        if can_deploy:
            self.button.text = 'deploy'
            self.button.background = (204, 255, 204) if can_buy else (255, 204, 204)
            self.button.show(ui)
        elif can_remove:
            self.button.text = 'remove'
            self.button.background = (255, 255, 255)
            self.button.show(ui)
