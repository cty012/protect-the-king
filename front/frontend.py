import pygame

import front.event as e
import front.ui as u


class FrontEnd:
    def __init__(self, args):
        self.args = args
        self.screen = None
        self.event = None
        self.ui = None
        self.clock = None

    def prepare(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size=self.args.size)
        pygame.display.set_caption('Protect The King')
        self.event = e.Event()
        self.ui = u.UI(self.screen)
        pygame.display.set_icon(self.ui.image.load('icon.png'))
        self.clock = pygame.time.Clock()

    # Event operation
    def get_events(self):
        return self.event.detect()

    # UI operation
    def render(self, component):
        self.ui.clear()
        component.show(self.ui)
        self.ui.update()

    def quit(self):
        pygame.display.quit()
        pygame.quit()
