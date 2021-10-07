#!/usr/bin/python3
from botbase import *

_northeim_c = re.compile(r"mittlerweile ([0-9.]+)\s*\(([+-]?[0-9.]+)\) Corona-Infektionen")
_northeim_g = re.compile(r"([0-9.]+)\s*\(([+-]?[0-9.]+)\) Personen gelten mittlerweile als genesen")
_northeim_d = re.compile(r"insgesamt ([0-9.]+)\s*\(([+-]?[0-9.]+)\) Personen verstorben")

def northeim(sheets):
    from urllib.parse import urljoin
    soup = get_soup("https://www.landkreis-northeim.de/portal/seiten/fallzahlen-im-landkreis-northeim-900000280-23900.html?rubrik=900000070")
    articles = soup.findAll(itemtype="http://schema.org/Article")
    article = next(a for a in articles if "Coronavirus - Entwicklung" in a.find("h4").get_text())
    date = article.find(class_="nolis-list-date").text if article else None
    date = check_date(date, "Northeim")
    url = urljoin("https://www.landkreis-northeim.de/", article.find("a")["href"])
    print("Getting", url)
    assert url
    soup = get_soup(url)
    text = soup.find(id="nolis_content_site").get_text(" ")
    #text = "\n".join(p.get_text(" ") for p in soup.find(itemprop="articleBody").findAll("p"))
    #print(text)
    c, cc = map(force_int, _northeim_c.search(text).groups())
    d, dd = map(force_int, _northeim_d.search(text).groups())
    g, gg = map(force_int, _northeim_g.search(text).groups())
    update(sheets, 3155, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, sig="Bot")
    return True

schedule.append(Task(13, 00, 14, 55, 360, northeim, 3155))
if __name__ == '__main__': northeim(googlesheets())
