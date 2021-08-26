#!/usr/bin/python
import botbase
import random, time
from datetime import datetime
from heapq import heapify, heapreplace

import sh, berlin, hamburg, nds, bremen, nrw, hessen, rlp, bw, bayern, sachsen

def scheduler(sheets):
    queue = [(task.next_time("init"), task) for task in botbase.schedule]
    heapify(queue)
    while True:
        botbase.todaystr = time.strftime("%d.%m.%Y") # update today value
        nextex, task = queue[0] # peek() heap
        delay = (nextex - datetime.now()).total_seconds()
        if delay > 0:
            delay += random.random() * 2 # reduce collissions when running multiple times
            print("Waiting for %d seconds for AGS %05d %s at %s" % (delay, task.ags, task.fun.__name__, nextex))
            time.sleep(delay)
        success = task.run(sheets)
        heapreplace(queue, (task.next_time(success), task))

if __name__ == '__main__': scheduler(botbase.googlesheets())
