#!/usr/bin/python3
from botbase import *

def oberspreewald(sheets):
    soup = get_soup("https://www.osl-online.de/seite/447426/informationen-zum-coronavirus.html")
    main = soup.find(id="content")
    cap = main.find("small").text
    if not today().strftime("%d.%m.%Y") in cap: raise NotYetAvailableException("Oberspreewald noch alt:" + cap)
    args=dict()
    a, q = None, None
    for row in main.findAll("tr"):
        row = [x.text.strip() for x in row.findAll("td")]
        if len(row) != 2: continue
        # print(row, force_int(row[1]))
        if "bestätigt" in row[0]: args["c"] = force_int(row[1])
        if "Neufälle" in row[0]: args["cc"] = force_int(row[1])
        if "Genesene" in row[0]: args["g"] = force_int(row[1])
        if "Sterbefälle" in row[0]: args["d"] = force_int(row[1])
        if "stationär" in row[0]: args["s"] = force_int(row[1])
        if "aktuell" in row[0]: a = force_int(row[1])
        if "Quarant" in row[0]: q = int(re.search(r"(\d+)", row[1]).group(1))
    if a is not None and q is not None: args["q"] = a + q
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    update(sheets, 12066, **args, sig="Bot")
    return True

schedule.append(Task(10, 2, 12, 35, 600, oberspreewald, 12066))
if __name__ == '__main__': oberspreewald(googlesheets())
