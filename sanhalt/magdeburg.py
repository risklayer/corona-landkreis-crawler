#!/usr/bin/python3
## Tommy
from botbase import *

_magdeburg_date = re.compile(r"Stand (\d\d?\.\d\d?\.20\d\d)")
_magdeburg_cc = re.compile(r"Neue Fälle:\s*([0-9.]+)")
_magdeburg_c = re.compile(r"Fälle insgesamt \(seit März 2020\):\s*([0-9.]+)")
_magdeburg_d = re.compile(r"Verstorbene:\s*([0-9.]+)")

def magdeburg(sheets):
    soup = get_soup("https://www.magdeburg.de/Start/B%C3%BCrger-Stadt/Aktuelles-Presse/Coronavirus-Covid-19/Aktuelle-Zahlen-Informationen-und-Links/")
    header = next(x for x in soup.find_all("h2") if "Aktuelle Zahlen: Magdeburg" in x.get_text())
    date_header = header.findNext("h5")
    date_text = _magdeburg_date.search(date_header.get_text().strip()).group(1)
    check_date(date_text, "Magdeburg")
    content = date_header.findNext("p").get_text().strip()
    c = force_int(_magdeburg_c.search(content).group(1))
    cc = force_int(_magdeburg_cc.search(content).group(1))
    d = force_int(_magdeburg_d.search(content).group(1))
    update(sheets, 15003, c=c, cc=cc, d=d, sig="Vorläufig", comment="LK", ignore_delta="mon")
    return True

schedule.append(Task(14, 56, 16, 56, 360, magdeburg, 15003))
if __name__ == '__main__': magdeburg(googlesheets())

