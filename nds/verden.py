#!/usr/bin/python3
from botbase import *

_stand = re.compile(r"Stand")
_verden_c = re.compile(r"([.0-9]+)\s+\(\+?\s*(-?[.0-9]+)\s+zu\w?\s+(?:\w+|\d+\.\d+\.)\)\s+laborbestätigte\s+Coronavirus-Fälle")
_verden_g = re.compile(r"([.0-9]+)\s+\(\+?\s*(-?[.0-9]+)\s+zu\w?\s+(?:\w+|\d+\.\d+\.)\)\s+Covid-19-Patienten[a-z ]+wieder\s+genesen")
_verden_d = re.compile(r"([.0-9]+)\s+Personen\s+sind\s+verstorben")
_verden_q = re.compile(r"([.0-9]+)\s+Kontaktpersonen")
_verden_s1 = re.compile(r"([.0-9]+)\s+Person[A-Za-z ]+?stationär\s+in")
_verden_s2 = re.compile(r"([.0-9]+)\s+weitere\s+Person[A-Za-z ]+?längerfristig")

def verden(sheets):
    soup = get_soup("https://www.landkreis-verden.de/portal/seiten/aktuelles-zum-coronavirus-geschehen-im-landkreis-verden-901001573-20600.html?rubrik=901000034&vs=1")
    content = soup.find(id="info")
    text = content.get_text(" ")
    #print(text)
    date = content.find(text=_stand)
    if not today().strftime("%d.%m.%Y") in date: raise NotYetAvailableException("Verden noch alt: " + date)
    c, cc = map(force_int, _verden_c.search(text).groups())
    g, gg = map(force_int, _verden_g.search(text).groups())
    d = force_int(_verden_d.search(text).group(1))
    q = force_int(_verden_q.search(text).group(1)) + c - g - d
    s1, s2 = _verden_s1.search(text), _verden_s2.search(text)
    s = (force_int(s1.group(1),0) if s1 else 0) + (force_int(s2.group(1),0) if s2 else 0) if s1 is not None or s2 is not None else 0
    update(sheets, 3361, c=c, cc=cc, g=g, gg=gg, d=d, q=q, s=s, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(9, 30, 12, 35, 360, verden, 3361))
if __name__ == '__main__': verden(googlesheets())
