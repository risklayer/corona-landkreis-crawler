#!/usr/bin/python3
from botbase import *
import re, time
_sachsen = re.compile(r"coronavirus.sachsen.de").search

def sachsen(sheets):
    # url = "https://www.coronavirus.sachsen.de/infektionsfaelle-in-sachsen-4151.html"
    data = get_json("https://www.coronavirus.sachsen.de/corona-statistics/rest/stateOfDataApi.jsp")
    date = check_date(data["lastUpdate"], "Sachsen")
    data = get_json("https://www.coronavirus.sachsen.de/corona-statistics/rest/infectionOverview.jsp")
    todo=[]
    for ags, v in data.items():
        ags = int(ags)
        if ags == 14: continue # Land. Unten G ausfüllen?
        # print(ags, v)
        c, cc, d, dd = v["totalInfections"], v["infectionsDifferenceToYesterday"], v["totalDeaths"], v["deathsDifferenceToYesterday"]
        if ags == 14511: d,dd=None,None # Chemniz, use RKI D
        if ags == 14628: d += 6 # Sächsische Schweiz
        if ags == 14523: d += 27 # Vogtlandkreis
        #update(sheets, ags, c=c, cc=cc, d=d, dd=dd, sig="Land", comment="Land", date=date, check=_sachsen, batch=batch)
        todo.append([ags,c,cc,d,dd])
    rows = fetch_rows(sheets, [x[0] for x in todo])
    batch = []
    for i,x in enumerate(todo):
        ags,c,cc,d,dd = x
        update(sheets, ags, c=c, cc=cc, d=d, dd=dd, sig="Land", comment="Land", date=date, check=_sachsen, batch=batch, row=rows[i])
    do_batch(sheets, batch)
    return True

schedule.append(Task(13, 30, 16, 00, 300, sachsen, 14730))
if __name__ == '__main__': sachsen(googlesheets())
