import pygame

import front.font as f
import front.image as i
import utils.functions as utils


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.image = i.Image()
        self.font = f.Font()

    def clear(self):
        self.screen.fill((255, 255, 255))

    def toggle_fullscreen(self):
        flags = self.screen.get_flags()
        if flags == 0:
            pygame.display.set_mode(flags=pygame.FULLSCREEN)
        elif flags == pygame.FULLSCREEN:
            pygame.display.set_mode(flags=0)

    def update(self):
        pygame.display.update()

    def show_line(self, start, end, *, width=1, color=(0, 0, 0), pan=(0, 0)):
        pygame.draw.line(self.screen, color, (start[0] + pan[0], start[1] + pan[1]),
                         (end[0] + pan[0], end[1] + pan[1]), width)

    def show_triangle(self, pos, radius, direction, *, border=0, color=(0, 0, 0), pan=(0, 0)):
        pos = (pos[0] + pan[0], pos[1] + pan[1])
        if direction == 'left':
            points = ((pos[0] - radius, pos[1]), (pos[0] + radius, pos[1] - 2 * radius), (pos[0] + radius, pos[1] + 2 * radius))
        else:
            points = ((pos[0] + radius, pos[1]), (pos[0] - radius, pos[1] - 2 * radius), (pos[0] - radius, pos[1] + 2 * radius))
        pygame.draw.polygon(self.screen, color, points, border)

    def show_div(self, pos, size, *, border=0, color=(0, 0, 0), align=(0, 0), pan=(0, 0)):
        # align: 0 left/top, 1 center, 2 right/bottom
        pos = (pos[0] + pan[0], pos[1] + pan[1])
        rect = [utils.top_left(pos, size, align=align), size]
        pygame.draw.rect(self.screen, color, rect, border)

    def show_text(self, pos, text, font, *, color=(0, 0, 0), background=None, align=(0, 0), pan=(0, 0)):
        pos = (pos[0] + pan[0], pos[1] + pan[1])
        text_img = None
        if font[0] == 'ttf':
            text_img = pygame.font.Font(font[1], font[2]).render(text, True, color)
        elif font[0] == 'src':
            text_img = pygame.font.Font(self.font.get(font[1]), font[2]).render(text, True, color)
        elif font[0] == 'sys':
            text_img = pygame.font.SysFont(font[1], font[2]).render(text, True, color)
        size = text_img.get_size()
        pos = utils.top_left(pos, size, align=align)
        if background is not None:
            pygame.draw.rect(self.screen, background, [pos, size])
        self.screen.blit(text_img, pos)

    def show_img(self, pos, path, *, align=(0, 0), pan=(0, 0)):
        pos = (pos[0] + pan[0], pos[1] + pan[1])
        img = self.image.get(path)
        size = img.get_size()
        self.screen.blit(img, utils.top_left(pos, size, align=align))
