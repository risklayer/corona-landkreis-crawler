#!/usr/bin/python3
from botbase import *

_augsburg_c = re.compile(r"Insgesamt: ([0-9.]+)")
_augsburg_cc = re.compile(r"(-?[0-9.]+) Neuinfektionen")
_augsburg_d = re.compile(r"Davon verstorben: ([0-9.]+)")
_augsburg_g = re.compile(r"Davon genesen: ([0-9.]+)")

def augsburg(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.augsburg.de/umwelt-soziales/gesundheit/coronavirus/fallzahlen")
    main = soup.find(role="main")
    h2 = main.find(text=re.compile(r"Stand:"))
    if not today().strftime("%-d. %B %Y") in h2: raise NotYetAvailableException("Augsburg noch alt:" + h2)
    ps = [p.text for p in main.findAll("p")]
    #print(ps)
    args=dict()
    for p in ps:
        m = _augsburg_c.search(p)
        if m: args["c"] = force_int(m.group(1))
        m = _augsburg_d.search(p)
        if m: args["d"] = force_int(m.group(1))
        m = _augsburg_g.search(p)
        if m: args["g"] = force_int(m.group(1))
        m = _augsburg_cc.search(p)
        if m: args["cc"] = force_int(m.group(1))
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    update(sheets, 9761, **args, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(9, 33, 13, 35, 600, augsburg, 9761))
if __name__ == '__main__': augsburg(googlesheets())
