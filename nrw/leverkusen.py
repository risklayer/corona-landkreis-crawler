#!/usr/bin/python3
from botbase import *

def leverkusen(sheets):
    soup = get_soup("https://www.leverkusen.de/leben-in-lev/corona-info-leverkusen/index.php")
    content = soup.find(id="SP-content-inner")
    rows = content.find("table").findAll("tr")
    rows = [[x.text.strip() for x in row.findAll("td")] for row in rows]
    #print(rows)
    if not today().strftime("%-d. %b") in rows[1][0]: raise NotYetAvailableException("Leverkusen noch alt: " + rows[0][1])
    assert "Bestätigte" in rows[0][1]
    c, cc = force_int(rows[1][1]), force_int(rows[2][1],0)
    assert "Todesfälle" in rows[0][2]
    d, dd = force_int(rows[1][2]), force_int(rows[2][2],0)
    assert "Genesene" in rows[0][3]
    g, gg = force_int(rows[1][3]), force_int(rows[2][3],0)
    cc, dd, gg = c - cc, d - dd, g - gg
    update(sheets, 5316, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, sig="Bot", ignore_delta=False)
    return True

schedule.append(Task(9, 2, 12, 35, 600, leverkusen, 5316))
if __name__ == '__main__': leverkusen(googlesheets())
