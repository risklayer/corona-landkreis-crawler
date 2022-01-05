#!/usr/bin/python3
## Tommy

from botbase import *

_lueneburg_date = re.compile(r"Stand: (\d\d?\.\d\d?\.20\d\d)")
_lueneburg_c = re.compile(r"Bestätigte Fälle: ([0-9.]+)\s\(\+\/?\-?([0-9]+)")
_lueneburg_g = re.compile(r"Genesen: ([0-9.]+)")
_lueneburg_d = re.compile(r"Verstorben: ([0-9.]+)")
_lueneburg_s = re.compile(r"([0-9.]+|\w+) Persone?n? wegen COVID-19 in stationärer Behandlung")

def lueneburg(sheets):
    soup = get_soup("https://corona.landkreis-lueneburg.de/aktuelle-situation/")
    date_text = _lueneburg_date.search(soup.find("div", {"class": "aenderungsdatum"}).get_text()).group(1)
    date = check_date(date_text, "Lueneburg")
    content = soup.find("div", {"class": "aktuelles-weitere-zahlen"}).get_text().strip()

    c = force_int(_lueneburg_c.search(content).group(1))
    cc = force_int(_lueneburg_c.search(content).group(2))
    g = force_int(_lueneburg_g.search(content).group(1))
    d = force_int(_lueneburg_d.search(content).group(1))
    s = force_int(_lueneburg_s.search(soup.get_text()).group(1))

    update(sheets, 3355, c=c, cc=cc, d=d, g=g, s=s, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(16, 55, 18, 55, 360, lueneburg, 3355))
if __name__ == '__main__': lueneburg(googlesheets())
