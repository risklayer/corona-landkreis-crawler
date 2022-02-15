#!/usr/bin/python3
## Tommy
from botbase import *

_ostholstein_date = re.compile(r"Corona-Virus aktuell\s*Stand:\s*(\d\d?\.\d\d?\.20\d\d)")
_ostholstein_c = re.compile(r"(?:bestätigten|gemeldeten) Infektionsfälle in Ostholstein beträgt\s*([0-9.]+)")
_ostholstein_a = re.compile(r"Aktuell positive Fälle:\s*([0-9.]+)")
_ostholstein_g = re.compile(r"Als genesen gelten:\s*([0-9.]+)")
_ostholstein_s = re.compile(r"Aktuell klinisch in Behandlung:\s*([0-9.]+)")
_ostholstein_d = re.compile(r"Verstorben:\s*([0-9.]+)")
_ostholstein_q = re.compile(r"Aktuell in Quarantäne:\s*([0-9.]+)")

def ostholstein(sheets):
    soup = get_soup("https://www.kreis-oh.de/Service-Navigation/Start/Corona-Virus-aktuell.php?object=tx%2C2454.18444&ModID=7&FID=2454.18562.1&NavID=2454.255")
    content = soup.get_text()
    #print(content)
    date_text = _ostholstein_date.search(content).group(1)
    check_date(date_text, "Ostholstein")
    c = force_int(_ostholstein_c.search(content).group(1))
    d = force_int(_ostholstein_d.search(content).group(1))
    g = force_int(_ostholstein_g.search(content).group(1))
    q, s = None, None
    if _ostholstein_q.search(content):
        q = force_int(_ostholstein_q.search(content).group(1)) + force_int(_ostholstein_a.search(content).group(1))
    if _ostholstein_s.search(content):
        s = force_int(_ostholstein_s.search(content).group(1))
    update(sheets, 1055, c=c, d=d, g=g, q=q, s=s, sig="", comment="Später Land. Bot", ignore_delta="mon")
    return True

schedule.append(Task(15, 27, 17, 27, 360, ostholstein, 1055))
if __name__ == '__main__': ostholstein(googlesheets())
