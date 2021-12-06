#!/usr/bin/python3
## Tommy

from botbase import *

_greiz_c = re.compile(r"([0-9]+) Infektionen registriert")
_greiz_d = re.compile(r"([0-9]+) Patienten verstorben")
_greiz_date = re.compile(r"\(Stand *(\d+\.\d+\.20\d\d)")


def greiz(sheets):

    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.landkreis-greiz.de/landkreis-greiz/aktuell/nachrichten-details/corona-startseite/fallzahlen")

    content = soup.text
    date = _greiz_date.search(content).group(1)
    check_date(date, "Greiz")

    c = force_int(_greiz_c.search(content).group(1))
    d = force_int(_greiz_d.search(content).group(1))

    update(sheets, 16076, c=c, d=d, sig="Bot")

    return True

schedule.append(Task(11, 54, 13, 54, 360, greiz, 16076))
if __name__ == '__main__': greiz(googlesheets())
