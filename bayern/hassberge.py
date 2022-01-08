#!/usr/bin/python3
## Tommy
from botbase import *

_hassberge_date = re.compile(r"(\d\d?\.\d\d?\.20\d\d)")

def hassberge(sheets):

    soup = get_soup("https://www.hassberge.de/topmenu/startseite/corona-virus.html")
    header = next(x for x in soup.find_all("h4") if "Aktuelle Fallzahlen im Landkreis Haßberge" in x.get_text())
    date_text = _hassberge_date.search(header.findNext("h2").get_text()).group(1)
    check_date(date_text, "Hassberge")
    rows = [[x.text.strip() for x in row.findAll("td")] for row in header.findNext("table").findAll("tr")]
    assert "Gesamtzahl der positiv getesteten Personen" in rows[1][0]
    assert "davon geheilte Fälle" in rows[2][0]
    assert "aktuell infizierte Personen" in rows[3][0]
    assert "Verstorbene Personen" in rows[4][0]
    assert "Isolierte Kontakt-Personen" in rows[5][0]
    c = force_int(rows[1][1])
    g = force_int(rows[2][1])
    q = force_int(rows[3][1]) + force_int(rows[5][1])
    d = force_int(rows[4][1])
    update(sheets, 9674, c=c,  d=d, g=g, q=q, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(12, 42, 14, 42, 360, hassberge, 9674))
if __name__ == '__main__': hassberge(googlesheets())
