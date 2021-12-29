#!/usr/bin/python3
## Tommy
from botbase import *

_vulkaneifel_c = re.compile(r"Die Anzahl der bisher positiv auf das Corona-Virus getesteten Personen mit Wohnsitz im Landkreis Vulkaneifel liegt bei ([0-9.]+)")
_vulkaneifel_cc = re.compile(r"([0-9.]+|\w+) bestätigte Neuinfektionen")
_vulkaneifel_d = re.compile(r"([0-9.]+) Todesfälle im Zusammenhang mit COVID-19 zu beklagen")
_vulkaneifel_g = re.compile(r"genesen bislang insgesamt ([0-9.]+)")
_vulkaneifel_gg = re.compile(r"([0-9.]+) Personen seit dem gestrigen Tag")
_vulkaneifel_s = re.compile(r"(-?[0-9.]+|\w+) der positiv auf COVID-19 getesteten Personen bedürfen aktuell einer stationären Behandlung")

def vulkaneifel(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.vulkaneifel.de/buergerservice-verwaltung/corona/corona-presse.html")
    entry = next(x for x in soup.find_all("article") if "COVID-19 Tagesmeldung" in x.get_text())
    if not today().strftime("%e. %B %Y") in entry.get_text(): raise NotYetAvailableException("Vulkaneifel noch alt:" + entry.get_text().strip("\n").split("\n")[0].strip())
    link = entry.find(href=True)["href"] if entry else None
    from urllib.parse import urljoin
    link = urljoin("https://www.vulkaneifel.de/buergerservice-verwaltung/corona/corona-presse.html", link)
    print("Getting", link)
    content = get_soup(link).get_text()
    c = force_int(_vulkaneifel_c.search(content).group(1))
    cc = force_int(_vulkaneifel_cc.search(content).group(1))
    d = force_int(_vulkaneifel_d.search(content).group(1))
    g = force_int(_vulkaneifel_g.search(content).group(1))
    gg = force_int(_vulkaneifel_gg.search(content).group(1))
    s = force_int(_vulkaneifel_s.search(content).group(1)) if _vulkaneifel_s.search(content) else None
    update(sheets, 7233, c=c, cc=cc, d=d, g=g, gg=gg, s=s, sig="Bot")
    return True

schedule.append(Task(10, 50, 12, 50, 360, vulkaneifel, 7233))
if __name__ == '__main__': vulkaneifel(googlesheets())
