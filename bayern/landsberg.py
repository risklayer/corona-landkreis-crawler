#!/usr/bin/python3
from botbase import *

_landsberg_c = re.compile(r"Insgesamt infizierte[^:]+Personen:\s*([0-9.]+)", re.U)
_landsberg_g = re.compile(r"Genesen:\s*ca\.\s*([0-9.]+)", re.U)
_landsberg_d = re.compile(r"Todesfälle[^:]+:\s*([0-9.]+)", re.U)
_landsberg_q = re.compile(r"Kontaktpersonen[^:]+in Quarantäne:\s*([0-9.]+)", re.U)

def landsberg(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.landkreis-landsberg.de/aktuelles/fragen-antworten-zu-corona/")
    main = soup.find("main").find(class_="ce-bodytext")
    text = main.get_text(" ")
    #print(text)
    if not today().strftime("%-d. %B %Y") in text: raise NotYetAvailableException("Landsberg noch alt")
    c = force_int(_landsberg_c.search(text).group(1))
    d = force_int(_landsberg_d.search(text).group(1))
    g = force_int(_landsberg_g.search(text).group(1))
    q = force_int(_landsberg_q.search(text).group(1))
    q = q + c - d - g
    update(sheets, 9181, c=c, d=d, g=g, q=q, sig="Bot")
    return True

schedule.append(Task(10, 3, 12, 35, 360, landsberg, 9181))
if __name__ == '__main__': landsberg(googlesheets())
