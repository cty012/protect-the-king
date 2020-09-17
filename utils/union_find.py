class UnionFind:
    @classmethod
    def root(cls, uf, pos):
        if type(uf[pos[0]][pos[1]]) == int:
            return pos
        uf[pos[0]][pos[1]] = cls.root(uf, uf[pos[0]][pos[1]])
        return uf[pos[0]][pos[1]]

    @classmethod
    def union(cls, uf, pos1, pos2):
        pos1, pos2 = cls.root(uf, pos1), cls.root(uf, pos2)
        if pos1 != pos2:
            uf[pos2[0]][pos2[1]] += uf[pos1[0]][pos1[1]]
            uf[pos1[0]][pos1[1]] = pos2

    @classmethod
    def find(cls, uf, pos1, pos2):
        return cls.root(uf, pos1) == cls.root(uf, pos2)

    @classmethod
    def is_empty(cls, pos0, pos, board):
        return (pos[0] == pos0[0] and pos[1] == pos0[1]) or board[pos0[0]][pos0[1]].empty()

    @classmethod
    def can_move(cls, pos, board):
        (x, y), size = pos, (len(board), len(board[0]))
        uf = [[1 for j in range(size[1])] for i in range(size[0])]
        # union
        for i in range(size[0]):
            for j in range(size[1]):
                if cls.is_empty((i, j), (x, y), board):
                    if i > 0 and cls.is_empty((i - 1, j), (x, y), board):
                        cls.union(uf, (i, j), (i - 1, j))
                    if j > 0 and cls.is_empty((i, j - 1), (x, y), board):
                        cls.union(uf, (i, j), (i, j - 1))
        # find
        ans = []
        for i in range(size[0]):
            for j in range(size[1]):
                if not (x == i and y == j) and cls.find(uf, (x, y), (i, j)):
                    ans.append((i, j))
        return ans
