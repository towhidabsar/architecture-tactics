import Reactor
import multiprocessing
import random
import os
class ControlSystem:
    def __init__(self):
        self.reactor = Reactor.Reactor()

    def runNuclearReactor(self, queue):
        kill_process = 0
        count = 1
        while True:
            #Checking core Temperature of the reactor\n
            temp = self.reactor.getCentralTemp()
            if temp > 9:
                #ALERT: Temperature too high, please drop control rods!
                self.reactor.dropControlRods()
            else:
                #Temperature under control, raise control rods!
                self.reactor.raiseControlRods()

            #"Checking Safety Valve status\n"
            safety = self.reactor.getSafetyValveStats()
            if safety < 2:
                #"ALERT: Safety valve malfunction, please drop control rods!"
                self.reactor.dropControlRods()
            else:
                #"Safety valve functioning!"
                self.reactor.raiseControlRods()
            self.sendHeartbeat(queue)
            kill_process = random.randint(1,100)
            if kill_process == 99:
                queue.send([os.getpid(), count])
                print "Process dead", os.getpid()
                break
            else:
                count +=1

    def sendHeartbeat(self, queue):
        #print os.getpid(), "Alive"
        queue.send([os.getpid(), "Alive"])



