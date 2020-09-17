import back.backend as b
import front.frontend as f
import utils.args as a

# Front end: UI, user event
# Back end: ...


class App:
    def __init__(self, front_end=None, back_end=None, args=None):
        self.front_end = front_end
        self.back_end = back_end
        self.args = args
        self.running = False

    def prepare(self):
        self.front_end.prepare()  # input the utils into the back
        self.back_end.prepare()  # input the utils into the front

    def run(self):
        self.running = True
        while self.running:
            self.render()
            self.set_fps(80)
            self.events()

    def events(self):
        events = self.front_end.get_events()
        if events['quit']:
            self.quit()
        elif 'f' in events['key-down'] and ('left ctrl' in events['key-pressed'] or 'right ctrl' in events['key-pressed']):
            self.front_end.ui.toggle_fullscreen()
        else:
            command = self.back_end.process_events(events)
            if command == 'quit':
                self.quit()

    def render(self):
        self.front_end.render(self.back_end)

    def set_fps(self, fps):
        self.front_end.clock.tick(fps)

    def quit(self):
        self.front_end.quit()
        self.back_end.quit()
        self.running = False


def launch(args=a.Args()):
    app = App(f.FrontEnd(args), b.BackEnd(args), args)
    app.prepare()
    app.run()


if __name__ == '__main__':
    launch()
