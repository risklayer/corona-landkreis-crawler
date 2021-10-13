#!/usr/bin/python3
from botbase import *

_heinsberg_c = re.compile(r"([0-9.]+) bestätigte")
_heinsberg_d = re.compile(r"Verstorbenen liegt im Kreis Heinsberg bei ([0-9.]+)\.")
_heinsberg_a = re.compile(r"([0-9.]+) Personen als noch nicht genesen")

def heinsberg(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.kreis-heinsberg.de/aktuelles/aktuelles/?pid=5294")
    main = soup.find(id="directory")
    ps = [p.get_text(" ").strip() for p in main.findAll("p")]
    ps = [p for p in ps if not p == ""]
    # for p in ps[:5]: print(p)
    if not today().strftime("%-d. %B %Y") in ps[0]: raise NotYetAvailableException("Heinsberg noch alt:" + ps[0])
    c = force_int(_heinsberg_c.search(ps[0]).group(1))
    d = force_int(_heinsberg_d.search(ps[0]).group(1)) + 37 # "mit"
    a = force_int(_heinsberg_a.search(ps[0]).group(1)) if _heinsberg_a.search(ps[0]) else None
    g = c - d - a if a else None
    update(sheets, 5370, c=c, d=d, g=g, sig="Bot")
    return True

schedule.append(Task(10, 15, 14, 35, 600, heinsberg, 5370))
if __name__ == '__main__': heinsberg(googlesheets())
