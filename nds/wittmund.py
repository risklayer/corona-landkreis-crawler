#!/usr/bin/python3
from botbase import *

_stand = re.compile(r"Stand (\d\d.\d\d.20\d\d)")
_match_two = re.compile(r"\s*([0-9.]+)\s+\(([+-]?[0-9.]*)\)\s*", re.U | re.M)

def wittmund(sheets):
    soup = get_soup("https://corona.landkreis-wittmund.de/")
    content = soup.find(class_="main-content-area")
    date = content.find("h1").get_text()
    date = check_date(_stand.search(date).group(1),"Wittmund")
    rows = [[x.get_text() for x in y.findAll(["td","th"])] for y in content.findAll("tr")]
    #print(*rows, sep="\n")
    args = dict()
    for row in rows:
        if "Bestätigte Fälle" in row[0]: args["c"], args["cc"] = map(force_int, _match_two.match(row[1]).groups())
        if "verstorbene" in row[0]: args["d"] = force_int(row[1])
        if "genesene" in row[0]: args["g"] = force_int(row[1])
        if "Quarantäne" in row[0]: args["q"] = force_int(row[1])
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    if "q" in args: args["q"] = args["q"] + args["c"] - args["d"] - args["g"]
    update(sheets, 3462, **args, sig="Bot", ignore_delta=False)
    return True

schedule.append(Task(10, 40, 15, 35, 360, wittmund, 3462))
if __name__ == '__main__': wittmund(googlesheets())
