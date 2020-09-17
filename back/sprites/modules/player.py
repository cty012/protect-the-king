import back.sprites.piece as p
import utils.stopwatch as sw


class Human:
    def __init__(self, map, side):
        self.map = map
        self.side = side

    def process_click(self, pos, cursor, stage='battle', avail=lambda pos, side: False):
        grid = self.map.get_grid(pos)
        if cursor is not None and grid is not None:
            # both are valid blocks
            block = self.map.board[cursor[0]][cursor[1]]
            if not block.empty() and block.piece.side == self.side:
                # strategic redeployment
                if stage == 'deployment' and avail(grid, self.side) and self.map.board[grid[0]][grid[1]].empty():
                    self.map.move(cursor, grid, stage='deployment')
                elif block.piece.active:
                    if grid in block.can_move(self.map.board):
                        self.map.move(cursor, grid)
                    elif grid in block.can_attack(self.map.board):
                        self.map.attack(cursor, grid)
        return grid

    def process(self):
        return None


class ReplayBot:
    def __init__(self, map, log):
        self.map = map
        self.log = log
        self.gen = self.make_move()
        self.stopwatch = sw.Stopwatch()
        self.speed = 1

    def process_click(self, pos, cursor):
        return self.map.get_grid(pos)

    def process(self, barrack=None):
        if self.stopwatch.is_running() and self.stopwatch.get_time() >= 1:
            self.stopwatch.clear()
            self.stopwatch.start(self.speed)
            decision = next(self.gen, None)
            if decision is None:
                return 'end'
            elif decision[0] == 'move':
                self.map.move(decision[1], decision[2])
            elif decision[0] == 'attack':
                self.map.attack(decision[1], decision[2])
            elif decision[0] == 'deploy':
                cls_name = ''.join(map(lambda x: x.capitalize(), decision[2].split('_')))
                self.map.board[decision[1][0]][decision[1][1]].piece = eval(f'p.{cls_name}')(decision[3])
                self.map.board[decision[1][0]][decision[1][1]].piece.active = False
                if barrack is not None:
                    barrack.stores[decision[3]].buy(decision[2])
            elif decision[0] == 'next':
                return 'next'

    def make_move(self):
        for row in self.log.record:
            for command in row:
                yield command
            yield ['next']
