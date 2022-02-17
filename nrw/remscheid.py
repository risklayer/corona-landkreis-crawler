#!/usr/bin/python3
## Tommy
from botbase import *

_remscheid_date = re.compile(r"Corona-Virus \| Aktuelle Gesundheitslage vom (\d\d?\.\d\d?\.20\d\d)")
_remscheid_c = re.compile(r"([0-9.]+) (\(gestern [0-9.]+\) )?positiv getestete Remscheiderinnen und Remscheider")
_remscheid_g = re.compile(r"([0-9.]+) Remscheiderinnen und Remscheider gelten als genesen")
_remscheid_d = re.compile(r"([0-9]+) (?:Menschen|Remscheiderinnen und Remscheider.?) (?:\w+ )+verstorben")
_remscheid_q = re.compile(r"([0-9.]+|\w+) Personen, die als Verdachtsfälle unter häuslicher Quarantäne stehen")
_remscheid_a = re.compile(r"([0-9.]+|\w+) Remscheiderinnen und Remscheider, die an Covid-19 erkrankt sind und sich in (?:angeordneter )?Quarantäne befinden")
_remscheid_s = re.compile(r"([0-9.]+|\w+) Covid-19-erkrankte Personen als sogenannte Hospitalisierungsfälle")
_remscheid_i = re.compile(r"([0-9.]+|\w+) dieser Personen (?:ist|sind) intensivpflichtig")

def remscheid(sheets):
    soup = get_soup("https://www.remscheid.de/neuigkeiten-wissenswertes/corona/index.php")
    entry = next(x for x in soup.find_all("a") if "Corona-Virus | Aktuelle Gesundheitslage" in x.get_text())
    link = entry["href"] if entry else None
    link = urljoin("https://www.remscheid.de/neuigkeiten-wissenswertes/corona/index.php", link)
    print("Getting", link)
    page = get_soup(link)
    check_date(page.find("time").get("datetime"), "Remscheid")
    content = page.get_text(" ")
    #print(content)
    c = force_int(_remscheid_c.search(content).group(1))
    d = force_int(_remscheid_d.search(content).group(1))
    g = force_int(_remscheid_g.search(content).group(1)) if _remscheid_g.search(content) else None
    #a = force_int(_remscheid_a.search(content).group(1))
    q = None #q = force_int(_remscheid_q.search(content).group(1)) + a
    s = force_int(_remscheid_s.search(content).group(1))
    i = force_int(_remscheid_i.search(content).group(1))

    update(sheets, 5120, c=c, d=d, g=g, q=q, s=s, i=i, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(11, 25, 17, 25, 600, remscheid, 5120))
if __name__ == '__main__': remscheid(googlesheets())
