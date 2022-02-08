#!/usr/bin/python3
from botbase import *

_rbk2_c = re.compile(r"Insgesamt gibt es nun ([0-9.]+) bestätigte")
_rbk2_cc = re.compile(r"([0-9.]+) weitere bestätigte")
_rbk2_d = re.compile(r"Insgesamt stehen ([0-9.]+) Todesfälle")
_rbk2_g = re.compile(r"gelten ([0-9.]+) Personen inzwischen als genesen")
_rbk2_si = re.compile(r"([0-9.]+) Personen, die an Covid-19 erkrankt \w+, befinden sich aktuell in einem Krankenhaus [\w\s]+, davon \(?([0-9.]+|\w+)\) in intensiv", re.U)
_rbk2_q = re.compile(r"([0-9.]+) Personen befinden sich in Quarantäne")
_rbk2_a = re.compile(r"([0-9.]+) Personen gelten als aktuell")

def rbk2(sheets):
    soup = get_soup("https://www.rbk-direkt.de/aktuelles.aspx")
    article = next(a for a in soup.find(id="content-left").findAll("article") if "Corona-Fälle" in a.get_text())
    date = article.find("time").text if article else None
    date = check_date(date, "RBK")
    url = urljoin("https://www.rbk-direkt.de/", article.find(href=True)["href"])
    print("Getting", url)
    assert url
    soup = get_soup(url)
    text = soup.find(id="content-left").find("article").get_text(" ").strip()
    #print(text)
    c = force_int(_rbk2_c.search(text).group(1))
    cc = force_int(_rbk2_cc.search(text).group(1))
    d = force_int(_rbk2_d.search(text).group(1))
    g = force_int(_rbk2_g.search(text).group(1)) if _rbk2_g.search(text) else None
    q = force_int(_rbk2_q.search(text).group(1)) if _rbk2_q.search(text) else None
    a = force_int(_rbk2_a.search(text).group(1)) if _rbk2_a.search(text) else None
    s, i = map(force_int, _rbk2_si.search(text).group(1)) if _rbk2_si.search(text) else (None, None)
    if g is None and a is not None: g = c - d - a
    update(sheets, 5378, c=c, cc=cc, d=d, g=g, q=q, s=s, i=i, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(11, 30, 14, 35, 600, rbk2, 5378))
if __name__ == '__main__': rbk2(googlesheets())
