from multiprocessing import Process, Queue, Pool
from Queue import Empty
import ControlSystem
import Reactor
import time

class HBReceiver:
    def __init__(self):
        pass

    def updateStatus(self):
        lastTimeStamp = 0
        error1 = 0
        error2 = 0
        reactorqueue1 = Queue()
        reactorqueue2 = Queue()
        receiverQueue = Queue()
        receiverQueue1 = Queue()
        receiverQueue2 = Queue()
        reactor = Reactor.Reactor([reactorqueue1, reactorqueue2], receiverQueue)
        controlsystem1 = ControlSystem.ControlSystem(reactorqueue1, receiverQueue1)
        controlsystem2 = ControlSystem.ControlSystem(reactorqueue2,receiverQueue2)

        pr = Process(target=reactor.runNuclearReactor)
        pc1 = Process(target=controlsystem1.runNuclearReactor)
        pc2 = Process(target=controlsystem2.runNuclearReactor)
        pr.start()
        pc1.start()
        pc2.start()

        while True:
            data1 = ""
            data2 = ""
            try:
                data1 = receiverQueue1.get_nowait()
                timestamp = data1[3]
                error1 = 0
                while timestamp <= lastTimeStamp:
                    data1 = receiverQueue1.get_nowait()
                    timestamp = data1[3]
                lastTimeStamp = timestamp

            except Empty:
                error1 += 1
                time.sleep(0.01)
                if error1 > 5:
                    error1 = 0
                    pc1.join()
                    Process(target=controlsystem1.runNuclearReactor).start()
            try:
                data2 = receiverQueue2.get_nowait()
                timestamp = data2[3]
                error2 = 0
                while timestamp <= lastTimeStamp:
                    data1 = receiverQueue1.get_nowait()
                    timestamp = data1[3]
                lastTimeStamp = timestamp
            except Empty:
                error2 += 1
                time.sleep(0.01)
                if error2 > 5:
                    error2 = 0
                    pc2.join()
                    Process(target=controlsystem2.runNuclearReactor).start()

            if data1 != "":
                receiverQueue.put(data1)
            elif data2 != "":
                receiverQueue.put(data2)






def main2():
    hb = HBReceiver()
    phb = Process(target=hb.updateStatus)
    phb.start()


if __name__ == "__main__":
    main2()

