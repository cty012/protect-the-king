import back.sprites.controls.controls as c
import back.sprites.map as m
import back.sprites.modules.game_buttons as gb
import back.sprites.modules.game_menu as gm
import back.sprites.modules.log as l
import back.sprites.modules.player as p


class Game:
    def __init__(self, args, mode):
        # args
        self.args = args
        self.name = ''
        # game
        self.mode = mode
        # modules
        self.log = None
        self.map = None
        self.players = None
        self.game_menu = None  # top-right
        self.game_buttons = None  # bottom-right
        self.barrack = None  # bottom-left
        self.controls = None  # top-left

    def prepare(self, log=None):
        self.log = l.Log(self.mode)
        self.map = m.Map((self.args.size[0] // 2, self.args.size[1] // 2), self.mode, log=self.log, align=(1, 1))
        self.players = {'defend': p.Human(self.map, 'defend'), 'attack': p.Human(self.map, 'attack')}
        self.game_menu = gm.GameMenu((self.args.size[0] - 15, 15), align=(2, 0))
        self.game_buttons = gb.GameButtons((self.args.size[0] - 15, self.args.size[1] - 15), align=(2, 2))
        self.log.prepare(self.map)
        self.new_controls()

    def new_controls(self):
        self.controls = c.Controls(self.map)

    def process(self, events):
        pos = events['mouse-pos']
        if events['mouse-left'] == 'down':
            # detect barrack
            if self.barrack is not None and self.barrack.in_range(pos):
                pass
            # detect info box
            elif self.controls.cursor is not None and self.controls.info_box.in_range(pos):
                return self.execute(self.controls.info_box.process(pos))
            # detect game menu
            elif self.game_menu.in_range(pos):
                return self.execute(self.game_menu.process(pos))
            # detect game buttons
            elif self.game_menu.winner is None and self.game_buttons.in_range(pos):
                return self.execute(self.game_buttons.process(pos))
            # detect board
            else:
                new_cs = self.players[self.game_menu.side].process_click(pos, self.controls.cursor)
                self.controls.cursor = new_cs
        # detect hover on info
        if self.controls.cursor is not None:
            cursor = self.controls.cursor
            self.controls.info_box.get_hover(pos, self.map.board[cursor[0]][cursor[1]])
        self.execute(self.players[self.game_menu.side].process())

    def execute(self, name):
        if name == 'save':
            return 'save'
        elif name == 'quit':
            return 'quit'
        elif name == 'next':
            self.next()
        elif name == 'restore':
            self.restore()

    def move(self, units):
        pos = (self.map.pos[0] + units[0], self.map.pos[1] + units[1])
        pos = (min(pos[0], self.args.size[0] // 2), min(pos[1], self.args.size[1] // 2))
        size = self.map.calc_size()
        self.map.pos = [max(pos[0], self.args.size[0] // 2 - size[0]), max(pos[1], self.args.size[1] // 2 - size[1])]

    def next(self):
        # save configurations
        m.BoardLoader.save(self.map.board, self.map._board)
        # commit log
        if self.log is not None:
            self.log.commit()
        # check victory condition
        winner = self.check_victory()
        if winner is not None:
            self.game_menu.victory(winner)
            self.map.deactivate()
        else:
            self.game_menu.next()
            self.map.activate(self.game_menu.side)

    def restore(self):
        m.BoardLoader.load(self.map.board, self.map._board)
        self.map.activate(self.game_menu.side)
        self.log.clear()

    def check_victory(self):
        # check king and attack
        king = False
        attack = False
        for row in self.map.board:
            for block in row:
                if not block.empty() and block.piece.name == 'king':
                    king = True
                if not block.empty() and block.piece.side == 'attack':
                    attack = True
        if not king:
            return 'attack'
        elif not attack:
            return 'defend'
        # check rounds
        elif self.game_menu.round == 30 and self.game_menu.side == 'attack':
            return 'defend'
        # no one wins
        else:
            return None

    def show(self, ui):
        # map
        self.map.show(ui, self.controls.cursor)
        # controls
        self.controls.show(ui)
        # if game not finished
        if self.game_menu.winner is None:
            # game buttons
            self.game_buttons.show(ui)
        # game menu
        self.game_menu.show(ui)
