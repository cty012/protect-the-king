import back.sprites.piece as p
import utils.functions as utils


class Block:
    def __init__(self, grid, size, *, align=(0, 0)):
        self.piece = None
        self.grid = grid
        self.pos = utils.top_left((grid[0] * size, grid[1] * size), (size, size), align=align)
        self.size = size

    def empty(self):
        return self.piece is None

    def in_range(self, pos, *, pan=(0, 0)):
        abs_pos = (self.pos[0] + pan[0], self.pos[1] + pan[1])
        return abs_pos[0] < pos[0] < abs_pos[0] + self.size and abs_pos[1] < pos[1] < abs_pos[1] + self.size

    def can_move(self, board):
        if self.piece is None or not self.piece.active:
            return []
        return self.piece.can_move(self.grid, board)

    def can_attack(self, board):
        if self.piece is None or not self.piece.active:
            return []
        return self.piece.can_attack(self.grid, board)

    def show(self, ui, *, color=(255, 255, 255), pan=(0, 0)):
        ui.show_div(self.pos, (self.size, self.size), color=color, pan=pan)
        if not self.empty():
            self.piece.show(ui, (self.pos[0] + self.size // 2 + pan[0], self.pos[1] + self.size // 2 + pan[1]), self.size)


class Map:
    def __init__(self, pos, mode, *, log=None, block_size=80, align=(0, 0)):
        # display
        self.mode = mode
        self.log = log
        self.size = {'1': (10, 5), '2': (12, 7), '3': (12, 7)}[self.mode]
        self.pos = utils.top_left(pos, (self.size[0] * block_size, self.size[1] * block_size), align=align)
        self.block_size = block_size
        # game
        self.board = [[Block((i, j), self.block_size)
                       for j in range(self.size[1])] for i in range(self.size[0])]
        self._board = [[None for j in range(self.size[1])] for i in range(self.size[0])]
        # prepare
        BoardLoader.preload(self.mode, self.board)
        BoardLoader.save(self.board, self._board)
        if self.mode == '3':
            self.deactivate()
        else:
            self.activate('defend')

    def calc_size(self):
        return self.size[0] * self.block_size, self.size[1] * self.block_size

    def move(self, pos, target, stage='battle'):
        b_pos, b_target = self.board[pos[0]][pos[1]], self.board[target[0]][target[1]]
        b_target.piece = b_pos.piece
        b_pos.piece = None
        b_target.piece.active = False
        if stage == 'battle' and self.log is not None:
            self.log.push(('move', pos, target))

    def attack(self, pos, target):
        b_pos, b_target = self.board[pos[0]][pos[1]], self.board[target[0]][target[1]]
        if 'aoe' in b_pos.piece.props:
            for p in b_pos.can_attack(self.board):
                self.board[p[0]][p[1]].piece = None
        else:
            b_target.piece = None
        b_pos.piece.active = False
        if self.log is not None:
            self.log.push(('attack', pos, target))

    def activate(self, side):
        for row in self.board:
            for block in row:
                if not block.empty():
                    block.piece.active = (block.piece.side == side)

    def deactivate(self):
        for row in self.board:
            for block in row:
                if not block.empty():
                    block.piece.active = False

    def get_grid(self, pos):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.board[i][j].in_range(pos, pan=self.pos):
                    return i, j

    def show_deploy(self, ui, cursor, side):
        available = (0, 3) if side == 'defend' else (9, 12)
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                is_avail = available[0] <= i < available[1]
                if (i, j) == cursor:
                    self.board[i][j].show(ui, color=(230, 230, 230) if is_avail else (168, 168, 168), pan=self.pos)
                elif is_avail:
                    self.board[i][j].show(ui, pan=self.pos)
                else:
                    self.board[i][j].show(ui, color=(128, 128, 128), pan=self.pos)
        self.show_grid(ui)

    def show(self, ui, cursor):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if (i, j) == cursor:
                    self.board[i][j].show(ui, color=(230, 230, 230), pan=self.pos)
                else:
                    self.board[i][j].show(ui, pan=self.pos)
        self.show_grid(ui)

    def show_grid(self, ui):
        # horizontal lines
        for i in range(self.size[1] + 1):
            start = (self.pos[0], self.pos[1] + i * self.block_size)
            end = (self.pos[0] + self.size[0] * self.block_size, self.pos[1] + i * self.block_size)
            ui.show_line(start, end)
        # vertical lines
        for i in range(self.size[0] + 1):
            start = (self.pos[0] + i * self.block_size, self.pos[1])
            end = (self.pos[0] + i * self.block_size, self.pos[1] + self.size[1] * self.block_size)
            ui.show_line(start, end)


class BoardLoader:
    @classmethod
    def preload(cls, version, board):
        if version == '1':
            cls.load(board, [
                [('soldier', 'defend'), ('cannon', 'defend'), ('king', 'defend'),
                 ('cannon', 'defend'), ('soldier', 'defend')],
                [('soldier', 'defend'), ('soldier', 'defend'), ('soldier', 'defend'),
                 ('soldier', 'defend'), ('soldier', 'defend')],
                [None, None, None, None, None],
                [None, None, None, None, None],
                [None, None, None, None, None],
                [None, None, None, None, None],
                [None, None, None, None, None],
                [('soldier', 'attack'), ('soldier', 'attack'), ('soldier', 'attack'),
                 ('soldier', 'attack'), ('soldier', 'attack')],
                [('soldier', 'attack'), ('soldier', 'attack'), ('soldier', 'attack'),
                 ('soldier', 'attack'), ('soldier', 'attack')],
                [('soldier', 'attack'), ('soldier', 'attack'), ('cannon', 'attack'),
                 ('soldier', 'attack'), ('soldier', 'attack')]
            ])
        elif version == '2':
            cls.load(board, [
                [('guard', 'defend'), ('flamethrower', 'defend'), ('cannon', 'defend'), ('king', 'defend'),
                 ('cannon', 'defend'), ('flamethrower', 'defend'), ('guard', 'defend')],
                [('soldier', 'defend'), ('soldier', 'defend'), ('soldier', 'defend'), ('soldier', 'defend'),
                 ('soldier', 'defend'), ('soldier', 'defend'), ('soldier', 'defend')],
                [None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None],
                [('militia', 'attack'), ('militia', 'attack'), ('militia', 'attack'), ('militia', 'attack'),
                 ('militia', 'attack'), ('militia', 'attack'), ('militia', 'attack')],
                [('soldier', 'attack'), ('soldier', 'attack'), ('soldier', 'attack'), ('soldier', 'attack'),
                 ('soldier', 'attack'), ('soldier', 'attack'), ('soldier', 'attack')],
                [('chariot', 'attack'), ('soldier', 'attack'), None, ('cannon', 'attack'),
                 None, ('soldier', 'attack'), ('chariot', 'attack')]
            ])
        elif version == '3':
            board[0][3].piece = p.King('defend')

    @classmethod
    def load(cls, board, _board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if _board[i][j] is not None:
                    name, side = _board[i][j]
                    cls_name = ''.join(map(lambda x: x.capitalize(), name.split('_')))
                    board[i][j].piece = eval(f'p.{cls_name}')(side)
                else:
                    board[i][j].piece = None

    @classmethod
    def save(cls, board, _board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j].piece is not None:
                    _board[i][j] = board[i][j].piece.name, board[i][j].piece.side
                else:
                    _board[i][j] = None
