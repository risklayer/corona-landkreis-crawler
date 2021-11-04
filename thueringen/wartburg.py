#!/usr/bin/python3
from botbase import *

_wartburg_st = re.compile(r"Stand (\d\d\.\d\d.20\d\d), (\d\d)[.:](\d\d) Uhr")
_wartburg_c = re.compile(r"Wartburgkreis mit Eisenach eingegliedert:?\s*([0-9.]+)")
_wartburg_d = re.compile(r"Todesfälle seit Beginn der Pandemie\**:\s*([0-9.]+)")
_wartburg_a = re.compile(r"aktive Infektionen im Wartburgkreis\**:\s*([0-9.]+)")

def wartburg(sheets):
    soup = get_soup("https://www.wartburgkreis.de/leben-im-wartburgkreis/gesundheit/aktuelle-informationen-zum-corona-virus/fallzahlen")
    article = soup.find("article")
    text = article.find(class_="ce-bodytext").get_text(" ").strip()
    #print(text)
    m = _wartburg_st.search(text)
    date = m.group(1)+" "+m.group(2)+":"+m.group(3)
    date = check_date(date, "Wartburg")
    c = force_int(_wartburg_c.search(text).group(1))
    d = force_int(_wartburg_d.search(text).group(1))
    a = force_int(_wartburg_a.search(text).group(1))
    g = c - d - a
    update(sheets, 16063, c=c, d=d, g=g, date=date, sig="Bot")
    return True

schedule.append(Task(9, 30, 13, 35, 360, wartburg, 16063))
if __name__ == '__main__': wartburg(googlesheets())
