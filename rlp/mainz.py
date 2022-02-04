#!/usr/bin/python3
from botbase import *

_mainz_c = re.compile(r"([0-9.]+) *\(±?([+-]? *[0-9.]+) *zu (?:gestern|Freitag|\w+)\) positiv getestete Personen aus dem Landkreis Mainz-Bingen, *([0-9.]+) *\(±?([+-]? *[0-9.]+) *zu (?:gestern|Freitag|\w+)\) aus der Stadt", re.U)
_mainz_g = re.compile(r"Genesene: [0-9.]+ \(±?[+-]? *[0-9.]+\) *davon Mainz-Bingen: ([0-9.]+) *\(±?([+-]? *[0-9.]+)\) *davon Stadt Mainz: *([0-9.]+) *\(±?([+-]? *[0-9.]+)\)", re.U)
_mainz_d = re.compile(r"Todesfälle im Landkreis Mainz-Bingen *([0-9.]+)(?: *\(±?([+-]? *[0-9.]+)\))? *, *Todesfälle Stadt Mainz *([0-9.]+)(?: *\(±?([+-]? *[0-9.]+)\))?", re.U)

def mainz(sheets):
    soup = get_soup("https://www.mainz-bingen.de/")
    m = next(x for x in soup.findAll(class_="listEntryInner") if "Corona-Virus:" in x.get_text())
    date = check_date(m.find(class_="listEntryDate").get_text(), "Mainz")
    url = urljoin("https://www.mainz-bingen.de/", m.find("a")["href"])
    print("Getting", url)
    soup = get_soup(url)
    text = soup.find(id="blockContentFullRight").get_text(" ").strip()
    #print(text)
    if not today().strftime("%d.%m.%Y") in text: raise NotYetAvailableException("Mainz noch alt:" + ps[0])
    cb, ccb, cm, ccm = map(force_int, _mainz_c.search(text).groups())
    gb, ggb, gm, ggm = map(force_int, _mainz_g.search(text).groups())
    db, ddb, dm, ddm = map(force_int, _mainz_d.search(text).groups())
    update(sheets, 7315, c=cm, cc=ccm, d=dm, dd=ddm, g=gm, gg=ggm, sig="Bot", ignore_delta=True) # Mainz
    update(sheets, 7339, c=cb, cc=ccb, d=db, dd=ddb, g=gb, gg=ggb, sig="Bot", ignore_delta=True) # Mainz-Bingen
    return True

schedule.append(Task(13, 30, 17, 35, 600, mainz, 7339))
if __name__ == '__main__': mainz(googlesheets())
