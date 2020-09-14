class EnvShortCorridor:
    def on_action_received(self, a):
        if a == 0 and self.pos == 0:
            pass
        elif a == 1 and self.pos == 2:
            self.is_ended = True
        elif self.pos != 1:
            self.pos += (1 if (a == 1) else -1)
        elif self.pos == 1:
            self.pos += (1 if (a == 0) else -1)
        return -1

    def on_episode_begin(self):
        self.pos = 0
        self.is_ended = False

    def __init__(self):
        self.pos = 0
        self.is_ended = False


if __name__ == "__main__":
    env = EnvShortCorridor()
