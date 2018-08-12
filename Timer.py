import time

class Timer:
    def __init__(self,ability,cooldown):
        self.ability = ability
        self.cooldown = cooldown

        self.period = "waiting"
        self.t0 = time.time()
        self.time = self.t0

    def update(self):
        if not self.period == "waiting":
            self.time = int(time.time()-self.t0)

            if self.time >= self.ability and self.period == "ability":
                self.period = "cooldown"

            if self.time >= self.cooldown + self.ability and self.period == "cooldown":
                self.period = "waiting"

    def start(self):
        if self.period == "waiting":
            self.period = "ability"
            self.t0 = time.time()

    @property
    def status(self):
        return self.period
