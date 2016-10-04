import random
import time
from Queue import Empty
class Reactor:
    def __init__(self, queues, reciever):
        self.counter = 0
        self.rateOfReaction = 0
        self.controlRodDropped = False
        self.queues = queues
        self.receiver = reciever
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
        self.controlRodDropped = False

    def runNuclearReactor(self):
        timestamp = 0
        while True:
            time.sleep(0.01)
            temp = self.getCentralTemp()
            safety = self.getSafetyValveStats()
            for q in self.queues:
                #print [temp, safety, timestamp]
                q.put([temp, safety, timestamp])
            timestamp += 1
            try:
                order = self.receiver.get_nowait()
                print order
                if order[2] == "Raise":
                    self.raiseControlRods()
                else:
                    self.dropControlRods()


            except Empty:
                pass


