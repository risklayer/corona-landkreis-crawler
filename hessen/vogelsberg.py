#!/usr/bin/python3
from botbase import *

_vogelsberg_cc = re.compile(r"([0-9.]+) (?:neue Fälle|Neuinfektionen)")
_vogelsberg_gg = re.compile(r"([0-9.]+) Menschen (?:\w+ )*als genesen", re.U)
_vogelsberg_c = re.compile(r"Fälle gesamt: ([0-9.]+)")
_vogelsberg_g = re.compile(r"Genesene: ([0-9.]+)")
_vogelsberg_d = re.compile(r"Verstorbene: ([0-9.]+)")

def vogelsberg(sheets):
    soup = get_soup("https://www.vogelsbergkreis.de/kreisverwaltung/presse-und-oeffentlichkeitsarbeit/")
    li = next(x for x in soup.find("main").findAll("article") if "Corona-Update" in x.get_text())
    check_date(li.find("time").get_text(), "Vogelsbergkreis")
    link = li.find(href=True)["href"] if li else None
    from urllib.parse import urljoin
    link = urljoin("https://www.vogelsbergkreis.de/kreisverwaltung/presse-und-oeffentlichkeitsarbeit/", link)
    print("Getting", link)
    soup = get_soup(link)
    text = soup.find("main").find(class_="id-content").get_text(" ").strip()
    # print(text)
    cc = force_int(_vogelsberg_cc.search(text).group(1))
    c = force_int(_vogelsberg_c.search(text).group(1))
    gg = force_int(_vogelsberg_gg.search(text).group(1))
    g = force_int(_vogelsberg_g.search(text).group(1))
    d = force_int(_vogelsberg_d.search(text).group(1))
    update(sheets, 6535, c=c, cc=cc, d=d, g=g, gg=gg, ignore_delta=True)
    return True

schedule.append(Task(13, 30, 15, 35, 360, vogelsberg, 6535))
if __name__ == '__main__': vogelsberg(googlesheets())
