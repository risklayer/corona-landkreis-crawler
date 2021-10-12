#!/usr/bin/python3
from botbase import *

def unstrut(sheets):
    soup = get_soup("https://www.unstrut-hainich-kreis.de/index.php/informationen-zum-neuartigen-coronavirus")
    article = soup.find("article")
    text = article.find("h4").get_text().strip()
    #print(text)
    if not today().strftime("Stand: %d.%m.%Y") in text: raise NotYetAvailableException("Unstrut noch alt");
    rows = [[x.get_text() for x in tr.findAll(["td","th"])] for tr in article.findAll("tr")]
    assert "Aktuell infiziert" in rows[3][0]
    a = force_int(rows[3][1])
    assert "station" in rows[4][0]
    s = force_int(rows[4][1])
    assert "schwer" in rows[5][0]
    i = force_int(rows[5][1])
    assert "Quarant" in rows[8][0]
    q = force_int(rows[8][1]) + s
    assert "Infizierte ab" in rows[9][0]
    c = force_int(rows[9][1])
    assert "Neuinfekt" in rows[10][0]
    cc = force_int(rows[10][1])
    assert "Genesene ab" in rows[11][0]
    g = force_int(rows[11][1])
    assert "Genesene Per" in rows[12][0]
    gg = force_int(rows[12][1])
    assert "Verstorbene" in rows[13][0]
    d = force_int(rows[13][1])
    update(sheets, 16064, c=c, cc=cc, d=d, g=g, gg=gg, q=q, s=s, i=i, sig="Bot")
    return True

schedule.append(Task(8, 30, 12, 35, 360, unstrut, 16064))
if __name__ == '__main__': unstrut(googlesheets())
