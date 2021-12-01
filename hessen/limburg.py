#!/usr/bin/python3
from botbase import *

_limburg_c = re.compile(r"Insgesamt gab es bislang ([0-9.]+) bestätigte Fälle \(\+?/?\s*(-?\s*[0-9.]+) zu")
_limburg_g = re.compile(r"([0-9.]+) Personen sind inzwischen genesen \(\+?/?\s*(-?\s*[0-9.]+) zu")
_limburg_d = re.compile(r"([0-9.]+) Personen sind leider in Verbindung mit dem Corona-Virus verstorben")
_limburg_si = re.compile(r"(\d+) mit dem Corona-Virus infizierte Person\w+ im Normalpflegebett und (\d+) Person\w+ im Intensivbett")
_limburg_q = re.compile(r"([0-9.]+) Menschen befinden sich im Landkreis derzeit in Quarantäne")

def limburg(sheets):
    soup = get_soup("https://www.landkreis-limburg-weilburg.de/leben-im-landkreis/gesundheit/informationen-zum-corona-virus")
    li = next(x for x in soup.find(id="maincontent").findAll(itemtype="http://schema.org/Article") if "Limburg-Weilburg zum Corona-Virus" in x.get_text())
    check_date(li.find("time").get_text(), "Limburg-Weilburg")
    link = li.find("a")["href"] if li else None
    from urllib.parse import urljoin
    link = urljoin("https://www.landkreis-limburg-weilburg.de/leben-im-landkreis/gesundheit/informationen-zum-corona-virus", link)
    print("Getting", link)
    soup = get_soup(link)
    text = soup.find(id="maincontent").get_text()
    #print(text)
    c, cc = map(force_int, _limburg_c.search(text).groups())
    d = force_int(_limburg_d.search(text).group(1))
    g, gg = map(force_int, _limburg_g.search(text).groups())
    s, i = map(force_int, _limburg_si.search(text).groups())
    s = s + i
    q = force_int(_limburg_q.search(text).group(1))
    update(sheets, 6533, c=c, cc=cc, d=d, g=g, gg=gg, q=q, s=s, i=i)
    return True

schedule.append(Task(10, 15, 15, 35, 360, limburg, 6533))
if __name__ == '__main__': limburg(googlesheets())
