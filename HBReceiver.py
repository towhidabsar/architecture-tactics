
import threading
import time
import multiprocessing
import ControlSystem
import time


class HBReceiver:
    def __init__(self):
        self.nodes = {}

    def checkStatus(self, id, status):
        if id in self.nodes.keys():
            lastUpdatedTime = self.nodes[id]

        if status == "Alive":
            self.nodes[id] += 1

def main():

    parent_pipe, child_pipe = multiprocessing.Pipe()
    controlsystem1 = ControlSystem.ControlSystem()
    hb = HBReceiver()
    #pool = multiprocessing.Pool(2, controlsystem1.runNuclearReactor, (child_pipe, ))
    while True:
        print parent_pipe.recv()

    # process1.start()
    # process2.start()
    # while True:
    #     message = queue.get()
    #     id = message[0]
    #     status = message[1]
    #     print "ID", id
    #     print "Status", status

main()

