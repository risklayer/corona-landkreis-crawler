#!/usr/bin/python3
from botbase import *

_stade_a = re.compile(r"Aktuell Erkrankte: *([0-9.]+) *\(\+?(-? *[0-9.]+|unverändert)\)")
_stade_c = re.compile(r"Positiv Getestete insgesamt: *([0-9.]+) *\(\+?(-? *[0-9.]+|unverändert)\)")
_stade_g = re.compile(r"Genesene: *([0-9.]+) *\(\+?(-? *[0-9.]+|unverändert)\)")
_stade_d = re.compile(r"Verstorbene: *([0-9.]+) *(?:\(\+?(-? *[0-9.]+|unverändert)\))?")
_stade_q = re.compile(r"Quarantäne: *([0-9.]+)")
_stade_si = re.compile(r"([0-9.]+) *\((?:[0-9.+-]+|unverändert)\) stationär, davon ([0-9.]+) *\((?:[0-9.+-]+|unverändert)\) *Patient")
_stade_st = re.compile(r"Stand (\d\d\.\d\d\.20\d\d) / (\d\d?:\d\d) *Uhr")

def stade(sheets):
    soup = get_soup("https://www.landkreis-stade.de/corona")
    main = soup.find(id="nolis_content_site").find(class_="innen")
    text = main.get_text(" ").strip()
    #print(text)
    date = check_date(" ".join(_stade_st.search(text).groups()), "Stade", datetime.timedelta(hours=8))
    a, aa = map(force_int, _stade_a.search(text).groups())
    c, cc = map(force_int, _stade_c.search(text).groups())
    d, dd = map(force_int, _stade_d.search(text).groups())
    g, gg = map(force_int, _stade_g.search(text).groups())
    q = force_int(_stade_q.search(text).group(1)) + a
    s, i = map(force_int, _stade_si.search(text).groups())
    update(sheets, 3359, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, q=q, s=s, i=i, date=date, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(9, 15, 14, 35, 360, stade, 3359))
if __name__ == '__main__': stade(googlesheets())
