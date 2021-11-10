#!/usr/bin/python3
from botbase import *

_miltenberg_c = re.compile(r"Coronavirus-Infektionen beläuft sich auf ([0-9.]+) Fälle")
_miltenberg_cc = re.compile(r"([0-9.]+) Neuinfektionen")
_miltenberg_d = re.compile(r"gab (?:bisher )?([0-9.]+) Todesfälle")
_miltenberg_a = re.compile(r"Aktuell befinden sich ([0-9.]+) mit SARS-CoV-2 infizierte")
_miltenberg_q = re.compile(r"([0-9.]+) Menschen als Kontaktperson I in Quarantäne")
_miltenberg_si = re.compile(r"([0-9.]+|\w+) Persone?n? aus dem Landkreis in stationärer Behandlung(?:, davon sind ([0-9.]+|\w+) intensiv)?", re.U)

def miltenberg(sheets):
    from urllib.parse import urljoin
    soup = get_soup("https://www.landkreis-miltenberg.de/Landkreis/Aktuell.aspx")
    articles = soup.find(id="aktuell").findAll("li")
    todaystr = today().strftime("%d.%m.%Y")
    article = next(a for a in articles if todaystr in a.get_text() and "Fallzahlen im Landkreis" in a.get_text())
    date = check_date(todaystr if article else articles[0].get_text(), "Miltenberg")
    url = urljoin("https://www.landkreis-miltenberg.de/Landkreis/", article.find("a")["href"])
    print("Getting", url)
    assert url
    soup = get_soup(url)
    text = soup.find(id="news_beschreibung").get_text()
    #print(text)
    a = force_int(_miltenberg_a.search(text).group(1))
    c = force_int(_miltenberg_c.search(text).group(1))
    cc = force_int(_miltenberg_cc.search(text).group(1))
    d = force_int(_miltenberg_d.search(text).group(1))
    q = force_int(_miltenberg_q.search(text).group(1))
    g = c - d - a
    q = q + a
    s, i = map(force_int, _miltenberg_si.search(text).groups())
    update(sheets, 9676, c=c, cc=cc, d=d, g=g, q=q, s=s, i=i, sig="Bot")
    return True

schedule.append(Task(11, 30, 15, 35, 360, miltenberg, 9676))
if __name__ == '__main__': miltenberg(googlesheets())
