#!/usr/bin/python3
from botbase import *

def warendorf(sheets):
    data = get_json("https://geoportal.kreis-warendorf.de/geoportal/snippets/corona/data/confirmed.json")
    data = [x for x in data if x["region"] == "Kreis Warendorf"]
    d1, d2 = data[-2:]
    #print(d1, d2)
    date = check_date(d2["datetime"], "Warendorf")
    c, cc = int(d2["confirmed"]), int(d2["new"])
    g, d = int(d2["recovered"]), int(d2["death"])
    gg, dd = g - int(d1["recovered"]), d - int(d1["death"])
    update(sheets, 5570, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, sig="Bot", comment="Bot ohne SI", ignore_delta="mon")
    return True

schedule.append(Task(9, 2, 12, 35, 600, warendorf, 5570))
if __name__ == '__main__': warendorf(googlesheets())
