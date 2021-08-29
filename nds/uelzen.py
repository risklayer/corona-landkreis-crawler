#!/usr/bin/python3
from botbase import *

_uelzen_c = re.compile(r"insgesamt bestätigten Fälle nunmehr bei ([0-9.]+)")
_uelzen_d = re.compile(r"([0-9.]+) verstorben")
_uelzen_g = re.compile(r"([0-9.]+) Menschen, bei denen das Virus bisher nachgewiesen wurde, sind wieder genesen")
_uelzen_s = re.compile(r"([0-9.]+|\w+) Personen mit oder wegen COVID-19")
_uelzen_q = re.compile(r"In häuslicher Quarantäne befinden sich ([0-9.]+) Personen")

def uelzen(sheets):
    soup = get_soup("https://www.landkreis-uelzen.de/home/soziales-familie-und-gesundheit/gesundheit/corona-virus/corona-update.aspx")
    main = soup.find(id="ctl01_contentpane").find(class_="description")
    if not today().strftime("%d.%m.%Y") in main.find("u").text: raise NotYetAvailableException("Uelzen noch alt:" + main.find("u").text)
    ps = [p.text for p in main.findAll("p")]
    #print(ps)
    args=dict()
    for p in ps:
        m = _uelzen_c.search(p)
        if m: args["c"] = force_int(m.group(1))
        m = _uelzen_d.search(p)
        if m: args["d"] = force_int(m.group(1))
        m = _uelzen_g.search(p)
        if m: args["g"] = force_int(m.group(1))
        m = _uelzen_s.search(p)
        if m: args["s"] = force_int(m.group(1))
        m = _uelzen_q.search(p)
        if m: args["q"] = force_int(m.group(1))
    assert "c" in args and "d" in args and "g" in args
    update(sheets, 3360, **args, sig="Bot")
    return True

schedule.append(Task(15, 2, 20, 35, 600, uelzen, 3360))
if __name__ == '__main__': uelzen(googlesheets())
