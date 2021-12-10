#!/usr/bin/python3
from botbase import *

_stand = re.compile(r"Stand (\d\d.\d\d.20\d\d)")
_match_two = re.compile(r"\s*([0-9.]+)\s*(?:\(([+-]?[0-9.]*)\))?\s*", re.U | re.M)

def wittmund(sheets):
    soup = get_soup("https://corona.landkreis-wittmund.de/")
    content = soup.find(class_="main-content-area")
    date = content.find("h1").get_text()
    date = check_date(_stand.search(date).group(1),"Wittmund")
    rows = [[x.get_text() for x in y.findAll(["td","th"])] for y in content.findAll("tr")]
    #print(*rows, sep="\n")
    c, cc, d, dd, g, q = None, None, None, None, None, None
    for row in rows:
        if "Bestätigte Fälle" in row[0]: c, cc = map(force_int, _match_two.match(row[1]).groups())
        if "verstorbene" in row[0]: d, dd = map(force_int, _match_two.search(row[1]).groups())
        if "genesene" in row[0]: g = force_int(row[1])
        if "Quarantäne" in row[0]: q = force_int(row[1])
    if q is not None: q += c - d - g
    update(sheets, 3462, c=c, cc=cc, d=d, dd=dd, g=g, q=q, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(10, 20, 15, 35, 360, wittmund, 3462))
if __name__ == '__main__': wittmund(googlesheets())
