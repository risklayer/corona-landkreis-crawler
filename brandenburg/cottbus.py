#!/usr/bin/python3
from botbase import *

_twonums = re.compile(r"\+?(-?\d+)\s*\(\+?\s*(-?\d+)\)")

def cottbus(sheets):
    soup = get_soup("http://www.cottbus.de/verwaltung/gb_iii/gesundheit/corona/index.html")
    main = soup.find(id="cbf_main")
    cap = main.find("caption").text
    if not today().strftime("%d.%m.%Y") in cap: raise NotYetAvailableException("Cottbus noch alt:" + cap)
    args=dict()
    for row in main.findAll("tr"):
        row = [x.text.strip() for x in row.findAll("td")]
        #print(row, _twonums.search(row[1]), force_int(row[1]))
        if len(row) != 2: continue
        if "bestätigt" in row[0]: args["c"] = force_int(row[1])
        if "zum Vortag" in row[0] and not "Verstorbene" in row[0]: args["cc"] = force_int(row[1])
        if "Verstorbene" in row[0]: args["d"], args["dd"] = map(force_int, _twonums.search(row[1]).groups())
        if "davon auf der ITS" in row[0]: args["s"], args["i"] = map(force_int, _twonums.search(row[1]).groups())
    #print(args)
    assert "c" in args and "d" in args
    update(sheets, 12052, **args, sig="Bot")
    return True

schedule.append(Task(10, 2, 15, 35, 600, cottbus, 12052))
if __name__ == '__main__': cottbus(googlesheets())
