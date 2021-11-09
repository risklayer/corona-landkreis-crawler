#!/usr/bin/python3
from botbase import *

# Beware: this site uses plenty of non-breaking spaces
_neunkirchen_cc = re.compile(r"gibt\ses\s([0-9.]+|\w+)\sweitere", re.U)
_neunkirchen_c = re.compile(r"insgesamt\salso\s(?:weiter\s)?([0-9.]+)\spositive", re.U)
_neunkirchen_d = re.compile(r"\s([0-9.]+)\sCovid-19-Todesfälle", re.U)
_neunkirchen_g = re.compile(r"können\s([0-9.]+)\s*Personen\s[^\s]*\s*als\sgeheilt", re.U)
_neunkirchen_gg = re.compile(r"können\s[0-9.]+\s*Personen\s\(([+-]*[0-9]+)\)\sals\sgeheilt", re.U)

def neunkirchen(sheets):
    soup = get_soup("https://www.landkreis-neunkirchen.de/index.php?id=3554")
    ps, todaystr = None, today().strftime("%d.%m.%Y")
    for b in soup.find(id="ContentText").findAll(class_="csc-default")[:50]:
        ps = ["".join([x for x in p.findAll(text=True)]).strip() for p in b.findAll("p")]
        ps = [p for p in ps if p != ""]
        if todaystr in " ".join(ps): break
        ps = None
    #for p in ps: print(p)
    if ps is None: raise NotYetAvailableException("Neunkirchen noch alt.")
    args={}
    for p in ps:
        m = _neunkirchen_c.search(p)
        if m: args["c"] = force_int(m.group(1))
        m = _neunkirchen_cc.search(p)
        if m: args["cc"] = force_int(m.group(1))
        m = _neunkirchen_d.search(p)
        if m: args["d"] = force_int(m.group(1))
        m = _neunkirchen_g.search(p)
        if m: args["g"] = force_int(m.group(1))
        m = _neunkirchen_gg.search(p)
        if m: args["gg"] = force_int(m.group(1))
    #print(args)
    assert "c" in args and "d" in args and "g" in args, str(args)
    update(sheets, 10043, **args, sig="Bot", ignore_delta=False)
    return True

schedule.append(Task(16, 30, 23, 55, 900, neunkirchen, 10043))
if __name__ == '__main__': neunkirchen(googlesheets())
