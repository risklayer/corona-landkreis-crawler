#!/usr/bin/python3
from botbase import *

_enkreis_c = re.compile(r"([0-9.]+) bestätigte")
_enkreis_cc = re.compile(r"um ([0-9.]+) gestiegen")
_enkreis_d = re.compile(r"([0-9.]+) Personen im Zusammenhang mit einer Corona-Infektion verstorben")
_enkreis_d2 = re.compile(r"Todesfälle (?:[^0-9.]*)(?:um [0-9]+ )?auf ([0-9.]+)")
_enkreis_g = re.compile(r"([0-9.]+) Menschen gelten als genesen")
_enkreis_si = re.compile(r"([0-9.]+) Patienten mit einer Corona-Infektion in stationärer Behandlung, ([0-9.]+) Person(?:en)? werden intensiv", re.U)
_enkreis_q = re.compile(r"([0-9.]+) Kreisbewohner in Quarantäne")

def enkreis(sheets):
    from urllib.parse import urljoin
    soup = get_soup("https://www.enkreis.de/")
    articles = soup.findAll(class_="article")
    article = next(a for a in articles if "bestätigte Corona" in a.find(itemprop="description").get_text())
    date = article.find("time").text if article else None
    date = check_date(date, "EN-Kreis")
    url = urljoin("https://www.enkreis.de/", article.find("a")["href"])
    print("Getting", url)
    assert url
    soup = get_soup(url)
    text = "\n".join(p.get_text(" ") for p in soup.find(class_="article").findAll("p"))
    #print(text)
    c = force_int(_enkreis_c.search(text).group(1))
    cc = force_int(_enkreis_cc.search(text).group(1))
    d = force_int((_enkreis_d.search(text) or _enkreis_d2.search(text)).group(1))
    g = force_int(_enkreis_g.search(text).group(1))
    s, i, q = None, None, None
    m = _enkreis_q.search(text)
    if m: q = force_int(m.group(1))
    m = _enkreis_si.search(text)
    if m: s, i = force_int(m.group(1)), force_int(m.group(2))
    update(sheets, 5954, c=c, cc=cc, d=d, g=g, q=q, s=s, i=i, sig="Bot")
    return True

schedule.append(Task(11, 30, 14, 35, 360, enkreis, 5954))
if __name__ == '__main__': enkreis(googlesheets())
