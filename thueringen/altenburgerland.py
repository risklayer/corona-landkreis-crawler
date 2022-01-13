#!/usr/bin/python3
## Tommy
from botbase import *

_altenburgerland_c = re.compile(r"Bisher haben sich insgesamt ([0-9.]+)")
_altenburgerland_d = re.compile(r"Zahl der Verstorbenen: ([0-9.]+)")
_altenburgerland_s = re.compile(r"Im Klinikum (?:müssen|muss) (?:aktuell )?([0-9.]+|\w+)")
_altenburgerland_i = re.compile(r"([0-9.]+|\w+) davon auf der Intensivstation")
_altenburgerland_cc = re.compile(r"([0-9.]+|\w+) (?:Infizierter? mehr |Neuinfektion)")
_altenburgerland_st = re.compile(r"Stand: (\d\d?\.\d\d?\.20\d\d)")

def altenburgerland(sheets):
    soup = get_soup("https://www.altenburgerland.de/sixcms/detail.php?&_nav_id1=2508&_lang=de&id=371691")
    temp = soup.find_all("div", {"class": "text_bild_kombi"})

    content = False
    for t in temp:
        if "Bisher haben sich insgesamt" in t.text:
            content = t.text.strip()
            break
    assert content

    date = _altenburgerland_st.search(content).group(1)
    check_date(date, "Altenburgerland")
    #print(content)

    c = force_int(_altenburgerland_c.search(content).group(1))
    cc = force_int(_altenburgerland_cc.search(content).group(1))
    d = force_int(_altenburgerland_d.search(content).group(1))
    s = force_int(_altenburgerland_s.search(content).group(1))
    i = force_int(_altenburgerland_i.search(content).group(1))

    update(sheets, 16077, c=c, cc=cc, d=d, s=s, i=i, sig="Bot", comment="Bot ohne G", ignore_delta="mon")
    return True

schedule.append(Task(15, 2, 16, 40, 360, altenburgerland, 16077))
if __name__ == '__main__': altenburgerland(googlesheets())
