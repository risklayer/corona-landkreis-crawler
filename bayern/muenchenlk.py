#!/usr/bin/python3
from botbase import *

def muenchenlk(sheets):
    soup = get_soup("https://www.landkreis-muenchen.de/themen/verbraucherschutz-gesundheit/gesundheit/coronavirus/fallzahlen/")
    main = soup.find(class_="maincontent")
    #print(main.get_text(" "))
    h2 = main.find(text=re.compile(r"Stand:"))
    if not today().strftime("%d.%m.%Y") in h2: raise NotYetAvailableException("München noch alt: " + h2)
    args=dict()
    for row in main.findAll("tr"):
        row = [td.get_text(" ") for td in row.findAll("td")]
        #print(row)
        if "Gemeldete Fälle seit" in row[0]: args["cc"] = force_int(row[1])
        if "Streichungen" in row[0]: args["cm"] = force_int(row[1])
        if "Gemeldete Fälle insgesamt" in row[0]: args["c"] = force_int(row[1])
        if "genesen" in row[0]: args["g"] = force_int(row[1])
        if "Todesfälle gesamt" in row[0]: args["d"] = force_int(row[1])
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    comment = "Bot"
    if "cm" in args:
        if args["cm"] is not None and args["cm"] > 0: comment = "C-%d Streichungen Bot" % args["cm"]
        del args["cm"]
    update(sheets, 9184, **args, sig="Bot", comment=comment, ignore_delta=True)
    return True

schedule.append(Task(15, 6, 17, 35, 360, muenchenlk, 9184))
if __name__ == '__main__': muenchenlk(googlesheets())
