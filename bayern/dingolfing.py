#!/usr/bin/python3
from botbase import *

_dingolfing_c = re.compile(r"([0-9.]+)\spositiv\sgetestete")
_dingolfing_d = re.compile(r"([0-9.]+)\sTodesfälle")
_dingolfing_g = re.compile(r"([0-9.]+)\saus\sQuarantäne")

def dingolfing(sheets):
    soup = get_soup("https://www.landkreis-dingolfing-landau.de/buergerservice/coronavirus/")
    main = soup.find("main").find("section")
    p = main.find("li").parent
    pt = p.find_previous_sibling("p").get_text()
    t = p.get_text(" ")
    #print(t)
    if not today().strftime("%d.%m.%Y") in pt: raise NotYetAvailableException("Dingolfing noch alt:" + pt)
    c = force_int(_dingolfing_c.search(t).group(1))
    d = force_int(_dingolfing_d.search(t).group(1))
    g = force_int(_dingolfing_g.search(t).group(1))
    update(sheets, 9279, c=c, d=d, g=g, sig="Bot")
    return True

schedule.append(Task(9, 4, 11, 35, 600, dingolfing, 9279))
if __name__ == '__main__': dingolfing(googlesheets())
