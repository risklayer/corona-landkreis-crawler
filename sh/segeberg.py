#!/usr/bin/python3
from botbase import *

_segeberg_c = re.compile(r"Gesamtzahl aller bisher nachgewiesenen Infizierten im Kreis beträgt jetzt ([0-9.]+)")
_segeberg_cc = re.compile(r"([0-9.]+) per PCR-Test nachgewiesene Corona-Neuinfektionen")
_segeberg_g = re.compile(r"genesen gelten ([0-9.]+)")
_segeberg_d = re.compile(r"Verstorbenen? an oder mit COVID-[^.]* ([0-9.]+)")
_segeberg_q = re.compile(r"Quarantäne befinden sich derzeit ([0-9.]+)")
_segeberg_s = re.compile(r"([0-9.]+|\w+) Personen werden in einer Klinik")
_segeberg_i = re.compile(r"([0-9.]+|\w+) davon intensivmedizinisch")
_segeberg_st = re.compile(r"Stand (\d+\.\d+\.?\d*)")

def segeberg(sheets):
    import bs4
    soup = get_soup("https://www.segeberg.de/F%C3%BCr-Segeberger/Coronavirus/Aktuelle-Informationen-und-Mitteilungen/")
    main = soup.find(class_="inhalt")
    #print(next(x for x in main.findAll(class_="aufklappcontent_container")))
    main = next(x for x in main.findAll(class_="aufklappcontent_container") if "Gesamtzahl" in x.get_text())
    text = main.get_text(" ").strip()
    #print(text)
    date = check_date(_segeberg_st.search(text).group(1), "Segeberg")
    c = force_int(_segeberg_c.search(text).group(1))
    cc = force_int(_segeberg_cc.search(text).group(1))
    g = force_int(_segeberg_g.search(text).group(1))
    d = force_int(_segeberg_d.search(text).group(1))
    q = force_int(_segeberg_q.search(text).group(1)) + c - g - d
    s = force_int(_segeberg_s.search(text).group(1))
    i = force_int(_segeberg_i.search(text).group(1))
    update(sheets, 1060, c=c, cc=cc, d=d, g=g, q=q, s=s, i=i, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(16, 1, 19, 35, 360, segeberg, 1060))
if __name__ == '__main__': segeberg(googlesheets())
