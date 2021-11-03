#!/usr/bin/python3
from botbase import *

_hamm_a = re.compile(r"Akut infizierte Personen: *([0-9.]+)")
_hamm_g = re.compile(r"Genesene Personen: *([0-9.]+)")
_hamm_q = re.compile(r"Quarantäne: *([0-9.]+)")
_hamm_s = re.compile(r"stationärer Behandlung: *([0-9.]+)")
_hamm_i = re.compile(r"Intensivstation: *([0-9.]+)")
_hamm_d = re.compile(r"verstorbene Personen: *([0-9.]+)")
_hamm_cc1 = re.compile(r"(?:Neuinfektionen|zusätzlich rückwirkend): *([0-9.]+)")
_hamm_cc2 = re.compile(r"zusätzlich *([0-9.]+) Nachmeldungen")

def hamm(sheets):
    soup = get_soup("https://www.hamm.de/corona")
    main = soup.find(id="c78919")
    date = check_date(main.find("em").text.replace("Stand:",""), "Hamm")
    #if not today().strftime("%d.%m.%Y") in main.text: raise NotYetAvailableException("Hamm noch alt:" + main.text)
    text = main.get_text(separator=" ")
    #print(text)
    a = force_int(_hamm_a.search(text).group(1))
    g = force_int(_hamm_g.search(text).group(1))
    q = force_int(_hamm_q.search(text).group(1))
    s = force_int(_hamm_s.search(text).group(1))
    i = force_int(_hamm_i.search(text).group(1))
    d = force_int(_hamm_d.search(text).group(1))
    cc = 0
    for m in _hamm_cc1.findall(text): cc += int(m)
    for m in _hamm_cc2.findall(text): cc += int(m)
    c = a + g + d
    update(sheets, 5915, c=c, cc=cc, d=d, g=g, q=q, s=s, i=i, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(12, 14, 19, 35, 360, hamm, 5915))
if __name__ == '__main__': hamm(googlesheets())
