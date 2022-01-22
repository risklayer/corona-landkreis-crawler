#!/usr/bin/python3
## Tommy
from botbase import *

_gifhorn_date = re.compile(r"Aktueller Stand: (\d\d?\.\d\d?\.20\d\d)")
_gifhorn_c = re.compile(r"Anzahl der positiv getesteten Personen:\s([0-9.]+) \(\+\/?\-? ([0-9]+)")
_gifhorn_d = re.compile(r"Todesfälle:\s+([0-9.]+)\s*\(\+?\/?\-?\s([0-9]+)")

def gifhorn(sheets):
    soup = get_soup("https://www.gifhorn.de/der-landkreis/oeffentlichkeitsarbeit/corona/presseinformationen/")
    entry = next(x for x in soup.find_all("a") if "Aktueller Stand:" in x.get_text())
    date = _gifhorn_date.search(entry.get_text()).group(1)
    check_date(date, "Gifhorn")

    link = entry["href"] if entry else None
    from urllib.parse import urljoin
    link = urljoin("https://www.gifhorn.de/der-landkreis/oeffentlichkeitsarbeit/corona/presseinformationen/", link)
    print("Getting", link)

    content = get_soup(link).get_text()
    c = force_int(_gifhorn_c.search(content).group(1))
    cc = force_int(_gifhorn_c.search(content).group(2))
    d = force_int(_gifhorn_d.search(content).group(1))
    dd = force_int(_gifhorn_d.search(content).group(2))

    update(sheets, 3151, c=c, cc=cc, d=d, dd=dd, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(15, 50, 17, 50, 360, gifhorn, 3151))
if __name__ == '__main__': gifhorn(googlesheets())
