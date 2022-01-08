#!/usr/bin/python3
from botbase import *

_schleswigf_cc = re.compile(r"Neu gemeldete Fälle: *([0-9.]+)")
_schleswigf_c = re.compile(r"Gesamtzahl gemeldete Fälle: *([0-9.]+)")
_schleswigf_g = re.compile(r"Genesen: *([0-9.]+)")
_schleswigf_d = re.compile(r"Verstorben: *([0-9.]+)")
_schleswigf_q = re.compile(r"Quarantäne: *([0-9.]+)")

def schleswigf(sheets):
    soup = get_soup("https://www.schleswig-flensburg.de/Aktuelle-Zahlen/")
    text = soup.find(id="readthis").get_text(" ").strip()
    #print(text)
    if not today().strftime("Schleswig-Flensburg (%d.%m.%Y)") in text: raise NotYetAvailableException("Schleswig-Flensburg noch alt: " + re.split(r"\s*\n[\s\n]*", text)[1])
    c = force_int(_schleswigf_c.search(text).group(1))
    cc = force_int(_schleswigf_cc.search(text).group(1))
    g = force_int(_schleswigf_g.search(text).group(1))
    d = force_int(_schleswigf_d.search(text).group(1))
    q = force_int(_schleswigf_q.search(text).group(1)) if _schleswigf_q.search(text) else None
    update(sheets, 1059, c=c, cc=cc, d=d, g=g, q=q, ignore_delta=True)
    return True

schedule.append(Task(11, 55, 14, 35, 600, schleswigf, 1059))
if __name__ == '__main__': schleswigf(googlesheets())
