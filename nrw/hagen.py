#!/usr/bin/python3
from botbase import *

def hagen(sheets):
    soup = get_soup("https://www.hagen.de/web/de/hagen_de/01/0111/011101/aktuelle_infos_aus_hagen.html")
    content = soup.find(id="content")
    table = next(t for t in content.findAll("table") if t.find("h3") is not None and "Gesamtzahl" in t.find("h3").get_text())
    rows = [[x.get_text(" ").strip() for x in row.findAll(["td","th"])] for row in table.findAll("tr")]
    #for row in rows: print(row)
    if not today().strftime("%d.%m.%Y") in rows[-1][0]: raise NotYetAvailableException("Hagen: "+rows[-1][0])
    assert "Gesamt" in rows[0][0]
    c = force_int(rows[1][0])
    assert "Genesene" in rows[3][1]
    g = force_int(rows[4][1])
    assert "Neu-Infizierte" in rows[6][0]
    cc = force_int(rows[7][0])
    assert "Neu-Genesene" in rows[6][1]
    gg = force_int(rows[7][1])
    assert "Verstorbene" in rows[3][2]
    d = sum([force_int(x) for x in re.findall(r"[0-9.]+", rows[4][2])])
    update(sheets, 5914, c=c, cc=cc, d=d, g=g, gg=gg, sig="Bot", comment="Bot ohne Q", ignore_delta=False)
    return True

schedule.append(Task(9, 2, 11, 35, 600, hagen, 5914))
if __name__ == '__main__': hagen(googlesheets())
