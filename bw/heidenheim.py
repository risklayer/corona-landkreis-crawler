#!/usr/bin/python3
from botbase import *

_heidenheim_st = re.compile(r"Stand: *(\d\d?\.\d\d?\.20\d\d)")
_twoval = re.compile(r"([0-9.]+)(?:\s+\(\+?\s*(-?[0-9.]+)\s*\))?")

def heidenheim(sheets):
    data = get_soup("https://www.info-corona-lrahdh.de/startseite")
    body = data.find(role="main").find("article")
    #print(body.find("h2", text=_heidenheim_st).get_text())
    date = _heidenheim_st.search(body.find("h2", text=_heidenheim_st).get_text()).group(1)
    date = check_date(date, "Heidenheim")
    rows = [[x.get_text() for x in y.findAll(["td","th"])] for y in body.findAll("tr")]
    #print(*rows, sep="\n")
    assert "bestätigte" in rows[0][0]
    c, cc = map(force_int, _twoval.search(rows[1][0]).groups())
    assert "Todesfälle" in rows[0][1]
    d, dd = map(force_int, _twoval.search(rows[1][1]).groups())
    update(sheets, 8135, c=c, cc=cc, d=d, dd=dd, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(16, 0, 19, 50, 360, heidenheim, 8135))
if __name__ == '__main__': heidenheim(googlesheets())
