#!/usr/bin/python3
from botbase import *

_traunstein_cc = re.compile(r"([0-9.]+) Neuinfektionen")
_traunstein_c = re.compile(r"insgesamt ([0-9.]+) bestätigte Fälle")
_traunstein_g = re.compile(r"genesen gelten mindestens ([0-9.]+) Personen \(([0-9.]+) Personen mehr")
_traunstein_d = re.compile(r"insgesamt ([0-9.]+) Todesfälle")
_traunstein_dd = re.compile(r"seit (?:\w+ )*([0-9.]+|\w+) Todesmeldungen")
#_traunstein_si = re.compile(r"([0-9.]+) auf der Normalstation und ([0-9.]+) auf der Intensivstation.")

def traunstein(sheets):
    soup = get_soup("https://www.traunstein.com/aktuelles")
    li = next(x for x in soup.findAll("article") if "Covid-Patienten" in x.get_text())
    check_date(li.find(class_="presse_datum").get_text(), "Traunstein")
    link = li.find(href=True)["href"] if li else None
    link = urljoin("https://www.traunstein.com/aktuelles", link)
    print("Getting", link)
    soup = get_soup(link)
    text = soup.find(id="block-system-main").get_text(" ").strip()
    #print(text)
    cc = force_int(_traunstein_cc.search(text).group(1))
    c = force_int(_traunstein_c.search(text).group(1))
    g, gg = map(force_int, _traunstein_g.search(text).groups()) if _traunstein_g.search(text) else (None, None)
    d = force_int(_traunstein_d.search(text).group(1))
    dd = force_int(_traunstein_dd.search(text).group(1)) if _traunstein_dd.search(text) else None
    #s, i = map(force_int, _traunstein_si.search(text).groups())
    #s += i
    update(sheets, 9189, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, comment="Bot ohne SI", ignore_delta="mon")
    return True

schedule.append(Task(14, 0, 16, 35, 360, traunstein, 9189))
if __name__ == '__main__': traunstein(googlesheets())
