#!/usr/bin/python3
## Tommy

from botbase import *

_marburg_date = re.compile(r"Pressemitteilung \| (\d\d?\.\d\d?\.20\d\d)")
_marburg_c = re.compile(r"Die Gesamtzahl der seit März 2020 bestätigten Corona-Infektionen liegt aktuell bei\s([0-9.]+)")
_marburg_cc = re.compile(r"([0-9.]+|\w+) Corona-Neuinfektionen")
_marburg_g1 = re.compile("Die Zahl der genesenen Fälle (?:liegt bei |beträgt )([0-9.]+)")
_marburg_g2 = re.compile("Die Zahl der genesenen Fälle hat sich um ([0-9.]+|\w+) auf ([0-9.]+) erhöht.")
_marburg_d1 = re.compile(r"Die Zahl der Todesfälle im Zusammenhang mit einer Corona-Infektion (?:beträgt |liegt )(?:weiterhin |aktuell )?(?:bei)?([0-9.]+)")
_marburg_d2 = re.compile(r"Die Zahl der Todesfälle im Zusammenhang mit einer Corona-Infektion hat sich(?:.+) ([0-9.]+) erhöht (?:\(\+\d\))?. Das Gesundheitsamt")
_marburg_s = re.compile(r"([0-9.]+|\w+) (?:Menschen|Personen) stationär im Krankenhaus behandelt")
_marburg_i = re.compile(r"([0-9.]+|\w+) (?:Menschen|Personen) eine intensivmedizinische Betreuung")

def marburg(sheets):

    soup = get_soup("https://www.marburg-biedenkopf.de/dienste_und_leistungen/inhalte/index.php")
    entry = next(x for x in soup.find_all("li", {"class": "SP-TeaserList__item"}) if "Infektionen" in x.get_text())
    date_text = _marburg_date.search(entry.find("div", {"class": "SP-Teaser__kicker"}).get_text()).group(1) if entry else None
    link = entry.find("a", {"href": True})["href"] if entry else None
    check_date(date_text, "Marburg-Biedenkopf")
    from urllib.parse import urljoin
    link = urljoin("https://www.marburg-biedenkopf.de/dienste_und_leistungen/inhalte/index.php", link)
    print("Getting", link)

    content = get_soup(link).get_text()

    c = force_int(_marburg_c.search(content).group(1))
    cc = force_int(_marburg_cc.search(content).group(1))

    if _marburg_g1.search(content):
        gg = None
        g = force_int(_marburg_g1.search(content).group(1))

    elif _marburg_g2.search(content):
        gg = force_int(_marburg_g2.search(content).group(1))
        g = force_int(_marburg_g2.search(content).group(2))

    if _marburg_d1.search(content):
        d = force_int(_marburg_d1.search(content).group(1))
    elif _marburg_d2.search(content):
        d = force_int(_marburg_d2.search(content).group(1))

    s = force_int(_marburg_s.search(content).group(1)) if _marburg_s.search(content) is not None else None
    i = force_int(_marburg_i.search(content).group(1)) if _marburg_i.search(content) is not None else None

    update(sheets, 6534, c=c, cc=cc, g=g, gg=gg, d=d, s=s, i=i, sig="Bot")
    return True

schedule.append(Task(15, 47, 17, 47, 360, marburg, 6534))
if __name__ == '__main__': marburg(googlesheets())
