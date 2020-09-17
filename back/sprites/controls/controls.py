import os

import back.sprites.controls.info as i


class Controls:
    def __init__(self, map):
        self.map = map
        self.cursor = None
        self.info_box = i.Info((15, 15))

    def show(self, ui, stage=None, can_deploy=False, can_buy=False, can_remove=False):
        if self.cursor is None:
            return
        block = self.map.board[self.cursor[0]][self.cursor[1]]
        b_s = self.map.block_size
        if stage is None or stage == 'battle':
            # show can_move
            grids = block.can_move(self.map.board)
            for grid in grids:
                pos = (grid[0] * b_s + b_s // 2, grid[1] * b_s + b_s // 2)
                ui.show_img(pos, os.path.join('others', 'can_move.png'), align=(1, 1), pan=self.map.pos)
            # show can_attack
            grids = block.can_attack(self.map.board)
            for grid in grids:
                pos = (grid[0] * b_s + b_s // 2, grid[1] * b_s + b_s // 2)
                ui.show_img(pos, os.path.join('others', 'can_attack.png'), align=(1, 1), pan=self.map.pos)
        # show info box
        self.info_box.show(ui, block, can_deploy=can_deploy, can_buy=can_buy, can_remove=can_remove)
