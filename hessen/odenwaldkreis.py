#!/usr/bin/python3
from botbase import *

_odenwaldkreis_st = re.compile(r"[Aa]m (?:\w+ \()?(\d\d?\. \w+)\)?")
_odenwaldkreis_c = re.compile(r"um ([0-9.]+|\w+) auf ([0-9]+\.[0-9]{3})")
_odenwaldkreis_c2 = re.compile(r"([0-9.]+) neue positive Corona-Testergebnisse \(Gesamt ([0-9.]+)\)")
_odenwaldkreis_g = re.compile(r"[Gg]elten ([0-9.]+) Personen als genesen(?: – ([0-9.]+|\w) mehr als am Vortag)?")
_odenwaldkreis_g2 = re.compile(r"([0-9.]+|\w+) weitere Persone?n? (?:sind|gelten als) genesen(?: \(\w+esamt ([0-9.]+|\w))?")
_odenwaldkreis_d1 = re.compile(r"Zahl der (?:Todesfälle|[Vv]erstorb\w+) (?:\w+\s+)+\(?([0-9.]+)\)?")
_odenwaldkreis_d2 = re.compile(r"([0-9.]+) (?:Todesfälle|[\w\s]+verstorben)")
_odenwaldkreis_si = re.compile(r"aktuell ([0-9.]+|\w+) Patienten behandelt, davon ([0-9.]+|\w+) (?:intensiv|auf der Intensiv)")

def odenwaldkreis(sheets):
    soup = get_soup("https://www.odenwaldkreis.de/index.php?id=154")
    li = next(x for x in soup.find(id="main").findAll(class_="news-list-item") if "Die Zahl der positiven" in x.get_text() or "Inzidenz" in x.get_text() or "Neuinfektion" in x.get_text() or "Gesamtzahl" in x.get_text())
    #print(li.get_text())
    m = _odenwaldkreis_st.search(li.get_text())
    check_date(m.group(1) if m else li.get_text()[:60], "Odenwaldkreis", datetime.timedelta(1))
    link = li.find(href=True)["href"] if li else None
    from urllib.parse import urljoin
    link = urljoin("https://www.odenwaldkreis.de/index.php?id=154", link)
    print("Getting", link)
    soup = get_soup(link)
    text = soup.find(itemtype="http://schema.org/Article").get_text()
    #print(text)
    cc, c = map(force_int, (_odenwaldkreis_c.search(text) or _odenwaldkreis_c2.search(text)).groups())
    g, gg = None, None
    m = _odenwaldkreis_g.search(text)
    if m: g, gg = map(force_int, m.groups())
    m = _odenwaldkreis_g2.search(text)
    if m: gg, g = map(force_int, m.groups()) # andere Reihenfolge!
    d = force_int((_odenwaldkreis_d1.search(text) or _odenwaldkreis_d2.search(text)).group(1))
    s, i = map(force_int, _odenwaldkreis_si.search(text).groups())
    update(sheets, 6437, c=c, cc=cc, d=d, g=g, gg=gg, s=s, i=i, comment="Bot beta")
    return True

schedule.append(Task(9, 30, 11, 35, 600, odenwaldkreis, 6437))
if __name__ == '__main__': odenwaldkreis(googlesheets())
