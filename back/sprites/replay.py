import back.sprites.game as g
import back.sprites.map as m
import back.sprites.modules.barrack as b
import back.sprites.modules.game_buttons as gb
import back.sprites.modules.game_menu as gm
import back.sprites.modules.player as p
import back.sprites.piece as pi


class Replay(g.Game):
    def __init__(self, args, mode):
        super().__init__(args, mode)
        self.script = None

    def prepare(self, log=None):
        self.script = log
        self.log = None
        self.map = m.Map((self.args.size[0] // 2, self.args.size[1] // 2), self.mode, log=self.log, align=(1, 1))
        bot = p.ReplayBot(self.map, self.script)
        m.BoardLoader.load(self.map.board, log.init_board)
        self.map.activate('defend')
        self.players = {'defend': bot, 'attack': bot}
        self.game_menu = gm.GameMenu((self.args.size[0] - 15, 15), buttons=('play', 'quit'), align=(2, 0))
        self.game_buttons = gb.ReplaySpeed((self.args.size[0] - 15, self.args.size[1] - 15), align=(2, 2))
        if self.mode == '3':
            self.barrack = b.Barrack((15, self.args.size[1] - 15), self.args, self.map, self.log, align=(0, 2))
            st = self.barrack.stores['defend'], self.barrack.stores['attack']
            (st[0]._items, st[1]._items), (st[0]._money, st[1]._money) = log.init_items, log.init_money
            b.StoreLoader.load(st[0])
            b.StoreLoader.load(st[1])
        self.new_controls()

    def execute(self, name):
        if name == 'play':
            bot = self.players[self.game_menu.side]
            if not bot.stopwatch.is_running():
                bot.stopwatch.start()
            self.game_menu.buttons['play'].text = 'pause'
        elif name == 'pause':
            bot = self.players[self.game_menu.side]
            if bot.stopwatch.is_running():
                bot.stopwatch.stop()
            self.game_menu.buttons['play'].text = 'play'
        elif name == 'end':
            bot = self.players[self.game_menu.side]
            if bot.stopwatch.is_running():
                bot.stopwatch.stop()
            self.game_menu.buttons['play'].text = 'replay'
        elif name == 'replay':
            self.prepare(self.script)
            self.execute('play')
        elif name == 'speed+':
            bot = self.players[self.game_menu.side]
            speed = min(bot.speed * 2, 4)
            bot.speed = speed
            bot.stopwatch.set_speed(speed)
            self.game_buttons.buttons[''].text = f'speed×{speed}'
        elif name == 'speed-':
            bot = self.players[self.game_menu.side]
            speed = max(bot.speed // 2, 1)
            bot.speed = speed
            bot.stopwatch.set_speed(speed)
            self.game_buttons.buttons[''].text = f'speed×{speed}'
        elif name == 'quit':
            return 'quit'
        elif name == 'next':
            self.next()
            self.salary()

    def salary(self):
        if self.game_menu.round > 1 and self.game_menu.side == 'defend':
            for row in self.map.board:
                for block in row:
                    if not block.empty() and 'profitable' in block.piece.props:
                        self.barrack.stores[block.piece.side].money += 0.5

    def show(self, ui):
        super().show(ui)
        if self.barrack is not None:
            self.barrack.show(ui, side=None)
