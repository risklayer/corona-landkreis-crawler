#!/usr/bin/python3
from botbase import *

_sha_c = re.compile(r"insgesamt\s+([0-9.]+)\s+bestätigte")
_sha_d = re.compile(r"([0-9.]+)\*?\s+Corona-Erkrankte[^\d]+Covid-19 verstorben")
_sha_g = re.compile(r"([0-9.]+)\s+Corona-Erkrankte[^\d]+wieder gesundet")
_sha_q = re.compile(r"in Quarantäne:\s+([0-9.]+)")
_sha_si = re.compile(r"([0-9.]+|\w+) (?:positiver? )?(?:Covid-19-)?(?:F[aä]lle?|Patiente?n?) (?:sowie \w*\d* Verdachts\w* )?auf Station [^.]+ ([0-9.]+|\w+) (?:positiver? )?(?:F[aä]lle?|Patiente?n?) auf der Intensiv")
_sha_si2 = re.compile(r"([0-9.]+|\w+) (?:positiver? )?(?:Covid-19-)?(?:F[aä]lle?|Patiente?n?) (?:sowie \w*\d* Verdachts\w* )?auf Station. Auf der Intensivstation sind ([0-9.]+|\w+) (?:positiver? )?(?:F[aä]lle?|Patiente?n?)")
_sha_st = re.compile(r"Stand: (?:\w+,) (\d\d?\.\d\d?\.20\d\d, \d\d?:\d\d)")

def sha(sheets):
    soup = get_soup("https://www.lrasha.de/index.php?id=953&publish%5Bid%5D=1212280&publish%5Bstart%5D=")
    main = soup.find(id="contentbereich").find(class_="publishnews")
    text = main.get_text(" ").strip()
    date = _sha_st.search(text).group(1)
    date = check_date(date, "Schwäbisch-Hall")
    #print(text)
    #if not today().strftime(" %d.%m.%Y") in text: raise NotYetAvailableException("Schwäbischhall noch alt:" + text.split("\n")[0])
    c = force_int(_sha_c.search(text).group(1))
    d = force_int(_sha_d.search(text).group(1))
    g = force_int(_sha_g.search(text).group(1))
    m = _sha_q.search(text)
    q = force_int(m.group(1)) + c - d - g if m else None
    s, i = 0, 0
    for m in _sha_si.findall(text):
        s += force_int(m[0])
        s += force_int(m[1], 0)
        i += force_int(m[1], 0)
    for m in _sha_si2.findall(text):
        s += force_int(m[0])
        s += force_int(m[1], 0)
        i += force_int(m[1], 0)
    if not s and not i: s, i = None, None
    comment = "Bot SI unzuverlässig!" if s else "Bot"
    update(sheets, 8127, c=c, d=d, g=g, q=q, s=s, i=i, sig="Bot", comment=comment, date=date)
    return True

schedule.append(Task(16, 30, 20, 35, 600, sha, 8127))
if __name__ == '__main__': sha(googlesheets())
