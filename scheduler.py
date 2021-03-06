#!/usr/bin/python
import botbase
import random, time, sys
from datetime import datetime
from heapq import heapify, heapreplace, heappop

import sh, hamburg, nds, bremen, nrw, hessen, rlp, bw, bayern, saarland, berlin, brandenburg, sachsen, sanhalt, thueringen

def scheduler(sheets):
    queue = [(task.next_time("init"), task) for task in botbase.schedule]
    if "--all" in sys.argv: queue = [(datetime.now(), task) for task in dict([(x.fun, x) for x in botbase.schedule]).values()]
    heapify(queue)
    while len(queue) > 0:
        #botbase.todaystr = time.strftime("%d.%m.%Y") # update today value
        nextex, task = queue[0] # heap.peek()
        delay = (nextex - datetime.now()).total_seconds()
        if delay > 0:
            delay = delay + random.random() * 15 # reduce collissions when running multiple times
            print("Waiting for %d seconds for AGS %05d %s at %s" % (delay, task.ags, task.fun.__name__, nextex))
            time.sleep(delay)
        success = task.run(sheets)
        if "--once" in sys.argv:
            heappop(queue)
            time.sleep(.1)
            continue # don't reschedule
        heapreplace(queue, (task.next_time(success), task))

if __name__ == '__main__': scheduler(botbase.googlesheets())
