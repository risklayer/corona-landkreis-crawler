#!/usr/bin/python3
from botbase import *

def borken(sheets):
    data = get_json("https://corona.kreis-borken.de/api/incidents")
    assert "24:00" in data["STAND"]
    date = dateutil.parser.parse(data["STAND"].split(" ")[0], dayfirst=True) + datetime.timedelta(days=1) # 24:00
    date = check_date(date, "Borken")
    data = get_json("https://corona.kreis-borken.de/api/data")[0]
    #for k,v in data.items(): print(k,v,sep="\t")
    c, cc = data["INFIZIERTE_SUM"], force_int(data["INFIZIERTE"])
    d, dd = data["VERSTORBENE_SUM"], force_int(data["VERSTORBENE"])
    g, gg = data["GESUNDETE_SUM"], force_int(data["GESUNDETE"])
    update(sheets, 5554, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(9, 0, 10, 30, 360, borken, 5554))
if __name__ == '__main__': borken(googlesheets())
