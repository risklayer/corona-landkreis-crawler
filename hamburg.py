#!/usr/bin/python3
from botbase import *

def hamburg(sheets):
    soup = get_soup("https://www.hamburg.de/corona-zahlen")
    lis = soup.find("main").findAll("li")
    ags = 2000
    c, cc, g, d, dd, s, i = None,None,None,None,None,None,None
    for li in lis:
        db = li.find("span", class_="dashboar_number")
        if db:
            if "Bestätigte Fälle" in li.text: c = int(db.text)
            if "Neuinfektionen" in li.text: cc = force_int(db.text)
            if "Davon geheilt" in li.text: g = int(db.text)
            if "Todesfälle" in li.text and not "Neue" in li.text: d = int(db.text)
            if "Neue Todesfälle" in li.text: dd = int(db.text)
            if "Stationär gesamt" in li.text: s = int(db.text)
            if "Intensiv gesamt" in li.text: i = int(db.text)
    stand = soup.find("main").find(class_="chart_publication").text
    if not datetime.date.today().strftime("%d.%m.%Y") in stand: raise NotYetAvailableException("Hamburg noch alt? " + stand)
    update(sheets, ags, c=c, cc=cc, g=g, s=s, i=i, d=d, dd=dd, sig="Bot")
    return True

schedule.append(Task(11, 55, 12, 30, 120, hamburg, 2000))
if __name__ == '__main__': hamburg(googlesheets())
