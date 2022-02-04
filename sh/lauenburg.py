#!/usr/bin/python3
## Tommy
from botbase import *

_lauenburg_date = re.compile(r"SARS-CoV-2-Fälle im Kreis Herzogtum Lauenburg am (\d\d?\.\d\d?\.20\d\d)")
_lauenburg_g = re.compile(r"davon genesen\s*([0-9.]+)")
_lauenburg_d = re.compile(r"verstorben\s*([0-9.]+)")
_lauenburg_dd = re.compile(r"verstorben\s*(?:[0-9.]+)\*?\s*\(\+\s*([0-9.]+)\s*zum Vortag")
_lauenburg_c = re.compile(r"Gesamt:\s*([0-9.]+)")
_lauenburg_cc = re.compile(r"Gesamt:\s*(?:[0-9.]+)\*?\s*\(\+\s*([0-9.]+)\s*zum Vortag")

def lauenburg(sheets):
    soup = get_soup("https://www.kreis-rz.de/index.php")
    link = next(x["href"] for x in soup.find_all("a", {"href": True}) if "Alles zum Thema Corona (SARS-CoV-2" in x.get_text())
    link = urljoin("https://www.kreis-rz.de/index.php", link)
    print("Getting", link)
    content = get_soup(link).get_text()
    date_text = _lauenburg_date.search(content).group(1)
    check_date(date_text, "Lauenburg")
    c = force_int(_lauenburg_c.search(content).group(1))
    cc = force_int(_lauenburg_cc.search(content).group(1)) if _lauenburg_cc.search(content) else None
    d = force_int(_lauenburg_d.search(content).group(1))
    dd = force_int(_lauenburg_dd.search(content).group(1)) if _lauenburg_dd.search(content) else None
    g = force_int(_lauenburg_g.search(content).group(1))
    update(sheets, 1053, c=c, cc=cc, d=d, dd=dd, g=g, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(15, 42, 17, 42, 360, lauenburg, 1053))
if __name__ == '__main__': lauenburg(googlesheets())

