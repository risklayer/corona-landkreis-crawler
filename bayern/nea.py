#!/usr/bin/python3
from botbase import *

_nea_st = re.compile(r"Landkreis, (\d\d\.\d\d.20\d\d)")

def nea(sheets):
    soup = get_soup("https://www.kreis-nea.de/service-themen/gesundheit-soziales/aktuelle-situation-coronavirus-sars-cov-2.html")
    main = soup.find(id="content").find(class_="inner")
    rows = [[x.get_text() for x in row.findAll(["td","th"])] for row in main.findAll("tr")]
    #print(*rows, sep="\n")
    date = _nea_st.search(main.find("h3").get_text()).group(1)
    date = check_date(date, "Neustadt a.d. Aisch")
    assert "Gesamtfallzahl" in rows[0][0]
    c = force_int(rows[0][1])
    assert "Isolation" in rows[1][0]
    a = force_int(rows[1][1])
    assert "verstorben" in rows[2][0]
    d = force_int(rows[2][1])
    g = c - a - d
    update(sheets, 9575, c=c, d=d, g=g, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(14, 0, 19, 35, 360, nea, 9575))
if __name__ == '__main__': nea(googlesheets())
