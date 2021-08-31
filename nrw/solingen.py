#!/usr/bin/python3
from botbase import *

_solingen_c = re.compile(r"([0-9.]+) bestätigte")
_solingen_d = re.compile(r"([0-9.]+) mit dem Virus infizierte Menschen sind bisher verstorben")
_solingen_g = re.compile(r"([0-9.]+) Menschen sind wieder genesen")
_solingen_s = re.compile(r"([0-9.]+) Patient")
_solingen_q = re.compile(r"In Quarantäne befinden sich derzeit insgesamt ([0-9.]+) Personen")

def solingen(sheets):
    soup = get_soup("https://www.solingen.de/de/inhalt/coronavirus-statistik/")
    main = soup.find("main").find("article")
    ps = [p.text for p in main.findAll("p")]
    #print(ps)
    if not today().strftime("%d.%m.") in ps[0]: raise NotYetAvailableException("Solingen noch alt:" + rows[0][1])
    args=dict()
    for p in ps:
        m = _solingen_c.search(p)
        if m: args["c"] = force_int(m.group(1))
        m = _solingen_d.search(p)
        if m: args["d"] = force_int(m.group(1))
        m = _solingen_g.search(p)
        if m: args["g"] = force_int(m.group(1))
        m = _solingen_s.search(p)
        if m: args["s"] = force_int(m.group(1))
        m = _solingen_q.search(p)
        if m: args["q"] = force_int(m.group(1))
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    update(sheets, 5122, **args, sig="Bot")
    return True

schedule.append(Task(11, 2, 20, 35, 600, solingen, 5122))
if __name__ == '__main__': solingen(googlesheets())
