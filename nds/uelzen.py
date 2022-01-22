#!/usr/bin/python3
from botbase import *

_uelzen_c = re.compile(r"insgesamt bestätigten Fälle nunmehr bei ([0-9.]+)")
_uelzen_d = re.compile(r"([0-9.]+) verstorben")
_uelzen_g = re.compile(r"([0-9.]+) Menschen, bei denen das Virus bisher nachgewiesen wurde, sind wieder genesen")
_uelzen_s = re.compile(r"([0-9.]+|\w+) Personen mit oder wegen COVID-19")
_uelzen_q = re.compile(r"In häuslicher Quarantäne befinden sich ([0-9.]+) Personen")

def uelzen(sheets):
    soup = get_soup("https://www.landkreis-uelzen.de/home/soziales-familie-und-gesundheit/gesundheit/covid-19-pandemie/corona-update.aspx")
    main = next(x for x in soup.find(id="ctl01_contentpane").findAll(class_="row") if "Corona-Update" in x.get_text())
    content = main.get_text(" ").strip()
    #print(content)
    if not today().strftime("%d.%m.%Y") in main.find("u").text: raise NotYetAvailableException("Uelzen noch alt:" + main.find("u").text)
    c = force_int(_uelzen_c.search(content).group(1))
    d = force_int(_uelzen_d.search(content).group(1))
    g = force_int(_uelzen_g.search(content).group(1))
    s = force_int(_uelzen_s.search(content).group(1)) if _uelzen_s.search(content) else None
    q = force_int(_uelzen_q.search(content).group(1))
    update(sheets, 3360, c=c, d=d, g=g, s=s, q=q)
    return True

schedule.append(Task(15, 2, 20, 35, 600, uelzen, 3360))
if __name__ == '__main__': uelzen(googlesheets())
