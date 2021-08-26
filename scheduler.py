#!/usr/bin/python
import botbase
from botbase import *
from datetime import date, datetime, timedelta
from heapq import heapify, heapreplace
import random, time

from rlp import rlp
from lgl import lgl
from sh import sh
from sachsen import sachsen
import berlin, hamburg, nds, bremen, nrw

# TODO: wochenende...
# TODO: in die jeweiligen methoden (besser wären klassen) verschieben?
#botbase.schedule.append(Task(9, 0, 10, 0, 300, berlin, 11000))
#botbase.schedule.append(Task(11, 55, 12, 30, 120, hamburg, 2000))
botbase.schedule.append(Task(14, 00, 15, 00, 120, lgl, 9774))
botbase.schedule.append(Task(14, 00, 15, 00, 120, rlp, 7134))
botbase.schedule.append(Task(19, 00, 22, 00, 180, sh, 1057))
botbase.schedule.append(Task(13, 30, 16, 00, 300, sachsen, 14730))
#botbase.schedule.append(Task(16, 15, 18, 30, 300, bremen, 4011))
#botbase.schedule.append(Task(10, 5, 20, 30, 3600, wuppertal, 5124))
#botbase.schedule.append(Task(8, 10, 10, 10, 1800, essen, 5113))
#botbase.schedule.append(Task(11, 30, 13, 30, 180, coesfeld, 5558))

def scheduler(sheets):
    # Plan next executions
    global schedule # from botbase
    queue = [(task.next_time("init"), task) for task in botbase.schedule]
    heapify(queue)
    while True:
        botbase.todaystr = time.strftime("%d.%m.%Y") # update today value
        nextex, task = queue[0] # peek() heap
        print(nextex, task)
        delay = (nextex - datetime.now()).total_seconds()
        if delay > 0:
            delay += random.random() * 2 # reduce collissions when running multiple times
            print("Waiting for %d seconds for AGS %05d %s at %s" % (delay, task.ags, task.fun.__name__, nextex))
            time.sleep(delay)
        success = task.run(sheets)
        heapreplace(queue, (task.next_time(success), task))

def main():
    sheets = build('sheets', 'v4', credentials=authorize()).spreadsheets()
    scheduler(sheets)

if __name__ == '__main__':
    main()
