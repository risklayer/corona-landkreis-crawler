#!/usr/bin/python3
from botbase import *

_solingen_c = re.compile(r"([0-9.]+) +bestätigte")
_solingen_d = re.compile(r"([0-9.]+) +mit dem Virus infizierte Menschen sind bisher verstorben")
_solingen_g = re.compile(r"([0-9.]+) +Menschen sind wieder genesen")
_solingen_g2 = re.compile(r"Wieder genesen sind +ca. +([0-9.]+)")
_solingen_s = re.compile(r"([0-9.]+) +Patient")
_solingen_q = re.compile(r"In Quarantäne befinden sich derzeit insgesamt +([0-9.]+) +Personen")

def solingen(sheets):
    soup = get_soup("https://www.solingen.de/de/inhalt/coronavirus-statistik/")
    main = soup.find("main").find("article")
    content = main.get_text(" ").strip()
    #print(content)
    if not today().strftime("%d.%m.") in content: raise NotYetAvailableException("Solingen noch alt:" + ps[0])
    c = force_int(_solingen_c.search(content).group(1))
    d = force_int(_solingen_d.search(content).group(1))
    g = force_int((_solingen_g.search(content) or _solingen_g2.search(content)).group(1))
    s = force_int(_solingen_s.search(content).group(1))
    q = force_int(_solingen_q.search(content).group(1)) if _solingen_q.search(content) else None
    update(sheets, 5122, c=c, d=d, g=g, s=s, q=q, sig="Bot")
    return True

schedule.append(Task(9, 30, 20, 35, 600, solingen, 5122))
if __name__ == '__main__': solingen(googlesheets())
