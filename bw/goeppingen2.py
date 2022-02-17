#!/usr/bin/python3
from botbase import *

_goeppingen_st = re.compile(r"Stand: (\d\d?\.\d\d?\.\d\d, \d\d:\d\d)", re.U)
_goeppingen_c = re.compile(r"Fälle insgesamt: *([0-9.]+) \(\+?([-0-9.]+) zu", re.U)
_goeppingen_d = re.compile(r"Todesfälle insgesamt: *([0-9.]+)", re.U)
_goeppingen_a = re.compile(r"Quarantäne: *([0-9.]+)", re.U)

def goeppingen2(sheets):
    soup = get_soup("https://www.landkreis-goeppingen.de/start/_Aktuelles/coronavirus.html")
    content = soup.find(id="main")
    content = next(x for x in content.findAll(class_="toggle_container") if "Aktuelle Zahlen" in x.get_text()).get_text(" ").strip()
    #print(content)
    date = check_date(_goeppingen_st.search(content).group(1), "Göppingen")
    c, cc = map(force_int, _goeppingen_c.search(content).groups())
    d = force_int(_goeppingen_d.search(content).group(1))
    a = force_int(_goeppingen_a.search(content).group(1))
    g = c - d - a
    update(sheets, 8117, c=c, cc=cc, d=d, g=g, date=date, ignore_delta=False)
    return True

schedule.append(Task(14, 17, 16, 30, 600, goeppingen2, 8117))
if __name__ == '__main__': goeppingen2(googlesheets())
