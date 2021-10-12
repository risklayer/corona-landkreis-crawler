#!/usr/bin/python3
from botbase import *

_duispat = re.compile(r"Stand: *(\d\d?\.\d\d?\.20\d\d,? \d\d?:\d\d)")
_duisnum = re.compile(r"([0-9.]+)\s*\(\+?(-?[0-9]+)\)")

def duisburg(sheets):
    soup = get_soup("https://co-du.info/")
    main = soup.find(class_="spalte-1")
    h4 = main.find(text=re.compile(r"Stand"))
    date = check_date(_duispat.search(h4).group(1), "Duisburg", datetime.timedelta(hours=12))
    args,tmp=dict(), dict()
    for row in main.findAll("td"):
        row = (row.find("h4"), row.find("h3"))
        if row[0] is None or row[1] is None: continue
        row = (row[0].text.strip(), row[1].text.strip())
        #print(row)
        if "Bestätigte" in row[0]: args["c"], args["cc"] = map(force_int, _duisnum.search(row[1]).groups())
        if "Genesen" in row[0]: args["g"], args["gg"] = map(force_int, _duisnum.search(row[1]).groups())
        if "Verstorben" in row[0]: args["d"], args["dd"] = map(force_int, _duisnum.search(row[1]).groups())
        if "Aktuell Infiziert" in row[0]: tmp["a"] = force_int(_duisnum.search(row[1]).group(1))
        if "Kontaktpersonen" in row[0]: tmp["k"] = force_int(row[1])
        if "In Intensiv" in row[0]: args["i"] = force_int(row[1])
        # TODO: Impfungen auch?
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    args["q"] = tmp.get("a",0) + tmp.get("k",0)
    update(sheets, 5112, **args, sig="Bot")
    return True

schedule.append(Task(9, 2, 15, 35, 600, duisburg, 5112))
if __name__ == '__main__': duisburg(googlesheets())
