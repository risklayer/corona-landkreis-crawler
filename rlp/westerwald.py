#!/usr/bin/python3
from botbase import *

def westerwald(sheets):
    soup = get_soup("https://www.westerwaldkreis.de/aktuelles-detailansicht/gesundheitsamt-informiert.html")
    content = next(x for x in soup.find("section").findAll(class_="ce_text") if "Tagesmeldung" in x.find("h3").get_text())
    #print(content.get_text(""))
    t = content.find("h3").get_text()
    t = t.split(" ")[1]
    date = check_date(t, "Westerwald")
    table = next(x for x in content.findAll("table") if "Infizierte" in x.get_text())
    rows = [[x.text.strip() for x in row.findAll(["td","th"])] for row in table.findAll("tr")]
    #print(rows)
    assert "Westerwaldkreis" in rows[-1][0]
    assert "GESAMT" in rows[0][1]
    assert "genesen" in rows[0][2]
    assert "verstorben" in rows[0][3]
    c, g, d = map(force_int, rows[-1][1:4])
    update(sheets, 7143, c=c, d=d, g=g, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(9, 32, 11, 35, 600, westerwald, 7143))
if __name__ == '__main__': westerwald(googlesheets())
