#!/usr/bin/python3
from botbase import *

_saarlouis_c = re.compile(r"insgesamt: ([0-9.]+)")
_saarlouis_d = re.compile(r"Verstorben: ([0-9.]+)")
_saarlouis_g = re.compile(r"Genesen: ([0-9.]+)")

def saarlouis(sheets):
    import bs4
    soup = get_soup("https://www.kreis-saarlouis.de/Corona-Virus/Corona-Ticker.htm?")
    content = soup.find(id="content_frame")
    ps = []
    cur = next(content.find("hr").parent.children)
    stop = cur.findNext("hr")
    while cur is not None:
        if isinstance(cur, bs4.Tag): ps.extend([p for p in cur.find_all(text=True) if not p.strip() == ""])
        cur = cur.nextSibling
        if cur == stop:
            if len(ps) > 4: break
            stop = cur.findNext("hr")
    #for p in ps: print("A",p)
    #date = check_date(p[0], "Merzig-Wadern")
    if not today().strftime("%d.%m.%Y") in ps[0]: raise NotYetAvailableException("Saarlouis noch alt: "+ps[0])
    args={}
    for p in ps:
        m = _saarlouis_c.search(p)
        if m: args["c"] = force_int(m.group(1))
        m = _saarlouis_d.search(p)
        if m: args["d"] = force_int(m.group(1))
        m = _saarlouis_g.search(p)
        if m: args["g"] = force_int(m.group(1))
    assert "c" in args and "d" in args and "g" in args, "No data - yet?"
    update(sheets, 10044, **args, sig="Bot", ignore_delta=False)
    return True

schedule.append(Task(15, 30, 20, 35, 600, saarlouis, 10044))
if __name__ == '__main__': saarlouis(googlesheets())
