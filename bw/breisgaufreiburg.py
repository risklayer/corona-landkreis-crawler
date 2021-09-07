#!/usr/bin/python3
from botbase import *

def breisgaufreiburg(sheets):
    soup = get_soup("https://www.breisgau-hochschwarzwald.de/pb/Breisgau-Hochschwarzwald/Start/Service+_+Verwaltung/Corona-Virus.html")
    content = soup.find(id="content")
    rows = content.find("table").findAll("tr")
    rows = [[x.text.strip() for x in row.findAll("td")] for row in rows]
    #print(rows)
    if not today().strftime("%d.%m.") in rows[1][0]: raise NotYetAvailableException("Breisgau-Freiburg noch alt.")
    # Breisgau
    c, cc = force_int(rows[1][3].split("(")[0]), force_int(rows[1][3].split("(")[1].split(")")[0])
    d = int(rows[2][3].split(" ")[0])
    update(sheets, 8315, c=c, cc=cc, d=d, sig="Bot", ignore_delta=False)
    # Freiburg
    c, cc = force_int(rows[1][2].split("(")[0]), force_int(rows[1][2].split("(")[1].split(")")[0])
    d = int(rows[2][2].split(" ")[0])
    update(sheets, 8311, c=c, cc=cc, d=d, sig="Bot", ignore_delta=False)
    return True

schedule.append(Task(9, 00, 11, 30, 360, breisgaufreiburg, 8311))
if __name__ == '__main__': breisgaufreiburg(googlesheets())
