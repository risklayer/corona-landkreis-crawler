#!/usr/bin/python3
from botbase import *

_viersen_cc = re.compile(r"([0-9.]+) neue Infektionen")
_viersen_s = re.compile(r"([0-9.]+|\w+) Menschen werden stationär behandelt", re.U)
_viersen_i = re.compile(r"([0-9.]+|\w+) befinden sich auf der Intensiv", re.U)
_viersen_q = re.compile(r"([0-9.]+) Kontaktpersonen befinden")

def viersen(sheets):
    from urllib.parse import urljoin
    soup = get_soup("https://www.presse-service.de/meldungen.aspx?ps_id=1381")
    articles = soup.find(class_="ps_meldungsliste").findAll("li")
    #print(*[a.get_text() for a in articles], sep"\n")
    article = next(a for a in articles if "Sieben-Tage-Inzidenz" in a.get_text() or "Neuinfektionen" in a.get_text())
    if not today().strftime("%d.%m.%Y") in article.get_text(): raise NotYetAvailableException("Viersen noch alt: "+article.get_text().strip().split("\n")[0])
    url = urljoin("https://www.presse-service.de/meldungen.aspx?ps_id=1381", article.find("a")["href"])
    print("Getting", url)
    assert url
    soup = get_soup(url)
    main = soup.find(class_="ps_content")
    text = main.get_text(" ").strip()
    #print(text)
    table = next(t for t in main.findAll("table") if "bestätigte Fälle" in t.get_text())
    rows = [[x.get_text().strip() for x in y] for y in table.findAll("tr")]
    #print(*rows, sep="\n")
    assert "Gesamt" in rows[-1][1]
    assert "bestätigte Fälle" in rows[0][3]
    assert "Genesene" in rows[0][7]
    assert "verstorben" in rows[0][9]
    c, g, d = map(force_int, [rows[-1][3], rows[-1][7], rows[-1][9]])
    cc = force_int(_viersen_cc.search(text).group(1))
    s, i, q = None, None, None
    m = _viersen_q.search(text)
    if m: q = force_int(m.group(1)) + c - d - g
    m = _viersen_s.search(text)
    if m: s = force_int(m.group(1))
    m = _viersen_i.search(text)
    if m: i = force_int(m.group(1))
    update(sheets, 5166, c=c, cc=cc, d=d, g=g, q=q, s=s, i=i, sig="Bot")
    return True

schedule.append(Task(15, 30, 18, 35, 360, viersen, 5166))
if __name__ == '__main__': viersen(googlesheets())
