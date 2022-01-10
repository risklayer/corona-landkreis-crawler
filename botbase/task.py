from .parse import NotYetAvailableException

class Task:
    def __init__(self, sh, sm, eh, em, interval, fun, ags):
        self.sh = sh
        self.sm = sm
        self.eh = eh
        self.em = em
        self.interval = interval
        self.fun = fun
        self.ags = ags

    def __lt__(self, other): return 0 # unordered
    def __str__(self): return "AGS %05d %s" % (self.ags, self.fun.__name__ if self.__class__ == Task else self.__class__.__name__)

    def run(self, sheets):
        from .sheets import is_signed
        import sys
        try:
            sig = is_signed(sheets, self.ags)
        except Exception as err:
            print(err)
            import traceback
            traceback.print_tb(err.__traceback__)
            return False # e.g., Google timeout
        if sig is not None and not sig == "RKI" and not (sig == "Land" and "--recheck" in sys.argv):
            print("Already filled", self)
            return True # "success"
        try:
            print("Running", self)
            return self.fun(sheets)
        except NotYetAvailableException as err:
            print(err)
            return False
        except Exception as err:
            print(err)
            # todo: use a custom Exception type for these "errors"
            if "noch alt" in str(err): return False
            if "noch nicht" in str(err): return False
            import traceback
            traceback.print_tb(err.__traceback__)
            return False

    def next_time(self, success):
        from datetime import date, datetime, timedelta
        today = date.today()
        end = datetime(year=today.year, month=today.month, day=today.day, hour=self.eh, minute=self.em)
        if success == "init":
            start = datetime(year=today.year, month=today.month, day=today.day, hour=self.sh, minute=self.sm)
            if end < datetime.now(): start += timedelta(days=1)
            return start
        if success: # tomorrow again
            today += timedelta(days=1)
            return datetime(year=today.year, month=today.month, day=today.day, hour=self.sh, minute=self.sm)
        # Not successful, try again after a delay:
        # TODO: increase the polling interval every time, reset each day?
        start = datetime.now() + timedelta(seconds=self.interval)
        if start < end: return start
        # reschedule tomorrow
        return datetime(year=today.year, month=today.month, day=today.day, hour=self.sh, minute=self.sm) + timedelta(days=1)

class Hourly(Task):
    def __str__(self): return "AGS %05d hourly %s" % (self.ags, self.fun.__name__ if self.__class__ == Hourly else self.__class__.__name__)
    def next_time(self, success):
        import datetime
        n = Task.next_time(self, success)
        if n.minute > 10: return n - datetime.timedelta(minutes=n.minute-5)
        return n

