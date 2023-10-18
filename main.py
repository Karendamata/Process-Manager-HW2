####################################################
# Written by Karen da Mata as a homework project for 
# Operating Systems Class

####################################################

# Simulate content switching conducted by OS Process Manager. 
# Context switching between Ready and Run states, saves the state of the currently running process from CPU to PCB 
# and restores the state of the newly scheduled process from PCB to CPU. 
# Test your Process Manager on my file “ece565hw02.txt”.

from threading import Timer
import time
import datetime as dt
import pandas as pd

def Queues(PCBs): 
    ReadyQueue = []
    RunningQueue = []
    BlockedQueue = []
    CompletedQueue = []
    for column in PCBs.columns:
        if PCBs[column]['State'] == 'Ready':
             ReadyQueue.append(column)
        elif PCBs[column]['State'] == 'Running':
            RunningQueue.append(column)
        else:
            BlockedQueue.append(column)
    return {"Ready: ": ReadyQueue, "Running: ": RunningQueue, "Blocked: ": BlockedQueue, "Completed: ": CompletedQueue}

def RuntoReady(PCBs, CurrentQueue):
    if len(CurrentQueue['Running: '])!=0: # Checking if there's any process running
        st = time.time()
        run_to_ready = CurrentQueue['Running: '].pop(0) # removing process index of running queue
        PCBs[run_to_ready]['State'] = 'Ready' # updating process state to ready (at this point, no information needed for block state)
        CurrentQueue['Ready: '].append(run_to_ready) # moving process index to ready queue
        et = time.time()
        print("PID "+PCBs[run_to_ready]['PID']+" took "+str(st - et)+" seconds to run.") # printing how long it took for the process to run

def ReadytoRun(PCBs, CurrentQueue):
    if len(CurrentQueue['Ready: '])!=0: # Checking if there's any process ready
        ready_to_run = CurrentQueue['Ready: '].pop(0) # removing process index of ready queue
        PCBs[ready_to_run]['State'] = 'Running' # updating process state to running
        CurrentQueue['Running: '].append(ready_to_run)

def ProcessManager(epochs, PCBs, queues):
    for epoch in range(epochs):
        print("Epoch #: ", epoch)

        print("Initial Processes: \n", PCBcount)
        print("\n Initial queues: ", queues)

        print("\n After running an epoch: \n")
        RuntoReady(PCBs, queues)
        ReadytoRun(PCBs, queues)
        print(PCBcount)

        print("\n Current queues: ", queues)

        print("\n ########################")


file_path = 'ece565hw02.txt'

file = open(file_path)
PCBcount = [[]]  # to store PCBs
i = 0 # to count the number of PCBs

for line in file.readlines():
  if (line == '# Process mgmt info\n'): # Line that indicates a new PCB information is starting
    PCBcount.append([]) # initializying an empty PCB to store the information that from the next lines
    i+=1 # adding to the PCB counter
    continue
  elif (':' in line): # : indicates that some informationg from the PCB is in this line
    line = line[line.find(': ') + 2:line.find('\n')] # getting information after : and before \n
    PCBcount[i].append(line.replace(" ","")) # appending line and removing whitespaces
  else:
    continue # any other line, nothing needs to be store

dict_keys = ['State', 'PID', 'pPID', 'PC/IP',
             'AX', 'BX', 'CX', 'DX',
             'SP', 'BP', 'SI', 'DI',
             'Priority', 'Quantum', 'Burst',
             'CS', 'DS', 'SS', 'ES',
             'FP', 'Start time', 'CPU used'] # defining keys of PCB to store in a dictionary for easier access

for index, PCB in enumerate(PCBcount): # transforming lines of file to a dictonary format
  if index!=0: #checking if list isn't empty
    PCB_dict = dict()
    for i in range(len(dict_keys)):
      PCB_dict[dict_keys[i]] = PCB[i]
    PCBcount[index] = PCB_dict

PCBcount = pd.DataFrame(PCBcount[1:], index=range(1, len(PCBcount))).T # Transforming PCBs information to a pandas dataframe for better visualization

# Initializing four queues for four PCB states
currentQueues = Queues(PCBcount)

ProcessManager(4, PCBcount, currentQueues) # simulating process manager for 4 epochs