#!/usr/bin/python3
from botbase import *

_stand = re.compile(r"Stand: (\d\d.\d\d.20\d\d)")
_match_two = re.compile(r"([0-9.]+)(?:\s+\(([+-]?[0-9.]*),?\))?", re.U)

def wilhelmshaven(sheets):
    soup = get_soup("https://www.wilhelmshaven.de/")
    content = soup.find(id="innerBody")
    rows = [[x.get_text() for x in y.findAll(["td","th"])] for y in content.findAll("tr")]
    #print(*rows, sep="\n")
    args = dict()
    for row in rows:
        if "Gesamtzahl der Corona" in row[0]: args["c"], args["cc"] = map(force_int, _match_two.match(row[1]).groups())
        if "davon verstorben" in row[0]: args["d"], args["dd"] = map(force_int, _match_two.match(row[1]).groups())
        if "Genesungen" in row[0]: args["g"], args["gg"] = map(force_int, _match_two.match(row[1]).groups())
        if "stationär" in row[0]: args["s"], _ = map(force_int, _match_two.match(row[1]).groups())
        if "angeordnete Q" in row[0]: args["q"], _ = map(force_int, _match_two.match(row[1]).groups())
    date = content.find(text=_stand)
    date = check_date(_stand.search(date).group(1),"Wilhelmshaven")
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    update(sheets, 3405, **args, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(13, 9, 15, 35, 360, wilhelmshaven, 3405))
if __name__ == '__main__': wilhelmshaven(googlesheets())
