Nuclear Reactor Simulator
===================
----
Description
------------
>A simple simulator for a nuclear reactor control system to demonstrate some of the architectural quality attributes and tactics that can be used in a safety critical system.
>**Frameworks used:**

> - Python 2.7
> - Python *multiprocessing* module

Instructions
------------

> Python 2.7 is required.
> Run the following in the terminal:
> `python HBReceiver.py`

Design
--------------

System consists of three main processes:

 1. Reactor
 2. HBReceiver
 3. ControlSystem 

>**Reactor**
> Simulates the core reactor, generating random values for core temperature and safety valve status. If temperature goes too high or safety valves are compromised control rods need to be dropped to decrease fission in the reactor.


>**ControlSystem**
>Simulates the control system for the control rods in the core reactor. It is the safety critical process of the entire nuclear reactor system, as failure to lower the control rods may result in fission going out of hand with catastrophic consequences.

>**HBReactor**
>The moderator of the system. It monitors the ControlSystem and reacts accordingly to the status of the process. Primary responsibilities include synchronizing between redundant ControlSystem processes and performing fault recovery for ControlSystem.

Architectural Quality Attributes
------------

> Quality attribute that have been implemented so far in this project
> are:
> 
>  - Availibility
> 
> Tactics used are:
> 
> - **Fault Detection**:
> 	- *Heartbeat Tactic*
>      - *ControlSystem* process sends control order and data to the *HBReceiver* and that is counted as a heartbeat for the receiver.
>      - If the heartbeat is not received for around 5 time units, *HBReceiver* restarts the *ControlSystem*
> - Fault Recovery:
> 	- Active Redundancy
>      - At any given moment there are two *ControlSystem* processes running and reacting the *Reactor* generated data.
>      - If one of the processes fail, *HBReceiver* uses the other process until the failed process is restarted again.

