#!/usr/bin/python3
## Tommy
from botbase import *

_celle_date = re.compile(r"Stand (\d\d?\.\d\d?\.20\d\d)")
_celle_cc = re.compile(r"([0-9.]+|\w+)\sNeuinfektionen")
_celle_c = re.compile(r"ie Zahl der seit Beginn der Pandemie im März 2020 (?:im Landkreis Celle )?[eE]rkrankten (?:Personen )?(?:liegt bei|erhöht sich \w*\s*auf) ([0-9.]+)")
#_celle_a = re.compile(r"Aktuell sind mit dem Coronavirus im Landkreis Celle ([0-9.]+|\w+)")
#_celle_q = re.compile(r"([0-9.]+|\w+) Menschen in Quarantäne")
_celle_s = re.compile(r"([0-9.]+|\w+) (?:positiv getestete )?Personen behandelt")
_celle_i = re.compile(r"Auf der Intensivstation lieg\w* ([0-9.]+|\w+)")

def celle(sheets):
    soup = get_soup("https://www.landkreis-celle.de/")
    entry = next(x for x in soup.find_all("a", title=True) if "Situation SARS-CoV-2" in x["title"])
    date_text = _celle_date.search(entry["title"]).group(1)
    check_date(date_text, "Celle")
    link = entry["href"] if entry else None
    from urllib.parse import urljoin
    link = urljoin("https://www.landkreis-celle.de/", link)
    print("Getting", link)
    content = get_soup(link).get_text()
    #print(content)
    c = force_int(_celle_c.search(content).group(1))
    cc = force_int(_celle_cc.search(content).group(1))
    #a = force_int(_celle_a.search(content).group(1))
    #q = force_int(_celle_q.search(content).group(1)) + a
    s = force_int(_celle_s.search(content).group(1))
    i = force_int(_celle_i.search(content).group(1))

    update(sheets, 3351, c=c, cc=cc, s=s, i=i, ignore_delta=True)
    return True

schedule.append(Task(10, 15, 12, 15, 360, celle, 3351))
if __name__ == '__main__': celle(googlesheets())

