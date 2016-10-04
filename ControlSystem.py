import Reactor
import multiprocessing
import sys
from Queue import Empty
import random
import os
import time

'''
Class representing the control system for the nuclear reactor.
'''
class ControlSystem:
    def __init__(self, reactor, receiver):
        self.reactor = reactor
        self.receiver = receiver

    def runNuclearReactor(self):
        time.sleep(0.01)
        kill_process = 0
        instruction = "Drop"
        timestamp = 0
        count = 1
        while True:
            try:
                time.sleep(0.01)
                info = self.reactor.get_nowait()
                temp = info[0]
                safety = info[1]
                timestamp = info[2]
                if temp > 9 or safety < 2:
                    instruction = "Drop"
                else:
                    instruction = "Raise"
            except Empty:
                pass
            finally:
                self.sendHeartbeat(instruction, timestamp)
            kill_process = random.randint(1,100)
            if kill_process > 90:
                print "Process dead", os.getpid()
                break
            else:
                count +=1

    def sendHeartbeat(self, instruction,timestamp):
        #os.getpid(), "Alive", instruction
        self.receiver.put([os.getpid(), "Alive", instruction, timestamp])



