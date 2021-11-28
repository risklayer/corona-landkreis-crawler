#!/usr/bin/python3
from botbase import *

_merzig_cc = re.compile(r"([0-9.]+|\w+) neue Covid")
_merzig_c = re.compile(r"infiziert wurden, liegt bei ([0-9.]+)\.")
_merzig_d = re.compile(r"([0-9.]+) Todesfälle")
_merzig_d2 = re.compile(r"Todesfälle [\w\s-]+ auf ([0-9.]+) gestiegen", re.U)
_merzig_g = re.compile(r"genesen gelten, liegt bei ([0-9.]+)\.")

def merzigwadern(sheets):
    soup = get_soup("https://www.merzig-wadern.de/Kurzmen%C3%BC/Startseite/-Newsticker-zum-Coronavirus-.php?object=tx,2875.5&ModID=7&FID=2875.1724.1&NavID=1918.1")
    content = soup.find(id="readthis").find("article")
    ps = [p for p in content.find_all(text=True) if not p.strip() == ""]
    # TODO: iterate, instead of relying that its always the third?
    ps = ps[ps.index("---")+1:]
    ps = ps[ps.index("---")+1:]
    ps = ps[:ps.index("---")]
    #for p in ps: print(p)
    if not today().strftime("%d.%m.%Y") in ps: raise NotYetAvailableException("Merzig-Wadern noch alt: "+ps[0])
    args={}
    for p in ps:
        m = _merzig_c.search(p)
        if m: args["c"] = force_int(m.group(1))
        m = _merzig_cc.search(p)
        if m: args["cc"] = force_int(m.group(1))
        m = _merzig_d.search(p)
        if m: args["d"] = force_int(m.group(1))
        m = _merzig_d2.search(p)
        if m: args["d"] = force_int(m.group(1))
        m = _merzig_g.search(p)
        if m: args["g"] = force_int(m.group(1))
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    update(sheets, 10042, **args, sig="Bot", ignore_delta=False)
    return True

schedule.append(Task(14, 30, 20, 35, 600, merzigwadern, 10042))
if __name__ == '__main__': merzigwadern(googlesheets())
