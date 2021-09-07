#!/usr/bin/python3
from botbase import *

def flensburg(sheets):
    soup = get_soup("https://www.flensburg.de/Aktuelles/Corona-Portal/Aktuelle-Lagemeldungen/Aktuelles-Infektionsgeschehen/")
    content = soup.find(id="vorlesen")
    rows = content.find("table").findAll("tr")
    rows = [[x.text.strip() for x in row.findAll("td")] for row in rows]
    #print(rows)
    if not today().strftime("%d.%m.") in rows[0][1]: raise NotYetAvailableException("Flensburg noch alt: " + rows[0][1])
    assert "Gesamtzahl" in rows[1][0]
    c, cc = force_int(rows[1][1].replace("*","")), force_int(rows[1][2],0)
    assert "Verstorbene" in rows[3][0]
    d, dd = force_int(rows[3][1]), force_int(rows[3][2],0)
    assert "Genesene" in rows[4][0]
    g, gg = force_int(rows[4][1]), force_int(rows[4][2],0)
    assert "Quarantäne" in rows[5][0]
    q = force_int(rows[5][1].replace("*","")) + c - d - g
    update(sheets, 1001, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, q=q, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(15, 2, 20, 35, 600, flensburg, 1001))
if __name__ == '__main__': flensburg(googlesheets())
