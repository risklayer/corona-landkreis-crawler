#!/usr/bin/python3
from botbase import *

def cham(sheets):
    d = today().strftime("%d.%m.%Y")
    data = get_json("https://coronainfo.landkreis-cham.de/manage/api/index.php?mode=faelle")
    data = next(x for x in data["data_chart"] if x["date"] == d)
    #print(*data.items(), sep="\n")
    date = check_date(data["date"], "Cham")
    s = int(data["stationaer"])
    i = int(data["intensiv"])
    data = get_json("https://coronainfo.landkreis-cham.de/manage/api/index.php?mode=inzidenz")
    g = int(data["data_sum"]["genesen"])
    update(sheets, 9372, c=None, g=g, s=s, i=i, without_c=True, comment="RKI CD, Bot")
    return True

schedule.append(Task(9, 2, 10, 35, 600, cham, 9372))
if __name__ == '__main__': cham(googlesheets())
