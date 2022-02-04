#!/usr/bin/python3
from botbase import *

_mannheim_c = re.compile(r"bestätigten Fälle in Mannheim erhöht sich deshalb auf insgesamt ([0-9.]+)")
_mannheim_cc = re.compile(r"([0-9.]+) weitere Fälle einer nachgewiesenen Coronavirus-Infektion")
_mannheim_g = re.compile(r"gelten in Mannheim ([0-9.]+) Personen als genesen")
_mannheim_a = re.compile(r"([0-9.]+) akute Infektionsfälle")
_mannheim_d = re.compile(r"seit Beginn der Pandemie ([0-9.]+) Todesfälle")
_mannheim_dd = re.compile(r"heute ([0-9]+|\w+) weiteren? Todesf[aä]lle?")

def mannheim(sheets):
    data = get_soup("https://www.mannheim.de/de/informationen-zu-corona/aktuelle-situation-in-mannheim")
    link = next(x.find("a") for x in data.findAll("h5") if "Aktuelle Meldung zu Corona" in x.get_text())
    #print(link)
    if not today().strftime("%d.%m.%Y") in link.get_text(): raise NotYetAvailableException("Mannheim: "+link.get_text())
    link = urljoin("https://www.mannheim.de/de/informationen-zu-corona/aktuelle-situation-in-mannheim", link["href"])
    print("Getting", link)
    data = get_soup(link)
    text = data.find("main").find("article").get_text()
    c = force_int(_mannheim_c.search(text).group(1))
    cc = force_int(_mannheim_cc.search(text).group(1))
    g = force_int(_mannheim_g.search(text).group(1))
    a = force_int(_mannheim_a.search(text).group(1))
    m = _mannheim_d.search(text)
    d = force_int(m.group(1)) if m else c - g - a
    m = _mannheim_dd.search(text)
    dd = force_int(m.group(1)) if m else None
    #if d is None: d = c - g - a
    update(sheets, 8222, c=c, cc=cc, g=g, d=d, dd=dd, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(17, 30, 19, 30, 360, mannheim, 8222))
if __name__ == '__main__': mannheim(googlesheets())
