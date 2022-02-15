#!/usr/bin/python3
from botbase import *

_twovals = re.compile(r"([0-9.]+)\s*\(\+?\s*(-?[0-9.]+)")
_stand = re.compile(r"Stand:")
_station = re.compile(r"befinde[nt]\s+sich\s+([.0-9]+|\w+)\s+Person(?:en)?\s+in\s+stationärer\s+Behandlung", re.U)

def leer(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.landkreis-leer.de/Leben-Lernen/Coronavirus")
    content = soup.find(id="vorlesen")
    date = content.find(text=_stand)
    if not today().strftime("%-d. %B %Y") in date: raise NotYetAvailableException("Leer noch alt: " + date)
    args = dict()
    for row in content.findAll("tr"):
        row = [x.get_text(" ") for x in row.findAll(["td","th"])]
        #print(row)
        if len(row) < 2: continue
        if "Bestätigte" in row[0]: args["c"], args["cc"] =  map(force_int, _twovals.search(row[1]).groups())
        if "genesene Personen" in row[0]: args["g"] = force_int(row[1])
        if "verstorbene Personen" in row[0]: args["d"] = force_int(row[1])
        if "Quarantäne" in row[0]: args["q"] = force_int(row[1])
    gen = content.find(text=re.compile(r"stationärer Behandlung",re.U)).parent
    #print(gen)
    if gen: args["s"] = force_int(_station.search(gen.get_text(" ")).group(1))
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    update(sheets, 3457, **args, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(10, 2, 14, 35, 360, leer, 3457))
if __name__ == '__main__': leer(googlesheets())
