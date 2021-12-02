#!/usr/bin/python3
from botbase import *

_stwendel_cc = re.compile(r"wurden ([0-9.]+|\w+) Covid-19")
_stwendel_d = re.compile(r"Zusammenhang mit Covid-19: ([0-9.]+)")
_stwendel_g = re.compile(r"genesen gelten ([0-9.]+)")

def stwendel(sheets):
    soup = get_soup("https://www.landkreis-st-wendel.de/leben-soziales-gesundheit/gesundheitsamt/informationen-zum-coronavirus")
    content = soup.find("main").find("article")
    ps = [p for p in content.find(id="c3085").find_all(text=True) if not p.strip() == ""]
    # for p in ps: print(p)
    date = check_date(ps[1].replace("(","").replace(" Uhr)",":00"), "St. Wendel")
    #if not today().strftime("-%d.%m.") in ps[1]: raise NotYetAvailableException("St. Wendel noch alt: "+ps[1])
    args={}
    args["c"] = force_int(content.find(id="c3083").find("tfoot").findAll("td")[-1].text)
    for p in ps:
        m = _stwendel_cc.search(p)
        if m: args["cc"] = force_int(m.group(1))
        m = _stwendel_d.search(p)
        if m: args["d"] = force_int(m.group(1))
        m = _stwendel_g.search(p)
        if m: args["g"] = force_int(m.group(1))
    # print(args)
    assert "c" in args and "d" in args and "g" in args
    update(sheets, 10046, **args, sig="Bot", date=date, ignore_delta=True)
    return True

schedule.append(Task(15, 6, 20, 35, 360, stwendel, 10046))
if __name__ == '__main__': stwendel(googlesheets())
