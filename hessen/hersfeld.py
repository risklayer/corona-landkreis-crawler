#!/usr/bin/python3
from botbase import *

_hersfeld_c = re.compile(r"Infektionen\sinsgesamt:\s([0-9.]+)\s(?:\(\+?(-?\s*[0-9.]+)\szum\s)?")
_hersfeld_d = re.compile(r"Todesfälle:\s([0-9.]+)\s(?:\(\+?(-?\s*[0-9.]+)\szum\s)?")
_hersfeld_g = re.compile(r"Genesungen:\s([0-9.]+)\s(?:\(\+?(-?\s*[0-9.]+)\szum\s)?")
_hersfeld_s = re.compile(r"([0-9.]+)\sinfizierte(?:\sPersone?n?)?\sin\sBehandlung,\sdavon\s([0-9.]+)(?:\sPersone?n?)?\sauf\s[Ii]ntensiv")
_hersfeld_q = re.compile(r"Quarantäne:\s([0-9.]+)")

def hersfeld(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.hef-rof.de/")
    main = soup.find(id="fav-slide")
    ps = [p.text for p in main.findAll("p")]
    #for p in ps: print(p)
    if not any([today().strftime("Stand: %d.%m.%Y") in p for p in ps]): raise NotYetAvailableException("Hersfeld noch alt: " + next(p for p in ps if "Stand:" in p))
    c, cc, d, dd, g, gg, s, i, q = None, None, None, None, None, None, None, None, None
    for p in ps:
        m = _hersfeld_c.search(p)
        if m: c, cc = force_int(m.group(1)), force_int(m.group(2))
        #if m: c = force_int(m.group(1))
        m = _hersfeld_d.search(p)
        if m: d, dd = force_int(m.group(1)), force_int(m.group(2))
        m = _hersfeld_g.search(p)
        #if m: g = force_int(m.group(1))
        if m: g, gg = force_int(m.group(1)), force_int(m.group(2))
        m = _hersfeld_s.search(p)
        if m: s, i = force_int(m.group(1)), force_int(m.group(2))
        m = _hersfeld_q.search(p)
        if m: q = force_int(m.group(1))
    update(sheets, 6632, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, q=q, s=s, i=i, ignore_delta="mon")
    return True

schedule.append(Task(13, 0, 16, 35, 360, hersfeld, 6632))
if __name__ == '__main__': hersfeld(googlesheets())
