import back.sprites.map as m


class Log:
    def __init__(self, mode):
        self.mode = mode
        self.init_board = None
        self.init_items = None
        self.init_money = None
        self.record = []
        self._record = []

    def prepare(self, map, barrack=None):
        self.init_board = [[None for j in range(len(map.board[0]))] for i in range(len(map.board))]
        m.BoardLoader.save(map.board, self.init_board)
        if barrack is not None:
            self.init_items = barrack.stores['defend']._items, barrack.stores['attack']._items
            self.init_money = barrack.stores['defend']._money, barrack.stores['attack']._money

    def push(self, command):
        self._record.append(command)

    def commit(self):
        self.record.append(self._record)
        self._record = []

    def clear(self):
        self._record = []
