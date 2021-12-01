#!/usr/bin/python3
from botbase import *

_garmisch_c = re.compile(r"([0-9.]+) *positiv")
_garmisch_g = re.compile(r"([0-9.]+) *Personen sind genesen")
_garmisch_d = re.compile(r"bedauern wir *([0-9.]+) *\(intern\)")
_garmisch_s = re.compile(r"Hospitalisierte Personen: *([0-9.]+)")
_garmisch_i = re.compile(r"Intensiv behandelte Personen: *([0-9.]+)")

def garmisch(sheets):
    soup = get_soup("https://www.lra-gap.de/de/corona-fallzahlen-und-impf-fortschritt.html")
    main = soup.find(class_="content")
    ps = [p.get_text(" ") for p in main.findAll("p")]
    #for p in ps: print(p)
    h2 = [x for x in ps if "Stand" in x][0]
    if not today().strftime("%d.%m.%Y") in h2: raise NotYetAvailableException("Garmisch noch alt: " + h2)
    args=dict()
    for p in ps:
        m = _garmisch_c.search(p)
        if m: args["c"] = force_int(m.group(1))
        m = _garmisch_d.search(p)
        if m: args["d"] = force_int(m.group(1))
        m = _garmisch_g.search(p)
        if m: args["g"] = force_int(m.group(1))
        m = _garmisch_s.search(p)
        if m: args["s"] = force_int(m.group(1))
        m = _garmisch_i.search(p)
        if m: args["i"] = force_int(m.group(1))
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    update(sheets, 9180, **args, sig="Bot")
    return True

schedule.append(Task(15, 7, 19, 35, 360, garmisch, 9180))
if __name__ == '__main__': garmisch(googlesheets())
