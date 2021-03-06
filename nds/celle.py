#!/usr/bin/python3
## Tommy
from botbase import *

_celle_date = re.compile(r"Stand (\d\d?\.\d\d?\.20\d\d)")
_celle_cc = re.compile(r"([0-9.]+|\w+)\sNeuinfektionen")
_celle_cc2 = re.compile(r"Seit \w+ wurden im Landkreis Celle\s([0-9.]+|\w+)\sPersonen positiv")
_celle_c = re.compile(r"ie\s+Zahl\s+der\s+seit\s+Beginn\s+der\s+Pandemie\s+im\s+März\s+2020\s+(?:im\s+Landkreis\s+Celle\s+)?(?:[eE]rkrankten|[iI]nfizierten)\s+(?:Personen\s+)?(?:liegt\s+bei|erhöht\s+sich\s+\w*\s*auf)\s*([0-9.]+)")
#_celle_a = re.compile(r"Aktuell sind mit dem Coronavirus im Landkreis Celle ([0-9.]+|\w+)")
#_celle_q = re.compile(r"([0-9.]+|\w+) Menschen in Quarantäne")
_celle_s = re.compile(r"([0-9.]+|\w+)\s+(?:positiv\s+getestete\s+)?Personen\s+behandelt")
_celle_i = re.compile(r"uf\s+der\s+Intensivstation\s+lieg\w*\s+(?:derzeit )?([0-9.]+|kei\w*|nie\w*)")
_celle_i2 = re.compile(r"([0-9.]+|\w+)\s+Person\w*\s+auf\s+der\s+Intensivstation")

def celle(sheets):
    soup = get_soup("https://www.landkreis-celle.de/")
    entry = next(x for x in soup.find_all("a", title=True) if "Situation SARS-CoV-2" in x["title"])
    date_text = _celle_date.search(entry["title"]).group(1)
    check_date(date_text, "Celle")
    link = entry["href"] if entry else None
    link = urljoin("https://www.landkreis-celle.de/", link)
    print("Getting", link)
    content = get_soup(link).get_text()
    #print(content)
    c = force_int(_celle_c.search(content).group(1))
    cc = force_int((_celle_cc.search(content) or _celle_cc2.search(content)).group(1))
    #a = force_int(_celle_a.search(content).group(1))
    #q = force_int(_celle_q.search(content).group(1)) + a
    s, i = None, None
    try:
        s = force_int(_celle_s.search(content).group(1))
    except: pass
    try:
        i = force_int((_celle_i.search(content) or _celle_i2.search(content)).group(1))
    except: pass

    update(sheets, 3351, c=c, cc=cc, s=s, i=i, ignore_delta=True)
    return True

schedule.append(Task(10, 15, 12, 15, 360, celle, 3351))
if __name__ == '__main__': celle(googlesheets())

