#!/usr/bin/python3
from botbase import *

_kulmbach_two = re.compile(r"([0-9.]+)\s*\(\+?(-?\s*[0-9.]+)\)")

def kulmbach(sheets):
    soup = get_soup("https://www.landkreis-kulmbach.de/landkreis-kulmbach/coronavirus/")
    table = soup.find("main").find("table")
    rows = [[x.get_text() for x in row.findAll(["td","th"])] for row in table.findAll("tr")]
    #print(*rows, sep="\n")
    date = rows[0][1].split(":",1)[1]
    date = check_date(date, "Kulmbach")
    assert "aktuelle" in rows[2][0]
    a = force_int(rows[2][1])
    assert "stationär" in rows[5][0]
    s, _, i = map(force_int, re.findall(r"([0-9.]+)", rows[5][1]))
    assert "Quarantäne" in rows[6][0]
    q = force_int(rows[6][1]) + a
    assert "insgesamt" in rows[7][0]
    c, cc = map(force_int, _kulmbach_two.search(rows[7][1]).groups())
    assert "Genesene" in rows[8][0]
    g, gg = map(force_int, _kulmbach_two.search(rows[8][1]).groups())
    assert "Verstorbene" in rows[9][0]
    try:
        d, dd = map(force_int, _kulmbach_two.search(rows[9][1]).groups())
    except:
        d, dd = force_int(rows[9][1]), None
    update(sheets, 9477, c=c, cc=cc, d=d, g=g, gg=gg, s=s, i=i, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(15, 30, 18, 35, 600, kulmbach, 9477))
if __name__ == '__main__': kulmbach(googlesheets())
