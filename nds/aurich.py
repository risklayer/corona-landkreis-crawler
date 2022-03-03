#!/usr/bin/python3
from botbase import *

_stand = re.compile(r"Aktualisiert:")

def aurich(sheets):
    soup = get_soup("https://www.landkreis-aurich.de/fileadmin/ftp-upload/Uebersicht.htm")
    date = soup.find(text=_stand)
    #if not today().strftime("%d.%M.%Y") in date: raise NotYetAvailableException("Aurich noch alt: " + date)
    date = check_date(date.split(" ",2)[1], "Aurich")
    args = dict()
    for row in soup.findAll("tr"):
        row = [x.get_text(" ") for x in row.findAll(["td","th"])]
        #print(row)
        if len(row) < 2: continue
        if "Gesamtanzahl" in row[0]: args["c"] = force_int(row[1])
        if "zum Vortag" in row[1]: args["cc"] = force_int(re.search("([+-]?\s*[0-9.]+)", row[1]).group(1))
        if "Genesene" in row[0]: args["g"] = force_int(row[1])
        if "Verstorbene" in row[0]: args["d"] = force_int(row[1])
        if "Quarantäne" in row[0]: args["q"] = force_int(row[1])
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    update(sheets, 3452, **args, sig="Bot", ignore_delta=False)
    return True

schedule.append(Task(10, 2, 14, 35, 600, aurich, 3452))
if __name__ == '__main__': aurich(googlesheets())
