import random
class Reactor:
    def __init__(self, child_pipe):
        self.counter = 0
        self.rateOfReaction = 0
        self.controlRodDropped = False
        self.pipe = child_pipe
        random.seed(10)

    def getCentralTemp(self):
        temp = random.randint(1, 10)
        return temp


    def getSafetyValveStats(self):
        safety = random.randint(1, 10)
        return safety

    def dropControlRods(self):
        self.controlRodDropped = True

    def raiseControlRods(self):
        self.controlRodDropped = True

    def runNuclearReactor(self):
        while True:
            order = self.pipe.recv()
            if order == "Raise":
                self.raiseControlRods()
            else:
                self.dropControlRods()

            temp = self.getCentralTemp()
            safety = self.getSafetyValveStats()
            self.pipe.send([temp, safety])

