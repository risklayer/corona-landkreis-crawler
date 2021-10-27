#!/usr/bin/python3
from botbase import *

def biberach(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    data = get_soup("https://www.biberach.de/landratsamt/kreisgesundheitsamt.html")
    body = data.find(id="contentMiddle")
    #print(body.get_text(), today().strftime("%-d. %B %Y"))
    if not today().strftime("%-d. %B %Y") in body.get_text(): raise NotYetAvailableException("Biberach: "+body.find("strong").get_text())
    rows = [[x.get_text() for x in y.findAll(["td","th"])] for y in body.find(class_="csc-frame").findAll("tr")]
    #print(*rows, sep="\n")
    assert "Infizierte gesamt" in rows[0][0]
    c = force_int(rows[0][1])
    assert "Differenz" in rows[1][0]
    cc = force_int(rows[1][1])
    assert "Genesene gesamt" in rows[2][0]
    g = force_int(rows[2][1])
    assert "Verstorbene gesamt" in rows[3][0]
    d = force_int(rows[3][1])
    update(sheets, 8426, c=c, cc=cc, g=g, d=d, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(15, 00, 16, 30, 300, biberach, 8426))
if __name__ == '__main__': biberach(googlesheets())
