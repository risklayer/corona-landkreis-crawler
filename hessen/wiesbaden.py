#!/usr/bin/python3
from botbase import *

_wiesbaden_c = re.compile(r"([0-9.]+) positiv getestete")
_wiesbaden_d = re.compile(r"([0-9.]+) Menschen sind verstorben")
_wiesbaden_g = re.compile(r"([0-9.]+) Personen gelten nach den RKI-Kriterien als genesen")
_wiesbaden_s = re.compile(r"([0-9.]+) Patient")
_wiesbaden_q = re.compile(r"In Quarantäne befinden sich insgesamt ([0-9.]+) Personen")

def wiesbaden(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.wiesbaden.de/leben-in-wiesbaden/gesundheit/gesundheitsfoerderung/coronafallzahlen.php")
    main = soup.find(id="SP-content")
    ps = [p.text for p in main.findAll(["p", "strong", "li"])]
    #for p in ps: print(p)
    if not any([today().strftime("%d. %B %Y") in p for p in ps]): raise NotYetAvailableException("Wiesbaden noch alt: " + " ".join(ps[:3]))
    args=dict()
    for p in ps:
        m = _wiesbaden_c.search(p)
        if m: args["c"] = force_int(m.group(1))
        m = _wiesbaden_d.search(p)
        if m: args["d"] = force_int(m.group(1))
        m = _wiesbaden_g.search(p)
        if m: args["g"] = force_int(m.group(1))
        m = _wiesbaden_s.search(p)
        if m: args["s"] = force_int(m.group(1))
        m = _wiesbaden_q.search(p)
        if m: args["q"] = force_int(m.group(1))
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    if "q" in args: args["q"] += args["c"] - args["d"] - args["g"]
    update(sheets, 6414, **args, sig="Bot")
    return True

schedule.append(Task(15, 0, 20, 35, 600, wiesbaden, 6414))
if __name__ == '__main__': wiesbaden(googlesheets())
