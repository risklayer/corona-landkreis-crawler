#!/usr/bin/python3
from botbase import *

_saarpfalz_c = re.compile(r"infizierten? Personen: *([0-9.]+)")
_saarpfalz_cc = re.compile(r"Neuinfektionen: *([0-9.]+)")
_saarpfalz_a = re.compile(r"infiziert: *([0-9.]+)")
_saarpfalz_g = re.compile(r"Genesene: *([0-9.]+)")

def saarpfalz(sheets):
    soup = get_soup("https://www.saarpfalz-kreis.de/leben-soziales-gesundheit/gesundheit/coronavirus")
    content = soup.find(id="Item.MessagePartBody")
    ps = [x.get_text(" ") for x in content.findAll("p")]
    #for p in ps: print(p)
    stand = [p for p in ps if "Stand:" in p][0]
    #print(stand, today().strftime("%-d. %B"))
    if not today().strftime("%-d. %B") in stand: raise NotYetAvailableException("Saarpfalz noch alt: "+stand)
    args={}
    for p in ps:
        m = _saarpfalz_c.search(p)
        if m: args["c"] = force_int(m.group(1))
        m = _saarpfalz_a.search(p)
        if m: args["a"] = force_int(m.group(1))
        m = _saarpfalz_cc.search(p)
        if m: args["cc"] = force_int(m.group(1))
        m = _saarpfalz_g.search(p)
        if m: args["g"] = force_int(m.group(1))
    if "a" in args and "c" in args and "g" in args:
        args["d"] = args["c"] - args["g"] - args["a"]
        del args["a"]
    #print(args)
    assert "c" in args and "d" in args and "g" in args
    update(sheets, 10045, **args, sig="Bot", ignore_delta=False)
    return True

schedule.append(Task(14, 30, 17, 35, 600, saarpfalz, 10045))
if __name__ == '__main__': saarpfalz(googlesheets())
