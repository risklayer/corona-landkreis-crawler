#!/usr/bin/python3
from botbase import *
import re
_sachsen = re.compile(r"coronavirus.sachsen.de").search

def sachsen(sheets):
    import dateutil.parser, datetime
    # url = "https://www.coronavirus.sachsen.de/infektionsfaelle-in-sachsen-4151.html"
    data = get_json("https://www.coronavirus.sachsen.de/corona-statistics/rest/stateOfDataApi.jsp")
    updated = dateutil.parser.isoparse(data.get("lastUpdate"))
    if updated.date() != datetime.date.today(): raise Exception("Sachsen noch alt? " + str(updated))
    updated = updated.strftime("%d.%m.%Y %H:%M")

    data = get_json("https://www.coronavirus.sachsen.de/corona-statistics/rest/infectionOverview.jsp")
    for ags, v in json.loads(data).items():
        ags = int(ags)
        if ags == 14: continue # Land. Unten G ausfüllen?
        # print(ags, v)
        c, cc, d, dd = v["totalInfections"], v["infectionsDifferenceToYesterday"], v["totalDeaths"], v["deathsDifferenceToYesterday"]
        update(sheets, ags, c=c, cc=cc, d=d, dd=dd, sig="Land", comment="Bot", check=_sachsen)
    return True

schedule.append(Task(13, 30, 16, 00, 300, sachsen, 14730))
if __name__ == '__main__': sachsen(googlesheets())
