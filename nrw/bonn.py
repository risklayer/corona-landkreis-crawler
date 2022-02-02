#!/usr/bin/python3
from botbase import *

def bonn(sheets):
    import locale
    soup = get_soup("https://www.bonn.de/themen-entdecken/gesundheit-verbraucherschutz/corona-zahlen.php")
    main = soup.find(id="SP-Content")
    h2 = main.find("h2", class_="SP-Headline--paragraph").text
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    if not today().strftime("%d. %B %Y") in h2: raise NotYetAvailableException("Bonn noch alt:" + h2)
    args, a = dict(), None
    for row in main.findAll("tr"):
        row = [x.text for x in row.findAll("td")]
        if "Positiv" in row[0]: args["c"] = force_int(row[1].split(" ")[0])
        if "Verstorben" in row[0]: args["d"] = force_int(row[1].split(" ")[0])
        if "genesen" in row[0]: args["g"] = force_int(row[1].split(" ")[0])
        if "Aktuell" in row[0]: a = force_int(row[1].split(" ")[0])
        if "Quarantäne" in row[0]: args["q"] = force_int(row[1].split(" ")[0])
        if "in Behandlung" in row[0]: args["s"] = force_int(row[1].split(" ")[0])
        if "Auf Intensiv" in row[0]: args["i"] = force_int(row[1].split(" ")[0])
        # TODO: Impfungen auch?
    #print(args)
    assert "c" in args and "d" in args
    if not "d" in args and a is not None: args["g"] = args["c"] - args["d"] - a
    update(sheets, 5314, **args, sig="Bot")
    return True

schedule.append(Task(10, 2, 11, 35, 600, bonn, 5314))
if __name__ == '__main__': bonn(googlesheets())
