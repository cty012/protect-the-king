import back.sprites.component as c
import utils.functions as utils


class Store:
    def __init__(self, args, side, map, log, *, size=(600, 440), item_size=((40, 50), (170, 50), (40, 50))):
        # display
        self.args = args
        self.pos = utils.top_left((self.args.size[0] // 2, self.args.size[1] // 2), size, align=(1, 1))
        self.size = size
        self.item_size = item_size
        self.item_total_size = (item_size[0][0] + item_size[1][0] + item_size[2][0], item_size[1][1])
        self.cursor = None
        self.cursor_color = (230, 230, 230)
        self.avail_color = ((204, 255, 204), (255, 204, 204))
        # game
        self.side = side
        self.map = map
        self.log = log
        # store
        self.money = 60.00
        self._money = None
        self.items = {
            'mortar': {'count': 3, 'cost': 15, 'pos': (160, 60)},
            'cannon': {'count': 3, 'cost': 12, 'pos': (160, 140)},
            'crossbow': {'count': 6, 'cost': 7, 'pos': (160, 220)},
            'chariot': {'count': 6, 'cost': 6, 'pos': (160, 300)},
            'flamethrower': {'count': 6, 'cost': 6, 'pos': (160, 380)},
            'armored_soldier': {'count': 8, 'cost': 6, 'pos': (440, 60)},
            'miner': {'count': 8, 'cost': 6, 'pos': (440, 140)},
            'guard': {'count': 10, 'cost': 4, 'pos': (440, 220)},
            'soldier': {'count': 14, 'cost': 3, 'pos': (440, 300)},
            'driller': {'count': 8, 'cost': 3, 'pos': (440, 380)}
        }
        self._items = None
        StoreLoader.save(self)

    def in_range(self, pos):
        return self.pos[0] < pos[0] < self.pos[0] + self.size[0] and self.pos[1] < pos[1] < self.pos[1] + self.size[1]

    def in_button_range(self, pos, name):
        b_pos = utils.top_left(self.items[name]['pos'], self.item_total_size, align=(1, 1))
        b_pos = b_pos[0] + self.pos[0], b_pos[1] + self.pos[1]
        return b_pos[0] < pos[0] < b_pos[0] + self.item_total_size[0] and b_pos[1] < pos[1] < b_pos[1] + self.item_total_size[1]

    def process(self, pos):
        for name in self.items:
            if self.in_button_range(pos, name):
                self.cursor = name

    def can_buy(self, item):
        return item is not None and self.money >= self.items[item]['cost'] and self.items[item]['count'] > 0

    def buy(self, item, stage='deployment'):
        self.money -= self.items[item]['cost']
        self.items[item]['count'] -= 1

    def sell(self, item):
        self.items[item]['count'] += 1
        self.money += self.items[item]['cost']

    def show(self, ui):
        # container
        ui.show_div((self.args.size[0] // 2, self.args.size[1] // 2), self.size, color=(255, 255, 255), align=(1, 1))
        theme = {'defend': (128, 0, 0), 'attack': (0, 0, 128)}[self.side]
        ui.show_div((self.args.size[0] // 2, self.args.size[1] // 2), self.size,
                    border=3, color=theme, align=(1, 1))
        # contents
        for name in self.items:
            # CONTAINER
            pos1 = self.items[name]['pos']
            pos0 = (pos1[0] - (self.item_size[1][0] + self.item_size[0][0]) // 2, pos1[1])
            pos2 = (pos1[0] + (self.item_size[1][0] + self.item_size[2][0]) // 2, pos1[1])
            # count
            color = self.avail_color[0 if self.items[name]['count'] > 0 else 1]
            ui.show_div(pos0, self.item_size[0], color=color, align=(1, 1), pan=self.pos)
            # name
            color = self.cursor_color if self.cursor == name else (255, 255, 255)
            ui.show_div(pos1, self.item_size[1], color=color, align=(1, 1), pan=self.pos)
            # cost
            color = self.avail_color[0 if self.items[name]['cost'] <= self.money else 1]
            ui.show_div(pos2, self.item_size[2], color=color, align=(1, 1), pan=self.pos)
            # borders
            ui.show_div(self.items[name]['pos'], self.item_total_size,
                        color=theme, border=2, align=(1, 1), pan=self.pos)
            # CONTENTS
            # count
            ui.show_text(pos0, str(self.items[name]['count']), ('src', 'timesnewroman.ttf', 22), align=(1, 1), pan=self.pos)
            # name
            ui.show_text(pos1, name.replace('_', ' '), ('src', 'timesnewroman.ttf', 22), align=(1, 1), pan=self.pos)
            # cost
            ui.show_text(pos2, f'${self.items[name]["cost"]}', ('src', 'timesnewroman.ttf', 22), align=(1, 1), pan=self.pos)


class Barrack:
    def __init__(self, pos, args, map, log, *, size=(200, 220), align=(0, 0)):
        # display
        self.pos = utils.top_left(pos, size, align=align)
        self.args = args
        self.size = size
        # game
        self.stage = 'deployment'  # deployment, start
        self.map = map
        self.log = log
        # store
        self.active = False
        self.stores = {
            'defend': Store(self.args, 'defend', self.map, self.log),
            'attack': Store(self.args, 'attack', self.map, self.log)
        }
        self.buttons = {
            'store': c.Button((self.pos[0] + self.size[0] // 2, self.pos[1] + 150),
                              (150, 40), 'barrack', font=('src', 'timesnewroman.ttf', 22), align=(1, 0))
        }

    def in_range(self, pos):
        return self.pos[0] < pos[0] < self.pos[0] + self.size[0] and self.pos[1] < pos[1] < self.pos[1] + self.size[1]

    def process(self, pos):
        for name in self.buttons:
            if self.buttons[name].in_range(pos):
                if name == 'store':
                    if self.active:
                        self.stores['defend'].cursor = None
                        self.stores['attack'].cursor = None
                    self.active = not self.active

    def can_deploy(self, pos, side):
        if pos is None:
            return False
        elif self.stage == 'deployment':
            avail = (0, 3) if side == 'defend' else (9, 12)
            if avail[0] <= pos[0] < avail[1]:
                return True
        elif self.stage == 'battle':
            avail = ((0, 0), (0, 3), (0, 6)) if side == 'defend' else ((11, 0), (11, 3), (11, 6))
            if pos in avail:
                return True
        return False

    def can_buy(self, side):
        target = self.stores[side].cursor
        if target is None:
            return False
        return self.stores[side].can_buy(target)

    def show(self, ui, side):
        # container
        ui.show_div(self.pos, self.size, color=(255, 255, 255))
        ui.show_div(self.pos, self.size, border=2)
        # money
        ui.show_text((self.pos[0] + 30, self.pos[1] + 50), f'defend: ${self.stores["defend"].money: .2f}',
                     color=(255, 0, 0), font=('src', 'timesnewroman.ttf', 22), align=(0, 1))
        ui.show_text((self.pos[0] + 30, self.pos[1] + 100), f'attack: ${self.stores["attack"].money: .2f}',
                     color=(0, 0, 255), font=('src', 'timesnewroman.ttf', 22), align=(0, 1))
        if side is not None:
            # buttons
            for name in self.buttons:
                self.buttons[name].show(ui)
            # store
            if self.active:
                self.stores[side].show(ui)


class StoreLoader:
    @classmethod
    def save(cls, store):
        store._money = store.money
        store._items = {item: {info: store.items[item][info] for info in store.items[item]} for item in store.items}

    @classmethod
    def load(cls, store):
        store.money = store._money
        store.items = {_item: {_info: store._items[_item][_info] for _info in store._items[_item]} for _item in store._items}
