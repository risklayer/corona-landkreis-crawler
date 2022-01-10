#!/usr/bin/python3
## Tommy
from botbase import *

_ingolstadt_g = re.compile(r"Genesene: ([0-9.]+)")
_ingolstadt_d = re.compile(r"Gestorbene: ([0-9.]+)")
_ingolstadt_c = re.compile(r"Fälle insgesamt: ([0-9.]+)")
_ingolstadt_cc = re.compile(r"Entwicklung:\s([0-9.]+)")
_ingolstadt_s = re.compile(r"Im Klinikum Ingolstadt werden derzeit ([0-9.]+|\w+)")
_ingolstadt_i = re.compile(r"([0-9.]+|\w+) Patienten liegen auf der Intensivstation")

def ingolstadt(sheets):
    soup = get_soup("https://www.ingolstadt.de/Rathaus/Aktuelles/Aktuelle-Meldungen/Newsticker-Coronavirus/")
    entry = next(x for x in soup.find_all("div", {"class":"mitteilungen clearfix"}) if "Entwicklung lokaler Zahlen Corona" in x.get_text())
    date_text = entry.find("div", {"class": "date"}).get_text()
    check_date(date_text, "Ingolstadt")

    link = entry.find("a", {"href": True})["href"] if entry else None
    from urllib.parse import urljoin
    link = urljoin("https://www.ingolstadt.de/Rathaus/Aktuelles/Aktuelle-Meldungen/Newsticker-Coronavirus/", link)
    print("Getting", link)

    content = get_soup(link).get_text()
    c = force_int(_ingolstadt_c.search(content).group(1))
    cc = force_int(_ingolstadt_cc.search(content).group(1))
    g = force_int(_ingolstadt_g.search(content).group(1))
    d = force_int(_ingolstadt_d.search(content).group(1))
    s = force_int(_ingolstadt_s.search(content).group(1))
    i = force_int(_ingolstadt_i.search(content).group(1))

    update(sheets, 9161, c=c, cc=cc, g=g, d=d, s=s, i=i, ignore_delta=True)
    return True

schedule.append(Task(13, 25, 15, 25, 360, ingolstadt, 9161))
if __name__ == '__main__': ingolstadt(googlesheets())
