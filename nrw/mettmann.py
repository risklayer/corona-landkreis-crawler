#!/usr/bin/python3
from botbase import *

_mettmann_a = re.compile(r"([0-9.]+)\sInfizierte\serfasst")
_mettmann_d = re.compile(r"Verstorbene zählt der Kreis (?:damit |demnach |bislang |insgesamt )*([0-9.]*)\.")
_mettmann_g = re.compile(r"([0-9.]+)\sPersonen\sgelten\sals\sgenesen")

def mettmann(sheets):
    from urllib.parse import urljoin
    soup = get_soup("https://www.kreis-mettmann-corona.de/Aktuelle-Meldungen/")
    article = soup.find(class_="mitteilungen").findAll("li")
    article = next(x for x in article if "Genesene," in x.get_text())
    if not today().strftime("%d.%m.%Y") in article.get_text(): raise NotYetAvailableException("Mettmann noch alt: "+article.find(class_="list-text").find("small").get_text())
    url = urljoin("https://www.kreis-mettmann-corona.de/Aktuelle-Meldungen/", article.find("a")["href"])
    print("Getting", url)
    assert url
    soup = get_soup(url)
    text = "\n".join(p.get_text(" ") for p in soup.find("article").findAll("p"))
    #print(text)
    a = force_int(_mettmann_a.search(text).group(1))
    d = force_int(_mettmann_d.search(text).group(1))
    g = force_int(_mettmann_g.search(text).group(1))
    c = a + d + g
    update(sheets, 5158, c=c, d=d, g=g, comment="Bot ohne QS")
    return True

schedule.append(Task(11, 55, 13, 35, 360, mettmann, 5158))
if __name__ == '__main__': mettmann(googlesheets())
