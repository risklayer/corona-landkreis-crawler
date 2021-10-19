#!/usr/bin/python3
from botbase import *

_weimarerland_c = re.compile(r"([0-9.]+) (?:\(\+?\s*(-? *[0-9.]+)\)\s*)?Fälle bisher")
_weimarerland_d = re.compile(r"([0-9.]+) (?:\(\+?\s*(-? *[0-9.]+)\)\s*)?Verstorbene")
_weimarerland_g = re.compile(r"([0-9.]+) (?:\(\+?\s*(-? *[0-9.]+)\)\s*)?genesen")
_weimarerland_s = re.compile(r"([0-9.]+) (?:\(\+?\s*(-? *[0-9.]+)\)\s*)?Personen in station")
_weimarerland_q1 = re.compile(r"([0-9.]+) (?:\([-+0-9 ]*\))?\s*Kontaktpersonen")
_weimarerland_q2 = re.compile(r"([0-9.]+) (?:\([-+0-9 ]*\))?\s*Reiserück")

def weimarerland(sheets):
    soup = get_soup("https://weimarerland.de/de/aktuelle-informationen-zum-coronavirus/aktuelle-informationen-zum-coronavirus.html")
    article = soup.find(class_="weimar-article-content")
    text = article.get_text()
    #print(text)
    if not today().strftime("Stand: %d.%m.%Y") in text: raise NotYetAvailableException("Weimarer Land noch alt");
    c, cc = map(force_int, _weimarerland_c.search(text).groups())
    d, dd = map(force_int, _weimarerland_d.search(text).groups())
    g, gg = map(force_int, _weimarerland_g.search(text).groups())
    s = force_int(_weimarerland_s.search(text).group(1))
    q1 = force_int(_weimarerland_q1.search(text).group(1))
    q2 = force_int(_weimarerland_q2.search(text).group(1))
    q = c - g - d + q1 + q2
    update(sheets, 16071, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, q=q, s=s, sig="Bot")
    return True

schedule.append(Task(10, 00, 13, 35, 360, weimarerland, 16071))
if __name__ == '__main__': weimarerland(googlesheets())
