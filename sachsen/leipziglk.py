#!/usr/bin/python3
from botbase import *

_leipziglk_c = re.compile(r"wurden\s+([0-9.]+)\s+\(\+\s*(-?[0-9]+) zum")
_leipziglk_d = re.compile(r"\s+([0-9.]+)\s+\(\+\s*(-?[0-9]+)\)\s+Todesfälle")
_leipziglk_a = re.compile(r"([0-9.]+) infizierte")
_leipziglk_q = re.compile(r"([0-9.]+) Personen in Quarantäne")

def leipziglk(sheets):
    from urllib.parse import urljoin
    soup = get_soup("https://www.landkreisleipzig.de/pressemeldungen.html")
    articles = soup.findAll("article")
    article = next(a for a in articles if "bestätigte Fälle" in a.find("h2").get_text())
    date = article.find("time").text if article else None
    #print(date)
    date = check_date(date.split(" ")[1], "LK Leipzig")
    url = urljoin("https://www.landkreisleipzig.de/", article.find("a")["href"])
    print("Getting", url)
    assert url
    soup = get_soup(url)
    text = soup.find(itemprop="articleBody").get_text(" ")
    #print(text)
    c, cc = map(force_int, _leipziglk_c.search(text).groups())
    d, dd = map(force_int, _leipziglk_d.search(text).groups())
    a = force_int(_leipziglk_a.search(text).group(1))
    q = force_int(_leipziglk_q.search(text).group(1))
    g = c - d - a
    update(sheets, 14729, c=c, cc=cc, d=d, dd=dd, g=g, q=q, sig="Bot")
    return True

schedule.append(Task(12, 30, 15, 35, 360, leipziglk, 14729))
if __name__ == '__main__': leipziglk(googlesheets())
