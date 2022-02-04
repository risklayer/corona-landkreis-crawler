#!/usr/bin/python3
from botbase import *

_emden_cc = re.compile(r"(?:ha\w+en\swir\s(?:erneut\s)?|Gesundheitsamt)\s*([0-9.]+|\w+)\s+(?:Corona-)?Neuinfektion(?:en)?")
_emden = re.compile(r"([0-9.]+)\s(?:Personen|Infektionen)\s*,\svon\sdenen\s*([0-9.]+)\s(?:\(\+?(-?\s*[0-9.]+)\)\s)?Personen\sgenesen\sund\s([0-9.]+)\s(?:\(\+?(-?\s*[0-9.]+)\)\s)?Personen\sverstorben")
_emden_q = re.compile(r"[Ii]n\sQuarantäne\sbefind\w+\s(?:\w+\s)*([0-9.]+)", re.U)

def emden(sheets):
    soup = get_soup("https://www.emden.de/nachrichten")
    articles = soup.findAll(itemtype="http://schema.org/Article")
    article = next(a for a in articles if "Neuinfektion" in a.find("h3").get_text())
    date = article.find("time").text if article else None
    date = check_date(date, "Emden")
    url = urljoin("https://www.emden.de/", article.find("a")["href"])
    print("Getting", url)
    assert url
    soup = get_soup(url)
    text = "\n".join(p.get_text(" ") for p in soup.find(itemprop="articleBody").findAll("p"))
    #print(text)
    c, g, gg, d, dd = map(force_int, _emden.search(text).groups())
    cc = force_int(_emden_cc.search(text).group(1))
    q = force_int(_emden_q.search(text).group(1))
    update(sheets, 3402, c=c, cc=cc, d=d, dd=dd, g=g, q=q, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(9, 30, 13, 35, 360, emden, 3402))
if __name__ == '__main__': emden(googlesheets())
