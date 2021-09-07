#!/usr/bin/python3
from botbase import *

def harburg(sheets):
    soup = get_soup("https://www.landkreis-harburg.de/portal/seiten/alle-informationen-rund-um-die-corona-pandemie-901002222-20100.html?rubrik=1000042&vs=1")
    content = soup.find(id="content")
    rows = content.find("table", border="1").findAll("tr")
    rows = [[x.text.strip() for x in row.findAll("td")] for row in rows[:3]]
    # for row in rows: print(row)
    if not today().strftime("%d.%m.") in rows[1][0]: raise NotYetAvailableException("Harburg noch alt:" + rows[1][0])
    assert "insgesamt" in rows[0][4]
    c, cc = force_int(rows[1][4]), force_int(rows[2][4],0)
    assert "verstorben" in rows[0][6]
    d, dd = force_int(rows[1][6]), force_int(rows[2][6],0)
    assert "genesen" in rows[0][5]
    g, gg = force_int(rows[1][5]), force_int(rows[2][5],0)
    cc, dd, gg = c - cc, d - dd, g - gg
    update(sheets, 3353, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, sig="Bot", ignore_delta=False)
    return True

schedule.append(Task(16, 2, 20, 35, 600, harburg, 3353))
if __name__ == '__main__': harburg(googlesheets())
