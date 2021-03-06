#!/usr/bin/python3
from botbase import *

_stade_a = re.compile(r"Aktuell Erkrankte: *([0-9.]+) *\(\+?(-? *[0-9.]+|unverändert)\)")
_stade_c = re.compile(r"Positiv Getestete insgesamt: *([0-9.]+) *\(\+?(-? *[0-9.]+|unverändert)\)")
_stade_g = re.compile(r"Genesene: *([0-9.]+) *\(\+?(-? *[0-9.]+|unverändert)\)")
_stade_d = re.compile(r"Verstorbene: *([0-9.]+) *(?:\(\+?(-? *[0-9.]+|unverändert)\))?")
_stade_q = re.compile(r"Quarantäne: *([0-9.]+)")
_stade_si = re.compile(r"([0-9.]+)\s*\((?:[0-9.+-]+|unverändert)\)\s*stationär,\s*davon\s*([0-9.]+)\s*\((?:[0-9.+/-]+|unverändert)\)\s*Patient")
_stade_st = re.compile(r"Stand (\d\d\.\d\d\.20\d\d) / (\d\d?:\d\d) *Uhr")

def stade(sheets):
    #soup = get_soup("https://www.landkreis-stade.de/corona")
    soup = get_soup("https://www.landkreis-stade.de/umwelt-gesundheit-verbraucherschutz/gesundheit/corona-virus/corona-aktuelle-lage/?vs=1")
    main = soup.find(id="nolis_content_site") #.find(class_="innen")
    text = main.get_text(" ").strip()
    #print(text)
    date = check_date(" ".join(_stade_st.search(text).groups()), "Stade", datetime.timedelta(hours=8))
    a, aa = map(force_int, _stade_a.search(text).groups())
    c, cc = map(force_int, _stade_c.search(text).groups())
    d, dd = map(force_int, _stade_d.search(text).groups())
    g, gg = map(force_int, _stade_g.search(text).groups())
    q = (force_int(_stade_q.search(text).group(1)) + a) if _stade_q.search(text) else None
    s, i = None, None
    try:
        s, i = map(force_int, _stade_si.search(text).groups())
    except: pass
    comment = "Bot" if s is not None else "Bot ohne SI"
    update(sheets, 3359, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, q=q, s=s, i=i, date=date, comment=comment, ignore_delta=True)
    return True

schedule.append(Task(9, 15, 14, 35, 360, stade, 3359))
if __name__ == '__main__': stade(googlesheets())
