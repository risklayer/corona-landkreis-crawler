#!/usr/bin/python3
## Tommy
from botbase import *

def starnberg(sheets):
    #### BROKEN
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    #soup = get_soup("https://www.lk-starnberg.de/B%C3%BCrgerservice/Gesundheit-und-Krankheit/Coronavirus-Informationen-Fragen-und-Antworten/Infektionszahlen-und-weitere-Daten-zum-Coronavirus")
    soup = get_soup("https://www.lk-starnberg.de/B%C3%BCrgerservice/Gesundheit-und-Krankheit/Coronavirus-Informationen-Fragen-und-Antworten/#c30")
    tables = soup.find_all("table")

    header = tables[0].findAll("tr")[0].find_all("th")
    row = tables[0].find_all("tr")[1].find_all("td")
    assert "Datum" in header[0].text
    check_date(row[0].text, "Starnberg")
    assert "positiv getestete Fälle" in header[1].text
    c = force_int(row[1].text)
    assert "Veränderung zum Vortag" in header[2].text
    cc_text = row[2].text if not ("(Sa:") in row[2].text else row[2].text[:row[2].text.find("(Sa:")] ## "+x (Sa: +y ; So: +z)" on mondays
    cc = force_int(cc_text)

    rows = [[x.text.strip() for x in row.find_all("td")] for row in tables[2].find_all("tr")]
    assert "An Corona (COVID-19) verstorbene Personen" in rows[2][0]
    ad = force_int(rows[2][1])
    assert "Mit Corona (COVID-19) verstorbene Personen" in rows[3][0]
    md = force_int(rows[3][1])
    d = ad + md

    update(sheets, 9188, c=c, cc=cc, d=d, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(16, 1, 18, 15, 360, starnberg, 9188))
if __name__ == '__main__': starnberg(googlesheets())
