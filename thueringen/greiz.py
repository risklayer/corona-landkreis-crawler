#!/usr/bin/python3
## Tommy
from botbase import *

_greiz_c = re.compile(r"([0-9]+) Infektionen registriert")
_greiz_d = re.compile(r"([0-9]+) Personen verstorben")
_greiz_a = re.compile(r"gesamt\s+\(innerhalb von 21 Tagen\)\s+([0-9]+)")
_greiz_date = re.compile(r"\(Stand *(\d+\.\d+\.20\d\d)")

def greiz(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.landkreis-greiz.de/landkreis-greiz/aktuell/nachrichten-details/corona-startseite/fallzahlen")

    content = soup.get_text()
    #print(content)
    date = _greiz_date.search(content).group(1)
    check_date(date, "Greiz")

    c = force_int(_greiz_c.search(content).group(1))
    d = force_int(_greiz_d.search(content).group(1))
    a = force_int(_greiz_a.search(content).group(1))
    g = c - d - a

    update(sheets, 16076, c=c, d=d, g=g, sig="Bot")
    return True

schedule.append(Task(8, 54, 13, 54, 360, greiz, 16076))
if __name__ == '__main__': greiz(googlesheets())
