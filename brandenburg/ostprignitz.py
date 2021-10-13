#!/usr/bin/python3
from botbase import *

_ostprignitz_c = re.compile(r"([0-9.]+) (?:\(\+?\s*(-?[0-9.]+)\) *)?Fälle bisher")
_ostprignitz_d = re.compile(r"([0-9.]+) (?:\(\+?\s*(-?[0-9.]+)\) *)?Verstorbene")
_ostprignitz_g = re.compile(r"([0-9.]+) (?:\(\+?\s*(-?[0-9.]+)\) *)?genesen")
_ostprignitz_s = re.compile(r"([0-9.]+) Personen in station")
_ostprignitz_q1 = re.compile(r"([0-9.]+) (?:\([-+0-9 ]*\))?\s*Kontaktpersonen")
_ostprignitz_q2 = re.compile(r"([0-9.]+) (?:\([-+0-9 ]*\))?\s*Reiserück")

def ostprignitz(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.ostprignitz-ruppin.de/index.phtml?mNavID=353.254&sNavID=353.254&La=1")
    rows = [[x.get_text() for x in row.findAll(["th","td"])] for row in soup.find("table").findAll("tr")]
    #print(*rows, sep="\n")
    #print(today().strftime("%-d. %B %Y"))
    if not today().strftime("%-d. %B %Y") in rows[1][0]: raise NotYetAvailableException("Ostprignitz noch alt");
    c, cc, a, g, gg, d = map(force_int, rows[1][1:7])
    c, g = c + 3, g + 3
    update(sheets, 12068, c=c, cc=cc, d=d, g=g, gg=gg, sig="Bot")
    return True

schedule.append(Task(12, 00, 17, 35, 360, ostprignitz, 12068))
if __name__ == '__main__': ostprignitz(googlesheets())
