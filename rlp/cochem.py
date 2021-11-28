#!/usr/bin/python3
## Tommy

from botbase import *

_cochem_c = re.compile(r"([0-9.]+) Corona-Fälle")
_cochem_g = re.compile(r"([0-9.]+) als genesen")
_cochem_d = re.compile(r"([0-9.]+) Corona-Todesfälle zu beklagen")
_cochem_st = re.compile(r"(\d\d?\.\d\d?\.20\d\d)")

def cochem(sheets):

    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.cochem-zell.de/kv_cochem_zell/Unsere%20Themen/Gesundheitsamt/Coronafallzahlen%20im%20Landkreis%20Cochem-Zell/")

    maincontent = soup.find(id="maincontent")
    lines = set([p.get_text(" ").strip() for p in maincontent.findAll("p")])
    for line in lines:
        if "Stand:" in line:
            date = _cochem_st.search(line).group(1)
            date = check_date(date, "Cochem")
            break

    teaser = soup.find(id="teaser")
    lines = set([p.get_text(" ").strip() for p in teaser.findAll("blockquote")])
    args = dict()
    for line in lines:
        c_groups = _cochem_c.search(line)
        if c_groups: args["c"] = force_int(c_groups.group(1))
        g_groups = _cochem_g.search(line)
        if g_groups: args["g"] = force_int(g_groups.group(1))
        d_groups = _cochem_d.search(line)
        if d_groups: args["d"] = force_int(d_groups.group(1))

    #print(args)
    update(sheets, 7135, **args, sig="Bot")
    return True

schedule.append(Task(15, 30, 17, 30, 360, cochem, 7135))
if __name__ == '__main__': cochem(googlesheets())