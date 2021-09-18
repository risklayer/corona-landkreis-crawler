#!/usr/bin/python3
from botbase import *

def grossgerau(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.kreisgg.de/gesundheit/corona-krise-info-und-hotlines/")
    content = soup.find(id="rspeaker")
    ps = [x.get_text(" ") for x in content.findAll("h2")]
    #for p in ps: print(p)
    if not any(today().strftime("Stand: %d. %B %Y") in p for p in ps): raise NotYetAvailableException("Gross-Gerau noch alt: " + next(p for p in ps if "Stand:" in p))
    rows = content.find("table").findAll("tr")
    rows = [[x.text.strip() for x in row.findAll(["td","th"])] for row in rows]
    #print(rows)
    args=dict()
    for row in rows:
        if "Gesamt" in row[0]: args["c"] = force_int(row[1].split(" ")[0])
        if "Gesamt" in row[0]: args["cc"] = force_int(row[1].split(" ")[1].strip("("))
        if "Genesen" in row[0]: args["g"] = force_int(row[1])
        if "Todesfälle" in row[0]: args["d"] = force_int(row[1])
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    update(sheets, 6433, **args, sig="Bot", ignore_delta=today().weekday()==0) # delta am Montag
    return True

schedule.append(Task(12, 0, 14, 35, 360, grossgerau, 6433))
if __name__ == '__main__': grossgerau(googlesheets())
