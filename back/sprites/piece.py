import os

import utils.union_find as uf


class Piece:
    def __init__(self, side):
        self.name = 'piece'
        self.side = side
        self.active = False
        self.fr = {'attack': -1, 'defend': 1}[side]
        self.props = []

    def _edge(self, pos, board):
        (x, y), size = pos, (len(board), len(board[0]))
        ans = []
        for i, j in ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)):
            if 0 <= i < size[0] and 0 <= j < size[1]:
                ans.append((i, j))
        return ans

    def _corner(self, pos, board):
        (x, y), size = pos, (len(board), len(board[0]))
        ans = []
        for i, j in ((x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)):
            if 0 <= i < size[0] and 0 <= j < size[1]:
                ans.append((i, j))
        return ans

    def friendly(self, pos, board):
        block = board[pos[0]][pos[1]]
        return not block.empty() and block.piece.side == self.side

    def hostile(self, pos, board):
        block = board[pos[0]][pos[1]]
        return not block.empty() and block.piece.side != self.side

    def can_move(self, pos, board):
        return []

    def can_attack(self, pos, board):
        return []

    def show(self, ui, center, size):
        ui.show_img(center, os.path.join(self.side, self.name + '.png'), align=(1, 1))
        if self.active:
            ui.show_div(center, (size - 3, size - 3), border=6, color=(0, 255, 255), align=(1, 1))


class King(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.name = 'king'

    def can_move(self, pos, board):
        return [p for p in self._edge(pos, board) + self._corner(pos, board) if not self.friendly(p, board)]


class Mortar(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.name = 'mortar'
        self.props.append('ranged')

    def can_move(self, pos, board):
        return [p for p in self._edge(pos, board) if board[p[0]][p[1]].empty()]

    def can_attack(self, pos, board):
        i, j, size = pos[0] + self.fr, pos[1], (len(board), len(board[0]))
        num_piece = 0
        while 0 <= i < size[0]:
            if num_piece == 0 and not board[i][j].empty():
                num_piece = 1
            elif num_piece == 1:
                if self.hostile((i, j), board):
                    if 'armored' in board[i][j].piece.props:
                        return []
                    else:
                        return [(i, j)]
                elif self.friendly((i, j), board):
                    return []
            i += self.fr
        return []


class Cannon(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.name = 'cannon'
        self.props.append('ranged')

    def can_move(self, pos, board):
        return [p for p in self._edge(pos, board) if board[p[0]][p[1]].empty()]

    def can_attack(self, pos, board):
        i, j, size = pos[0] + self.fr, pos[1], (len(board), len(board[0]))
        while 0 <= i < size[0]:
            if self.hostile((i, j), board):
                if 'armored' in board[i][j].piece.props:
                    return []
                else:
                    return [(i, j)]
            elif self.friendly((i, j), board):
                return []
            else:
                i += self.fr
        return []


class Crossbow(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.name = 'crossbow'
        self.props.append('ranged')

    def can_move(self, pos, board):
        return [p for p in self._edge(pos, board) if board[p[0]][p[1]].empty()]

    def can_attack(self, pos, board):
        (x, y), size = pos, (len(board), len(board[0]))
        possible = self._edge(pos, board) + self._corner(pos, board)
        possible += [p for p in [(x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)] if
                     0 <= p[0] < size[0] and 0 <= p[1] < size[1]]
        return [p for p in possible if self.hostile(p, board) and 'armored' not in board[p[0]][p[1]].piece.props]


class Chariot(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.name = 'chariot'

    def can_move(self, pos, board):
        (x, y), size = pos, (len(board), len(board[0]))
        ans = [(i, j) for (i, j) in [(x, y - 1), (x, y + 1)] if 0 <= j < size[1] and not self.friendly((i, j), board)]
        # +1
        i, j = x + 1, y
        while i < size[0]:
            if not self.friendly((i, j), board):
                ans.append((i, j))
            if not board[i][j].empty():
                break
            i += 1
        # -1
        i, j = x - 1, y
        while i >= 0:
            if not self.friendly((i, j), board):
                ans.append((i, j))
            if not board[i][j].empty():
                break
            i -= 1
        return ans


class Flamethrower(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.name = 'flamethrower'
        self.props.append('ranged')
        self.props.append('aoe')

    def can_move(self, pos, board):
        return [p for p in self._edge(pos, board) if board[p[0]][p[1]].empty()]

    def can_attack(self, pos, board):
        (x, y), size = pos, (len(board), len(board[0]))
        ans = []
        for i, j in ((x + self.fr, y - 1), (x + self.fr, y), (x + self.fr, y + 1)):
            if 0 <= i < size[0] and 0 <= j < size[1] and \
                    self.hostile((i, j), board) and 'armored' not in board[i][j].piece.props:
                ans.append((i, j))
        return ans


class ArmoredSoldier(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.name = 'armored_soldier'
        self.props.append('armored')

    def can_move(self, pos, board):
        return [p for p in self._edge(pos, board) if not self.friendly(p, board)]


class Miner(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.name = 'miner'

    def can_move(self, pos, board):
        possible = uf.UnionFind.can_move(pos, board)
        print(possible)
        return [p for p in self._edge(pos, board) + self._corner(pos, board)
                if not self.friendly(p, board) and p not in possible] + possible


class Guard(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.name = 'guard'

    def can_move(self, pos, board):
        return [p for p in self._edge(pos, board) + self._corner(pos, board) if not self.friendly(p, board)]


class Soldier(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.name = 'soldier'

    def can_move(self, pos, board):
        return [p for p in self._edge(pos, board) if not self.friendly(p, board)]


class Driller(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.name = 'driller'
        self.props.append('profitable')

    def can_move(self, pos, board):
        return [p for p in self._edge(pos, board) if board[p[0]][p[1]].empty()]


class Militia(Piece):
    def __init__(self, side):
        super().__init__(side)
        self.name = 'militia'

    def can_move(self, pos, board):
        return [p for p in self._edge(pos, board) if (p[0] - pos[0]) * self.fr >= 0 and not self.friendly(p, board)]
