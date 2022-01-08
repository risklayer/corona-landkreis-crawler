#!/usr/bin/python3
from botbase import *

_herford_c = re.compile(r"kreisweit bislang ([0-9.]+) infizierte")
_herford_cc = re.compile(r"([0-9.]+)\** neue (?:Corona-)?Fälle")
_herford_d = re.compile(r"im Kreis Herford ([0-9.]+) Todesfälle")
_herford_g = re.compile(r"gelten ([0-9.]+) Personen als genesen")
_herford_s = re.compile(r"([0-9.]+) Patient.innen mit einer COVID-19-Infektion stationär")
_herford_i = re.compile(r"davon werden ([0-9.]+|\w+) Personen intensiv")

def herford(sheets):
    from urllib.parse import urljoin
    soup = get_soup("https://www.kreis-herford.de/index.php?NavID=2807.178")
    articles = soup.find(id="inhalt").findAll(class_="mitteilungen")
    article = next(a for a in articles if "Corona Update" in a.get_text())
    date = article.find(class_="date").text if article else None
    date = check_date(date, "Herford")
    url = urljoin("https://www.kreis-herford.de/", article.find(href=True)["href"])
    print("Getting", url)
    assert url
    soup = get_soup(url)
    text = soup.find(id="inhalt").get_text().strip()
    #print(text)
    c = force_int(_herford_c.search(text).group(1))
    cc = force_int(_herford_cc.search(text).group(1))
    d = force_int(_herford_d.search(text).group(1))
    g = force_int(_herford_g.search(text).group(1))
    s, i = None, None
    m = _herford_s.search(text)
    if m: s = force_int(m.group(1))
    m = _herford_i.search(text)
    if m: i = force_int(m.group(1))
    update(sheets, 5758, c=c, cc=cc, d=d, g=g, s=s, i=i, sig="Bot", ignore_delta=True) #"mon")
    return True

schedule.append(Task(11, 30, 15, 35, 360, herford, 5758))
if __name__ == '__main__': herford(googlesheets())
