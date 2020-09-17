import pygame


class Event:
    def __init__(self):
        pass

    def detect(self):
        all_events = {
            'quit': False,
            'mouse-left': 'hover',
            'mouse-wheel': 'static',
            'mouse-pos': pygame.mouse.get_pos(),
            'key-down': [],
            'key-up': [],
            'key-pressed': None,
        }
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                all_events['quit'] = True
            elif event.type == pygame.KEYDOWN:
                all_events['key-down'].append(pygame.key.name(event.key))
            elif event.type == pygame.KEYUP:
                all_events['key-up'].append(pygame.key.name(event.key))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    all_events['mouse-left'] = 'down'
                elif event.button == 4:
                    all_events['mouse-wheel'] = 'up'
                elif event.button == 5:
                    all_events['mouse-wheel'] = 'down'
            elif event.type == pygame.MOUSEBUTTONUP:
                all_events['mouse-left'] = 'up'
        pressed = pygame.key.get_pressed()
        all_events['key-pressed'] = [pygame.key.name(key) for key in range(len(pressed)) if pressed[key]]
        return all_events
