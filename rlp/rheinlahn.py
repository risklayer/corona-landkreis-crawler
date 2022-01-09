#!/usr/bin/python3
## Tommy
from botbase import *

_rheinlahn_c = re.compile(r"Gesamtinfizierte:\s*([0-9.]+)")
_rheinlahn_d = re.compile(r"Verstorbene:\s*([0-9.]+)")
_rheinlahn_g = re.compile(r"Genesene:\s*([0-9.]+)")

def rheinlahn(sheets):
    soup = get_soup("https://www.rhein-lahn-kreis.de/aktuelles/corona/")
    article = next(x for x in soup.find("div", {"class":"article-teaser-list"}).find_all("article") if "Aktuelle Corona-Lage" in x.get_text() or "Impfungen im Impfzentrum" in x.get_text())
    date = datetime.datetime.fromtimestamp(int(article["data-date"])//1000)
    check_date(date, "Rhein-Lahn")
    link = article.find("a")["href"]
    from urllib.parse import urljoin
    link = urljoin("https://www.rhein-lahn-kreis.de/aktuelles/corona/", link)
    print("Getting", link)
    content = get_soup(link).get_text()
    c = force_int(_rheinlahn_c.search(content).group(1))
    d = force_int(_rheinlahn_d.search(content).group(1))
    g = force_int(_rheinlahn_g.search(content).group(1))
    update(sheets, 7141, c=c, d=d, g=g, sig="Bot")
    return True

schedule.append(Task(13, 35, 15, 35, 360, rheinlahn, 7141))
if __name__ == '__main__': rheinlahn(googlesheets())


