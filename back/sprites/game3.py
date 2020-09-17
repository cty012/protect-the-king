import back.sprites.controls.controls as c
import back.sprites.map as m
import back.sprites.modules.barrack as b
import back.sprites.modules.game_buttons as gb
import back.sprites.modules.game_menu as gm
import back.sprites.modules.log as l
import back.sprites.modules.player as p
import back.sprites.piece as pi


class Game3:
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

    def prepare(self):
        self.log = l.Log(self.mode)
        self.map = m.Map((self.args.size[0] // 2, self.args.size[1] // 2), self.mode, log=self.log, align=(1, 1))
        self.players = {'defend': p.Human(self.map, 'defend'), 'attack': p.Human(self.map, 'attack')}
        self.game_menu = gm.GameMenu((self.args.size[0] - 15, 15), align=(2, 0))
        self.game_menu.round = 0
        self.game_buttons = gb.GameButtons((self.args.size[0] - 15, self.args.size[1] - 15), align=(2, 2))
        self.barrack = b.Barrack((15, self.args.size[1] - 15), self.args, self.map, self.log, align=(0, 2))
        self.new_controls()

    def new_controls(self):
        self.controls = c.Controls(self.map)

    def process(self, events):
        pos = events['mouse-pos']
        if events['mouse-left'] == 'down':
            # detect barrack
            if self.barrack.active and self.barrack.stores[self.game_menu.side].in_range(pos):
                return self.execute(self.barrack.stores[self.game_menu.side].process(pos))
            elif self.game_menu.winner is None and self.barrack.in_range(pos):
                return self.execute(self.barrack.process(pos))
            # detect info box
            elif self.controls.cursor is not None and self.controls.info_box.in_range(pos):
                return self.execute(self.controls.info_box.process(pos))
            # detect game menu
            elif not self.barrack.active and self.game_menu.in_range(pos):
                return self.execute(self.game_menu.process(pos))
            # detect game buttons
            elif not self.barrack.active and self.game_menu.winner is None and self.game_buttons.in_range(pos):
                return self.execute(self.game_buttons.process(pos))
            # detect board
            else:
                new_cs = self.players[self.game_menu.side]\
                    .process_click(pos, self.controls.cursor, stage=self.barrack.stage,
                                   avail=self.barrack.can_deploy)
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
            if self.barrack.stage == 'deployment'and self.game_menu.side == 'attack' and self.check_victory() is not None:
                return
            self.next()
            self.salary()
        elif name == 'restore':
            self.restore()
        elif name == 'deploy':
            cursor, side = self.controls.cursor, self.game_menu.side
            can_deploy = self.barrack.can_deploy(cursor, side) and self.map.board[cursor[0]][cursor[1]]
            can_buy = self.barrack.can_buy(side)
            if can_deploy and can_buy:
                self.deploy()
        elif name == 'remove':
            self.remove()

    def move(self, units):
        pos = (self.map.pos[0] + units[0], self.map.pos[1] + units[1])
        pos = (min(pos[0], self.args.size[0] // 2), min(pos[1], self.args.size[1] // 2))
        size = self.map.calc_size()
        self.map.pos = [max(pos[0], self.args.size[0] // 2 - size[0]), max(pos[1], self.args.size[1] // 2 - size[1])]

    def salary(self):
        if self.game_menu.round > 1 and self.game_menu.side == 'defend':
            for row in self.map.board:
                for block in row:
                    if not block.empty() and 'profitable' in block.piece.props:
                        self.barrack.stores[block.piece.side].money += 0.5

    def next(self):
        # save configurations
        m.BoardLoader.save(self.map.board, self.map._board)
        b.StoreLoader.save(self.barrack.stores[self.game_menu.side])
        # check
        if self.barrack.stage == 'deployment' and self.game_menu.side == 'attack':
            # start battle
            self.barrack.stage = 'battle'
            # prepare log
            if self.log is not None:
                self.log.prepare(self.map, self.barrack)
        elif self.barrack.stage == 'battle':
            # commit log
            if self.log is not None:
                self.log.commit()
        # check victory condition
        winner = self.check_victory()
        if self.barrack.stage == 'battle' and winner is not None:
            self.game_menu.victory(winner)
            self.map.deactivate()
        elif (self.barrack.stage == 'deployment' and self.game_menu.side == 'defend') or winner is None:
            self.game_menu.next()
            if self.barrack.stage == 'battle':
                self.map.activate(self.game_menu.side)

    def restore(self):
        m.BoardLoader.load(self.map.board, self.map._board)
        b.StoreLoader.load(self.barrack.stores[self.game_menu.side])
        if self.barrack.stage == 'battle':
            self.map.activate(self.game_menu.side)
        self.log.clear()

    def deploy(self):
        cursor, side = self.controls.cursor, self.game_menu.side
        # buy from store
        store = self.barrack.stores[side]
        store.buy(store.cursor)
        # deploy to map
        cls_name = ''.join(map(lambda x: x.capitalize(), store.cursor.split('_')))
        self.map.board[cursor[0]][cursor[1]].piece = eval(f'pi.{cls_name}')(side)
        self.map.board[cursor[0]][cursor[1]].piece.active = False
        # push to log
        if self.barrack.stage == 'battle':
            self.log.push(('deploy', cursor, store.cursor, side))

    def remove(self):
        cursor, side = self.controls.cursor, self.game_menu.side
        # sell to store
        store = self.barrack.stores[side]
        block = self.map.board[cursor[0]][cursor[1]]
        store.sell(block.piece.name)
        # remove from map
        block.piece = None

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
        if self.barrack.stage == 'deployment':
            self.map.show_deploy(ui, self.controls.cursor, self.game_menu.side)
        else:
            self.map.show(ui, self.controls.cursor)
        # controls
        cursor, side = self.controls.cursor, self.game_menu.side
        can_deploy = self.barrack.can_deploy(cursor, side) and self.map.board[cursor[0]][cursor[1]].empty()
        can_buy = self.barrack.can_buy(side)
        block = None if cursor is None else self.map.board[cursor[0]][cursor[1]]
        store = self.barrack.stores[side]
        can_remove = self.barrack.stage == 'deployment' and cursor is not None and not block.empty()\
                     and block.piece.side == side and block.piece.name in store.items
        self.controls.show(ui, stage=self.barrack.stage, can_deploy=can_deploy, can_buy=can_buy, can_remove=can_remove)
        # if game not finished
        if self.game_menu.winner is None:
            # game buttons
            self.game_buttons.show(ui)
            # barrack
            self.barrack.show(ui, self.game_menu.side)
        # game menu
        if self.barrack.stage == 'deployment':
            self.game_menu.show_deploy(ui)
        else:
            self.game_menu.show(ui)
