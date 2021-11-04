#!/usr/bin/python3
from botbase import *

_peine_cc = re.compile(r"(\d+) neue Fälle")
_peine_c = re.compile(r"([0-9.]+) bestätigte Corona-Fälle")
_peine_a = re.compile(r"([0-9.]+) Personen sind derzeit erkrankt")
_peine_q = re.compile(r"([0-9.]+) Personen befinden sich in Quarantäne")
_peine_d = re.compile(r"([0-9.]+) Todesfälle im Zusammenhang")
_peine_st = re.compile(r"Stand: (\d\d\.\d\d.20\d\d)")

def peine(sheets):
    soup = get_soup("https://www.landkreis-peine.de/Aktuelles-B%C3%BCrgerservice/Informationen-zu-Coronaviren")
    articles = soup.find(id="readid")
    text = articles.get_text(" ").strip()
    #print(text)
    date = check_date(_peine_st.search(text).group(1), "Peine")
    c = force_int(_peine_c.search(text).group(1))
    cc = force_int(_peine_cc.search(text).group(1))
    a = force_int(_peine_a.search(text).group(1))
    d = force_int(_peine_d.search(text).group(1))
    q = force_int(_peine_q.search(text).group(1)) + a
    g = c - d - a
    update(sheets, 3157, c=c, cc=cc, d=d, g=g, q=q, sig="Bot")
    return True

schedule.append(Task(16, 30, 19, 35, 360, peine, 3157))
if __name__ == '__main__': peine(googlesheets())
