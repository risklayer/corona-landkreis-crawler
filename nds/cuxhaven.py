#!/usr/bin/python3
from botbase import *

_cux_two = re.compile(r"([0-9.]+) Persone?n? (?:\(\+?(-?[0-9]+) im Vergleich)?")

def cuxhaven(sheets):
    from urllib.parse import urljoin
    #soup = get_soup("https://www.landkreis-cuxhaven.de/Quicknavigation/Aktuelles/")
    soup = get_soup("https://www.landkreis-cuxhaven.de/Corona/index.php?La=1&object=tx,3189.696.1&kat=&kuo=2&sub=0")
    articles = soup.find(role="main").findAll(class_="mitteilungen")
    article = next(a for a in articles if "Aktuelle Informationen" in a.get_text())
    date = article.find(class_="date").text if article else None
    date = check_date(date, "Cuxhaven")
    url = urljoin("https://www.landkreis-cuxhaven.de/Quicknavigation/Aktuelles/", article.find(href=True)["href"])
    print("Getting", url)
    assert url
    soup = get_soup(url)
    main = soup.find(role="main").find(class_="mitteilungen_detail")
    rows = [[x.get_text(" ").strip() for x in r.findAll("td")] for r in main.find("table").findAll("tr")]
    #print(*rows, sep="\n")
    assert "bestätigten Infektionen" in rows[0][0]
    c, cc = map(force_int, _cux_two.search(rows[0][1]).groups())
    assert "ohne akute" in rows[2][0]
    g, gg = map(force_int, _cux_two.search(rows[2][1]).groups())
    assert "Todesfälle" in rows[3][0]
    d, dd = map(force_int, _cux_two.search(rows[3][1]).groups())
    assert "Intensiv" in rows[6][0]
    i, _ = map(force_int, _cux_two.search(rows[6][1]).groups())
    update(sheets, 3352, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, i=i, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(15, 0, 17, 35, 360, cuxhaven, 3352))
if __name__ == '__main__': cuxhaven(googlesheets())
