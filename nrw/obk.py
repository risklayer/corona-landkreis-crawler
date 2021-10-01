#!/usr/bin/python3
from botbase import *

def obk(sheets):
    soup = get_soup("https://www.obk.de/cms200/aktuelles/sars/aktfall/index.shtml")
    main = soup.find(id="main")
    rows = main.findAll("tr")
    args=dict()
    for row in rows:
        row = [x.text for x in row.findAll(["th","td"])]
        if len(row) != 3: continue
        if "Stand:" in row[2]: args["date"] = check_date(row[2].strip().split("\n")[1].strip().rstrip(","), "OBK")
        if "Positiv getestete Personen" in row[0]:
            args["c"] = force_int(row[2])
            args["cc"] = args["c"] - force_int(row[1])
        if "genesene Personen" in row[0]:
            args["g"] = force_int(row[2])
            args["gg"] = args["g"] - force_int(row[1])
        if "Todesfälle" in row[0]:
            args["d"] = force_int(row[2])
            args["dd"] = args["d"] - force_int(row[1])
        if "Quarantäne" in row[0]: args["q"] = force_int(row[2])
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    assert "date" in args
    update(sheets, 5374, **args, sig="Bot", comment="Bot ohne SI", ignore_delta=today().weekday()==0)
    return True

schedule.append(Task(10, 30, 12, 35, 600, obk, 5374))
if __name__ == '__main__': obk(googlesheets())
