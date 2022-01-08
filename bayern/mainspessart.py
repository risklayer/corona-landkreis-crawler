#!/usr/bin/python3
## Tommy
from botbase import *

_mainspessart_date = re.compile(r"(?:Pressemitteilung vom|Stand:)\s(\d\d?\.(?:\d\d?\.20\d\d|\s\w+))")
_mainspessart_c = re.compile(r"Insgesamt gab es damit seit Beginn der Pandemie ([0-9.]+)")
_mainspessart_g = re.compile(r"Genesen sind davon ([0-9.]+)")
_mainspessart_a = re.compile(r"([0-9.]+) Personen mit dem\sCorona-?Virus infiziert")
_mainspessart_q = re.compile(r"([0-9.]+|\w+) enge\sKontaktpersonen")
_mainspessart_s = re.compile(r"(-?[0-9.]+|\w+)\sCovid-Patienten\sbehandelt")
_mainspessart_i = re.compile(r"(-?[0-9.]+|\w+)\sauf\sder\sIntensivstation")

def mainspessart(sheets):
    soup = get_soup("https://www.main-spessart.de/aktuelles/corona/index.html")
    content = soup.find("div", {"class": "c_content"}).get_text()
    #print(content)
    date_text = _mainspessart_date.search(content).group(1)
    check_date(date_text, "Main-Spessart")

    c = force_int(_mainspessart_c.search(content).group(1))
    g = force_int(_mainspessart_g.search(content).group(1))
    a = force_int(_mainspessart_a.search(content).group(1))
    q = force_int(_mainspessart_q.search(content).group(1)) + a
    s = force_int(_mainspessart_s.search(content).group(1)) if _mainspessart_s.search(content) else None
    i = force_int(_mainspessart_i.search(content).group(1)) if _mainspessart_i.search(content) else None

    update(sheets, 9677, c=c, g=g, q=q, s=s, i=i, sig="Bot")
    return True

schedule.append(Task(11, 55, 15, 55, 360, mainspessart, 9677))
if __name__ == '__main__': mainspessart(googlesheets())
