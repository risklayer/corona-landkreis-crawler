#!/usr/bin/python3
from botbase import *

_muenster_c = re.compile(r"bestätigte Corona-Fälle: ([0-9.]+) +\(\+? *([-0-9.]+)\)")
_muenster_g = re.compile(r"([0-9.]+) +\(\+? *([-0-9.]+)\) [A-Za-z ]*?wieder genesen")
_muenster_d = re.compile(r"([0-9.]+) +[A-Za-z ]*?storben")

def muenster(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.muenster.de/corona_entwicklung.html")
    main = soup.find("main")
    p = main.find("li").get_text(" ")
    #print(p)
    #date = check_date(p.split(":")[0], "Münster")
    if not today().strftime("%-d. %B") in p: raise NotYetAvailableException("Münster noch alt:" + p)
    c, cc = map(force_int, _muenster_c.search(p).groups())
    g, gg = map(force_int, _muenster_g.search(p).groups())
    d = force_int(_muenster_d.search(p).group(1))
    update(sheets, 5515, c=c, cc=cc, d=d, g=g, gg=gg, sig="Bot", ignore_delta=today().weekday()==0) # kein Delta am Montag
    return True

schedule.append(Task(12, 0, 13, 45, 300, muenster, 5515))
if __name__ == '__main__': muenster(googlesheets())
