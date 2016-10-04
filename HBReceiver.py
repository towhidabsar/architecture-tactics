from multiprocessing import Process, Queue, Pool
from Queue import Empty
import ControlSystem
import Reactor
import time
'''
Class HBReceiver is the main process that acts as the moderator for the Control System process.
It receives the Heartbeat and also synchronizes the data from the control system process
and sends it to the Reactor process. If one of the control system processes die, it restarts it
to make sure the Control System is always available to the Reactor.
'''
class HBReceiver:
    def __init__(self):
        pass

    def updateStatus(self):
        #Last updated data from the reactor and control system to synchronize them.
        lastTimeStamp = 0
        #Used to check if any of the processes have been dead.
        error1 = 0
        error2 = 0
        #Queus used to pass messages between the control system and the reactor
        reactorqueue1 = Queue()
        reactorqueue2 = Queue()
        receiverQueue = Queue()
        receiverQueue1 = Queue()
        receiverQueue2 = Queue()

        #The reactor simulator itself
        reactor = Reactor.Reactor([reactorqueue1, reactorqueue2], receiverQueue)

        #The two control system processes running in parallel
        controlsystem1 = ControlSystem.ControlSystem(reactorqueue1, receiverQueue1)
        controlsystem2 = ControlSystem.ControlSystem(reactorqueue2,receiverQueue2)


        pr = Process(target=reactor.runNuclearReactor)
        pc1 = Process(target=controlsystem1.runNuclearReactor)
        pc2 = Process(target=controlsystem2.runNuclearReactor)

        #Start the reactor
        pr.start()
        #Start the two control systems
        pc1.start()
        pc2.start()

        while True:
            data1 = ""
            data2 = ""

            #Get control instructions from the control system processes
            #If one of them is dead for more than 5 time units, restart them.
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
            #If Control System 1 is available use that data otherwise
            #Use Control System 2 data.
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

