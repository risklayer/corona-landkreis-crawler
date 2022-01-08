#!/usr/bin/python3
## Tommy
from botbase import *

def frankfurt(sheets):

    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://frankfurt.de/service-und-rathaus/verwaltung/aemter-und-institutionen/gesundheitsamt/informationen-zum-neuartigen-coronavirus-sars-cov-2/aktuelle-lage")
    header = next(x for x in soup.find_all("h4") if "Aktuelle Infektionszahlen in Frankfurt" in x.get_text())
    rows = [[x.text.strip() for x in row.findAll("td")] for row in header.findNext("table").findAll("tr")]
    date_text = rows[0][0]
    if not today().strftime("%d. %B %Y") in date_text: raise NotYetAvailableException("Frankfurt noch alt: " + date_text[:-93])
    assert "Gesamtzahl der COVID-19-Fälle in Frankfurt" in rows[1][0]
    assert "Todesfälle" in rows[2][0]
    assert "Genesene" in rows[3][0]
    c = force_int(rows[1][1])
    d = force_int(rows[2][1])
    g = force_int(rows[3][1])
    update(sheets, 6412, c=c,  d=d, g=g, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(8, 5, 10, 5, 360, frankfurt, 6412))
if __name__ == '__main__': frankfurt(googlesheets())
