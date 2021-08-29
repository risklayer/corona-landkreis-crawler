#!/usr/bin/python3
from botbase import *

def lueneburg(sheets):
    soup = get_soup("https://corona.landkreis-lueneburg.de/aktuelle-situation/")
    content = soup.find(id="main").find("article")
    rows = content.find(id="table_4").findAll("tr")
    rows = [[x.text.strip() for x in row.findAll(["td","th"])] for row in rows]
    #print(rows[0],rows[-2],rows[-1], sep="\n")
    if not today().strftime("%d.%m.") in rows[-1][1]: raise NotYetAvailableException("Lueneburg noch alt:" + rows[0][1])
    assert "Gesamt" in rows[0][5]
    c, cc = force_int(rows[-1][5]), force_int(rows[-2][5])
    assert "Todesf" in rows[0][7]
    d, dd = force_int(rows[-1][7]), force_int(rows[-2][7])
    assert "Genesene" in rows[0][6]
    g, gg = force_int(rows[-1][6]), force_int(rows[-2][6])
    cc, gg, dd = c - cc, g - gg, d - dd
    update(sheets, 3355, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, sig="Bot", ignore_delta=False)
    return True

schedule.append(Task(15, 2, 20, 35, 600, lueneburg, 3355))
if __name__ == '__main__': lueneburg(googlesheets())
