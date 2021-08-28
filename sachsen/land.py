#!/usr/bin/python3
from botbase import *
import re, time
_sachsen = re.compile(r"coronavirus.sachsen.de").search

def sachsen(sheets):
    # url = "https://www.coronavirus.sachsen.de/infektionsfaelle-in-sachsen-4151.html"
    data = get_json("https://www.coronavirus.sachsen.de/corona-statistics/rest/stateOfDataApi.jsp")
    date = check_date(data["lastUpdate"], "Sachsen")
    #updated = dateutil.parser.isoparse(data.get("lastUpdate"))
    #if updated.date() != datetime.date.today(): raise Exception("Sachsen noch alt? " + str(updated))
    #updated = updated.strftime("%d.%m.%Y %H:%M")

    data = get_json("https://www.coronavirus.sachsen.de/corona-statistics/rest/infectionOverview.jsp")
    batch=[]
    for ags, v in data.items():
        ags = int(ags)
        if ags == 14: continue # Land. Unten G ausfüllen?
        # print(ags, v)
        c, cc, d, dd = v["totalInfections"], v["infectionsDifferenceToYesterday"], v["totalDeaths"], v["deathsDifferenceToYesterday"]
        update(sheets, ags, c=c, cc=cc, d=d, dd=dd, sig="Land", comment="Bot", date=date, check=_sachsen, batch=batch)
        time.sleep(5)
    do_batch(sheets, batch)
    return True

schedule.append(Task(13, 30, 16, 00, 300, sachsen, 14730))
if __name__ == '__main__': sachsen(googlesheets())
