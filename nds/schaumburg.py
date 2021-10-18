#!/usr/bin/python3
from botbase import *

_schaumburg_c = re.compile(r"um ([0-9.]+) Personen auf insgesamt ([0-9.]+)", re.U)
_schaumburg_c2 = re.compile(r"Von ([0-9.]+) Infektionsfällen", re.U)
_schaumburg_a = re.compile(r"([0-9.]+) Menschen akut", re.U)
_schaumburg_g = re.compile(r"([0-9.]+) Personen inzwischen als geheilt", re.U)
_schaumburg_q = re.compile(r"([0-9.]+) Personen unter Quarantäne", re.U)
_schaumburg_s = re.compile(r"([0-9.]+) Personen der Erkrankten in stationärer", re.U)

def schaumburg(sheets):
    from urllib.parse import urljoin
    soup = get_soup("https://www.schaumburg.de/Coronavirus/")
    articles = soup.findAll("article")
    article = next(a for a in articles if "Corona Fälle Stand" in a.find("h3").get_text())
    date = article.find(class_="date").text if article else None
    date = check_date(date, "Schaumburg")
    url = urljoin("https://www.schaumburg.de/", article.find("a")["href"])
    print("Getting", url)
    assert url
    soup = get_soup(url)
    content = soup.find("article")
    text = content.get_text().strip()
    #print(text)
    if "nicht gestiegen" in text:
        cc, c = 0, force_int(_schaumburg_c2.search(text).group(1))
    else:
        cc, c = map(force_int, _schaumburg_c.search(text).groups())
    a = force_int(_schaumburg_a.search(text).group(1))
    g = force_int(_schaumburg_g.search(text).group(1))
    q = force_int(_schaumburg_q.search(text).group(1))
    s = force_int(_schaumburg_s.search(text).group(1)) if _schaumburg_s.search(text) is not None else None
    d = c - a - g
    update(sheets, 3257, c=c, cc=cc, d=d, g=g, q=q, s=s, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(12, 32, 15, 35, 360, schaumburg, 3257))
if __name__ == '__main__': schaumburg(googlesheets())

