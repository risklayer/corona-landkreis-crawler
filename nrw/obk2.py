#!/usr/bin/python3
from botbase import *

_obk2_c = re.compile(r"Positiv\sgetestete\sPersonen\s\(PCR-Test\)\sseit\sPandemiebeginn\**:\s*([0-9.]+)\s*\(=?\+?(-?[0-9.]*)\)", re.U)
_obk2_d = re.compile(r"verstorben:\s([0-9.]+)\s*\(=?\+?(-?[0-9.]*)\)", re.U)
_obk2_g = re.compile(r"aus\sQuarantäne\sentlassen:\s([0-9.]+)\s*\(=?\+?(-?[0-9.]*)\)", re.U)
_obk2_s = re.compile(r"in\sKrankenhäusern\**:\s([0-9.]+)\s*\(=?\+?-?[0-9.]*\)", re.U)
_obk2_ni = re.compile(r"auf\sNormalstation\**:\s([0-9.]+)\s*\(=?\+?-?[0-9.]*\)", re.U)
_obk2_q = re.compile(r"in\sangeordneter\sQuarantäne\**:\s([0-9.]+)\s*\(=?\+?-?[0-9.]*\)", re.U)

def obk2(sheets):
    soup = get_soup("https://www.obk.de/cms200/aktuelles/pressemitteilungen/")
    li = next(x for x in soup.find(id="col3").findAll("li") if "weitere Fälle" in x.get_text() or "neue Fälle" in x.get_text())
    check_date(li.get_text().split(":")[0], "Oberbergischer Kreis")
    link = li.find("a")["href"] if li else None
    from urllib.parse import urljoin
    link = urljoin("https://www.obk.de/cms200/aktuelles/pressemitteilungen/", link)
    print("Getting", link)
    soup = get_soup(link)
    text = soup.find(id="col3").get_text()
    #print(text)
    c, cc = map(force_int, _obk2_c.search(text).groups())
    d, dd = map(force_int, _obk2_d.search(text).groups())
    g, gg = map(force_int, _obk2_g.search(text).groups())
    s = force_int(_obk2_s.search(text).group(1))
    i = s - force_int(_obk2_ni.search(text).group(1))
    q = force_int(_obk2_q.search(text).group(1))
    update(sheets, 5374, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, q=q, s=s, i=i, ignore_delta="mon")
    return True

schedule.append(Task(9, 12, 13, 35, 600, obk2, 5374))
if __name__ == '__main__': obk2(googlesheets())
