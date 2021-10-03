#!/usr/bin/python3
from botbase import *

def bochum(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.bochum.de/Corona/Details-zu-den-aktuellen-Corona-Zahlen-in-Bochum")
    main = soup.find(id="par3600044514644979").parent
    h4 = main.find("h4").text
    if not today().strftime("%e. %B %Y") in h4: raise NotYetAvailableException("Bochum noch alt:" + h4)
    args=dict()
    for row in main.findAll("tr"):
        row = [x.text for x in row.findAll("td")]
        #print(row)
        if "Bestätigte" in row[0]: args["c"], args["cc"] = force_int(row[1]), force_int(row[2], 0)
        if "genesen" in row[0]: args["g"], args["gg"] = force_int(row[1]), force_int(row[2], 0)
        if "verstorben an" in row[0] or "verstorben mit" in row[0]:
            args["d"] = args.get("d",0) + force_int(row[1])
            args["dd"] = args.get("dd",0) + force_int(row[2], 0)
        if "stationär" in row[0]: args["s"] = force_int(row[1])
        if "intensiv" in row[0]: args["i"] = force_int(row[1])
        # TODO: Impfungen?
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    update(sheets, 5911, **args, sig="Bot")
    return True

schedule.append(Task(8, 2, 10, 35, 600, bochum, 5911))
if __name__ == '__main__': bochum(googlesheets())
