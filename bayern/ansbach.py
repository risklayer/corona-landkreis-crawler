#!/usr/bin/python3
from botbase import *

_ansbachl_c = re.compile(r"Infektionsfälle Landkreis Ansbach:\s*([0-9.]+)\s*\(\s*\+?\s*(-?[0-9.]+)?", re.U)
_ansbachs_c = re.compile(r"Infektionsfälle Stadt Ansbach:\s*([0-9.]+)\s*\(\s*\+?\s*(-?[0-9.]+)?", re.U)
_ansbachl_g = re.compile(r"Genesene Landkreis Ansbach:\s*([0-9.]+)", re.U)
_ansbachs_g = re.compile(r"Genesene Stadt Ansbach:\s*([0-9.]+)", re.U)
_ansbachl_d = re.compile(r"Verstorbene Landkreis Ansbach:\s*([0-9.]+)", re.U)
_ansbachs_d = re.compile(r"Verstorbene Stadt Ansbach:\s*([0-9.]+)", re.U)

def ansbach(sheets):
    soup = get_soup("https://www.landkreis-ansbach.de/Corona")
    main = soup.find(class_="content")
    ps = [p.get_text(" ") for p in main.findAll("p")]
    #for p in ps: print(p)
    h2 = [x for x in ps if x.startswith("Stand:")][-1].split(":")[1].strip()
    date = check_date(h2.split(" ")[0], "Ansbach")
    #if not today().strftime("%-d.%-m") in h2: raise NotYetAvailableException("Ansbach noch alt: " + h2)
    #datestr = "wurden für " + (today() - datetime.timedelta(1)).strftime("%A, %-d. %B")
    #if not any(datestr in p for p in ps): raise NotYetAvailableException("Ansbach noch alt, erwarte: "+datestr)
    argsl, argss=dict(), dict()
    for p in ps:
        m = _ansbachl_c.search(p)
        if m: argsl["c"], argsl["cc"] = force_int(m.group(1)), force_int(m.group(2), 0)
        m = _ansbachl_d.search(p)
        if m: argsl["d"] = force_int(m.group(1))
        m = _ansbachl_g.search(p)
        if m: argsl["g"] = force_int(m.group(1))
        m = _ansbachs_c.search(p)
        if m: argss["c"], argss["cc"] = force_int(m.group(1)), force_int(m.group(2), 0)
        m = _ansbachs_d.search(p)
        if m: argss["d"] = force_int(m.group(1))
        m = _ansbachs_g.search(p)
        if m: argss["g"] = force_int(m.group(1))
    #print(argss, argsl)
    assert "c" in argsl and "d" in argsl and "g" in argsl
    assert "c" in argss and "d" in argss and "g" in argss
    update(sheets, 9561, **argss, sig="Bot")
    update(sheets, 9571, **argsl, sig="Bot")
    return True

schedule.append(Task(12, 33, 14, 35, 360, ansbach, 9571))
if __name__ == '__main__': ansbach(googlesheets())
