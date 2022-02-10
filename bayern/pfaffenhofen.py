#!/usr/bin/python3
## Tommy
from botbase import *

_pfaffenhofen_cc = re.compile(r"([0-9.]+|\w+) neuer?n? Coronavirus-Fälle bestätigt")
_pfaffenhofen_c = re.compile(r"Seit Beginn der Corona-Pandemie wurden ([0-9.]+) Landkreisbürger\*innen positiv auf das Coronavirus getestet")
_pfaffenhofen_d = re.compile(r"([0-9.]+) Personen sind verstorben")
_pfaffenhofen_q = re.compile(r"([0-9.]+|\w+) Personen gelten derzeit als Kontaktpersonen und befinden sich deshalb in häuslicher Quarantäne")
_pfaffenhofen_a = re.compile(r"Aktuell sind damit ([0-9.]+|\w+)")
_pfaffenhofen_g = re.compile(r"([0-9.]+) als genesen")
_pfaffenhofen_s = re.compile(r"([0-9.]+|\w+) bestätigte\w+ Coronavirus-Patienten behandelt")
_pfaffenhofen_i = re.compile(r"([0-9.]+|\w+) davon m\w+ intensiv")

def pfaffenhofen(sheets):
    domain = "https://www.landkreis-pfaffenhofen.de"
    soup = get_soup("https://www.landkreis-pfaffenhofen.de/meta/aktuelle-pressemitteilungen-zum-coronavirus/")

    for item in soup.find_all("div", {"class":"newslist-item col-md-4 corona d-block d-md-flex style-modern layout-card design-custom"}):
        if "Corona-Update" in item.text:
            date = item.find("small", {"class":"text-muted card-date"}).text.strip()
            check_date(date, "Pfaffenhofen")
            link = item.find("a")["href"]
            break

    content = get_soup(domain+link).find(id="News").text
    #print(content)

    c = force_int(_pfaffenhofen_c.search(content).group(1))
    cc = force_int(_pfaffenhofen_cc.search(content).group(1))
    d = force_int(_pfaffenhofen_d.search(content).group(1))
    temp = force_int(_pfaffenhofen_q.search(content).group(1)) if _pfaffenhofen_q.search(content) else None
    a = force_int(_pfaffenhofen_a.search(content).group(1))
    q = temp + a if temp else None
    g = force_int(_pfaffenhofen_g.search(content).group(1))
    s = force_int(_pfaffenhofen_s.search(content).group(1)) if _pfaffenhofen_s.search(content) is not None else None
    i = force_int(_pfaffenhofen_i.search(content).group(1)) if _pfaffenhofen_i.search(content) is not None else None

    update(sheets, 9186, c=c, cc=cc, d=d, q=q, g=g, s=s, i=i, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(15, 5, 17, 45, 360, pfaffenhofen, 9186))
if __name__ == '__main__': pfaffenhofen(googlesheets())
