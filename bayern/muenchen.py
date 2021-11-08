
#!/usr/bin/python3
from botbase import *

_muenchen_c = re.compile(r"([0-9.]+) Infektionen bestätigt")
_muenchen_cc = re.compile(r"(-?[0-9.]+) neue Corona-Fälle")
_muenchen_d = re.compile(r"insgesamt ([0-9.]+) Todesfälle")
_muenchen_g = re.compile(r"enthalten sind ([0-9.]+)")
_muenchen_s = re.compile(r"([0-9.]+) Betten")
_muenchen_i = re.compile(r"([0-9.]+) Intensivbetten")

def muenchen(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.muenchen.de/rathaus/Stadtinfos/Coronavirus-Fallzahlen.html")
    main = soup.find(id="content")
    ps = [p.get_text(" ") for p in main.findAll("p")]
    #for p in ps: print(p)
    h2 = [x for x in ps if "Update" in x][0]
    if not today().strftime("%-d.%-m") in h2: raise NotYetAvailableException("München noch alt: " + h2)
    datestr = "wurden für " + (today() - datetime.timedelta(1)).strftime("%A, %-d. %B")
    if not any(datestr in p for p in ps): raise NotYetAvailableException("München noch alt, erwarte: "+datestr)
    args=dict()
    for p in ps:
        m = _muenchen_c.search(p)
        if m: args["c"] = force_int(m.group(1))
        m = _muenchen_cc.search(p)
        if m: args["cc"] = force_int(m.group(1))
        m = _muenchen_d.search(p)
        if m: args["d"] = force_int(m.group(1))
        m = _muenchen_g.search(p)
        if m: args["g"] = force_int(m.group(1))
        m = _muenchen_s.search(p)
        if m: args["s"] = force_int(m.group(1))
        m = _muenchen_i.search(p)
        if m: args["i"] = force_int(m.group(1))
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    update(sheets, 9162, **args, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(13, 32, 16, 35, 360, muenchen, 9162))
if __name__ == '__main__': muenchen(googlesheets())
