#!/usr/bin/python3
from botbase import *

def warendorf(sheets):
    soup = get_soup("https://www.kreis-warendorf.de/aktuelles/presseinformationen/aktuelle-informationen-zum-coronavirus")
    content = soup.find(id="corona-tabelle-7-tage")
    rows = content.find("table").findAll("tr")
    rows = [[x.text.strip() for x in row.findAll(["td","th"])] for row in rows]
    #print(rows)
    date = check_date(rows[1][0], "Warendorf")
    assert "Bestätigte" in rows[0][3]
    c, cc = force_int(rows[1][3]), force_int(rows[1][2],0)
    assert "Verstorben" in rows[0][5]
    d, dd = force_int(rows[1][5]), force_int(rows[2][5],0)
    assert "Gesundet" in rows[0][4]
    g, gg = force_int(rows[1][4]), force_int(rows[2][4],0)
    dd, gg = d - dd, g - gg
    update(sheets, 5570, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, sig="Bot", comment="Bot ohne SI", ignore_delta=False)
    return True

schedule.append(Task(9, 2, 12, 35, 600, warendorf, 5570))
if __name__ == '__main__': warendorf(googlesheets())
