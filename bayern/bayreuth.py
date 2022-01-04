#!/usr/bin/python3
from botbase import *

_bayreuth_c = re.compile(r"insgesamt im Landkreis ([0-9.]+) und in der Stadt Bayreuth ([0-9.]+) Personen")
_bayreuth_cc = re.compile(r"eingegangen, (\S+) aus dem Landkreis und (\S+) aus de[rm] Stadt")
_bayreuth_d = re.compile(r"Landkreis sind bisher ([0-9.]+) *und aus der Stadt Bayreuth ([0-9.]+) Personen an den Folgen")
_bayreuth_g = re.compile(r"genesen gelten ([0-9.]+) Personen aus dem Landkreis und ([0-9.]+) aus der Stadt")

def bayreuth(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    from urllib.parse import urljoin
    soup = get_soup("https://www.landkreis-bayreuth.de/der-landkreis/pressemitteilungen/")
    art = next(x for x in soup.find("section").findAll("article") if "Corona-Lage" in x.get_text() or "Stadt und Landkreis" in x.get_text())
    date = check_date(art.find("strong").get_text(), "Bayreuth")
    url = urljoin("https://www.landkreis-bayreuth.de/der-landkreis/pressemitteilungen/", art.find("a")["href"])
    print("Getting", url)
    soup = get_soup(url)
    text = soup.find("section").get_text(" ").strip()
    #print(text)
    cl, cs = map(force_int, _bayreuth_c.search(text).groups())
    ccl, ccs = map(force_int, _bayreuth_cc.search(text).groups()) if _bayreuth_cc.search(text) else None, None
    dl, ds = map(force_int, _bayreuth_d.search(text).groups())
    gl, gs = map(force_int, _bayreuth_g.search(text).groups())
    gl, gs, dl, ds = gl - 2, gs - 3, dl + 2, ds + 3
    update(sheets, 9462, c=cs, cc=ccs, d=ds, g=gs, comment="Bot offset", ignore_delta=True) # Stadt
    update(sheets, 9472, c=cl, cc=ccl, d=dl, g=gl, comment="Bot offset", ignore_delta=True) # LK
    return True

schedule.append(Task(9, 2, 12, 35, 600, bayreuth, 9472))
if __name__ == '__main__': bayreuth(googlesheets())
