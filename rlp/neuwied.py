#!/usr/bin/python3
## Tommy
from botbase import *

_neuwied_date = re.compile(r"Stand (\d\d?\.\d\d?\.20\d\d)")

def neuwied(sheets):
    soup = get_soup("https://www.kreis-neuwied.de/kv_neuwied/Home/Aktuelles/wichtige%20Hinweise%20und%20Informationen/")
    link = next(x["href"] for x in soup.find("ul", {"class": "newsteaser small-block-grid-1 one-in-row"}).find_all("a", {"href": True}) if "Aktuelle Corona-Fallzahlen für den Landkreis Neuwied" in x.get_text())
    link = urljoin("https://www.kreis-neuwied.de/kv_neuwied/Home/Aktuelles/wichtige%20Hinweise%20und%20Informationen/", link)
    print("Getting", link)
    content = get_soup(link).find("div", {"class": "content"})
    if content.find("strike") is not None: return True # defekt
    date_text = _neuwied_date.search(content.get_text()).group(1)
    check_date(date_text, "Neuwied")
    table = next(x for x in content.findAll("table") if "Positivfälle" in x.get_text())
    rows = [[x.text.strip() for x in row.findAll("td")] for row in table.findAll("tr")]
    #print(*rows, sep="\n")
    c,g,d,a,cc = list(map(force_int, rows[-1][1:6]))
    update(sheets, 7138, c=c, cc=cc, g=g, d=d, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(15, 11, 17, 11, 360, neuwied, 7138))
if __name__ == '__main__': neuwied(googlesheets())

