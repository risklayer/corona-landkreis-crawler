#!/usr/bin/python3
## Tommy
from botbase import *

_stendal_s = re.compile(r"stationär:\s*([0-9.]+)")
_stendal_i = re.compile(r"ITS:\s*([0-9.]+)")

def stendal(sheets):
    soup = get_soup("https://www.landkreis-stendal.de/de/corona-nachrichten/informationen-zur-lage-coronavirus-im-landkreis-stendal.html")
    date_text = soup.find("div", {"class":"text-muted article-date mt-2"}).get_text().strip()
    check_date(date_text, "Stendal")
    rows = [[x.text.strip() for x in row.findAll("td")] for row in soup.find("table").findAll("tr")]
    # C,D vom LAND
    s = sum(map(force_int, _stendal_s.findall(rows[1][1])))
    i = sum(map(force_int, _stendal_i.findall(rows[1][1])))
    update(sheets, 15090, c=None, s=s, i=i, sig="", comment="LK", without_c=True)
    return True

schedule.append(Task(14, 56, 16, 56, 360, stendal, 15090))
if __name__ == '__main__': stendal(googlesheets())
