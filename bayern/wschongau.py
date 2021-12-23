#!/usr/bin/python3
## Tommy

from botbase import *

_wschongau_cc = re.compile(r"([0-9.]+|\w+) neue Fälle gemeldet")
_wschongau_c = re.compile(r"Insgesamt sind im Landkreis Weilheim-Schongau bisher ([0-9.]+) Personen mit einem positiven Test")
_wschongau_d = re.compile(r"insgesamt ([0-9.]+) Personen verstorben")
_wschongau_dd = re.compile(r"([0-9.]+|\w+) weiteren? Todesf")
_wschongau_q = re.compile(r"([0-9.]+|\w+) weitere Kontaktpersonen in Quarantäne")
_wschongau_a = re.compile(r"Aktuell befinden sich ([0-9.]+|\w+)")
_wschongau_g = re.compile(r"([0-9.]+) Fälle wieder genesen")

def wschongau(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    domain = "https://www.weilheim-schongau.de"
    soup = get_soup(domain)

    for item in soup.find_all("div", {"class":"newsItem"}):
        if "Aktuelle Meldung zum Coronavirus" in item.text:
            date = item.find("p").text.strip()
            check_date(date, "Wschongau")
            link = item.find("a")["href"]
            break

    content = get_soup(domain+link).text
    #print(content)

    c = force_int(_wschongau_c.search(content).group(1))
    cc = force_int(_wschongau_cc.search(content).group(1)) if _wschongau_cc.search(content) else None

    d = force_int(_wschongau_d.search(content).group(1))
    dd = force_int(_wschongau_dd.search(content).group(1)) if _wschongau_dd.search(content) else None

    temp = force_int(_wschongau_q.search(content).group(1))
    a = force_int(_wschongau_a.search(content).group(1))
    q = temp + a

    g = force_int(_wschongau_g.search(content).group(1))

    update(sheets, 9190, c=c, cc=cc, d=d, dd=dd, q=q, g=g, sig="Bot", ignore_delta="mon")

    return True

schedule.append(Task(15, 41, 17, 41, 360, wschongau, 9190))
if __name__ == '__main__': wschongau(googlesheets())


