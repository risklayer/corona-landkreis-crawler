#!/usr/bin/python3
from botbase import *

_stand = re.compile(r"Stand: \w+, (\d\d\.\d\d.20\d\d)")
_lahndill_a = re.compile(r"([0-9.]+)\s+aktive Corona-Fälle")
_lahndill_cc = re.compile(r"([0-9.]+)\s+Neuinfektionen")
_lahndill_c = re.compile(r"([0-9.]+)\s+Menschen mit dem Virus angesteckt")
_lahndill_d = re.compile(r"([0-9.]+)\s+Personen sind in Verbindung mit dem Virus verstorben")
_lahndill_g = re.compile(r"([0-9.]+)\s+Menschen gelten als genesen")
_lahndill_q = re.compile(r"([0-9.]+)\s+Kontaktpersonen")
_lahndill_si1 = re.compile(r"([0-9.]+)\s+Person(?:en)? stationär sowie\s+([0-9.]+)\s+Person(?:en)? auf der Intensiv", re.U)
_lahndill_s2 = re.compile(r"([0-9.]+)\s+Person(?:en)? stationär behandelt", re.U)

def lahndill(sheets):
    soup = get_soup("https://corona.lahn-dill-kreis.de/")
    main = soup.find(id="content")
    text = main.get_text(" ").strip()
    #print(text)
    date = main.find(text=_stand)
    #print(date)
    date = check_date(_stand.search(date).group(1), "Lahn-Dill")
    args=dict()
    a = force_int(_lahndill_a.search(text).group(1))
    args["cc"] = force_int(_lahndill_cc.search(text).group(1))
    #args["c"] = force_int(_lahndill_c.search(text).group(1))
    args["d"] = force_int(_lahndill_d.search(text).group(1))
    args["g"] = force_int(_lahndill_g.search(text).group(1))
    for m in _lahndill_si1.findall(text):
        args["s"] = args.get("s",0) + force_int(m[0]) + force_int(m[1])
        args["i"] = args.get("i",0) + force_int(m[1])
    for m in _lahndill_s2.findall(text):
        args["s"] = args.get("s",0) + force_int(m[0])
    args["q"] = force_int(_lahndill_q.search(text).group(1))
    assert "d" in args and "g" in args
    args["c"] = a + args["g"] + args["d"]
    assert "c" in args and "d" in args and "g" in args
    #print(args)
    update(sheets, 6532, **args, sig="Bot")
    return True

schedule.append(Task(13, 0, 16, 35, 600, lahndill, 6532))
if __name__ == '__main__': lahndill(googlesheets())
