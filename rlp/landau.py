#!/usr/bin/python3
from botbase import *

_gesamt_c = re.compile(r"Insgesamt wurden *([0-9.]+) *Fälle")
_gesamt_g = re.compile(r"([0-9.]+) *Personen sind gesundet")
_gesamt_d = re.compile(r"Insgesamt sind *([0-9.]+) *Personen verstorben")
_landau = re.compile(r"Stadt Landau *: *([0-9.]+) Personen *\( *([0-9.]+) *davon gesundet, *([0-9.]+) *verstorben")

def landau(sheets):
    from urllib.parse import urljoin
    soup = get_soup("https://www.landau.de/Verwaltung-Politik/Pressemitteilungen/")
    m = next(x for x in soup.find("section").findAll(class_="mitteilungen") if "Fallzahlen im" in x.get_text())
    date = check_date(m.find(class_="date").get_text(), "Landau")
    url = urljoin("https://www.landau.de/", m.find(class_="liste_titel").find("a")["href"])
    print("Getting", url)
    soup = get_soup(url)
    text = soup.find(class_="mitteilungen_detail").get_text(" ").strip()
    #print(text)
    if not today().strftime("%d.%m.%Y") in text: raise NotYetAvailableException("Landau noch alt:" + ps[0])
    c, g, d = map(force_int, _landau.search(text).groups())
    update(sheets, 7313, c=c, d=d, g=g, sig="Bot") # Landau
    c2 = force_int(_gesamt_c.search(text).group(1)) - c
    d2 = force_int(_gesamt_d.search(text).group(1)) - d
    g2 = force_int(_gesamt_g.search(text).group(1)) - g
    update(sheets, 7337, c=c2, d=d2, g=g2, sig="Bot") # Südl. Weinstraße
    return True

schedule.append(Task(13, 30, 15, 35, 600, landau, 7337))
if __name__ == '__main__': landau(googlesheets())
