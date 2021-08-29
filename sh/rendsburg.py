#!/usr/bin/python3
from botbase import *

_rend_date = re.compile(r"""lastUpdate *= *['"]([0-9.]+ *[0-9:]*)""")
_rend_infect = re.compile(r"""todaySumInfected *= *['"]?([0-9.]+)['";]""")
#_rend_active = re.compile(r"""todayActivInfected *= *['"]?([0-9.]+)['";]""")
_rend_gesund = re.compile(r"""todayHealth *= *['"]?([0-9.]+)['";]""")
_rend_tot = re.compile(r"""todayDeath *= *['"]?([0-9.]+)['";]""")

def rendsburg(sheets):
    data = get_raw("https://covid19dashboardrdeck.aco/daten/update.js").decode("utf-8")
    date = check_date(_rend_date.search(data).group(1), "Rendsburg")
    data = get_raw("https://covid19dashboardrdeck.aco/daten/dash.js").decode("utf-8")
    c = int(_rend_infect.search(data).group(1))
    d = int(_rend_tot.search(data).group(1))
    g = int(_rend_gesund.search(data).group(1))
    sig, comment = "Bot", "Bot"
    if date.hour < 20: sig, comment = "Vorläufig", "Zwischenstand"
    update(sheets, 1058, c=c, g=g, d=d, sig=sig, comment=comment, date=date, check=lambda x: x == None or x == "" or x == "Vorläufig")
    return date.hour >= 20

schedule.append(Hourly(10, 5, 21, 30, 3600, rendsburg, 1058))
if __name__ == '__main__': rendsburg(googlesheets())
