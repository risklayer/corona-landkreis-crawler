#!/usr/bin/python3
## Tommy
from botbase import *

_saarbruecken_cc1 = re.compile(r"Das Gesundheitsamt des Regionalverbandes meldet heute ([0-9.]+|\w+)")
_saarbruecken_cc2 = re.compile(r"Das Gesundheitsamt des Regionalverbandes meldet am Samstag (?:[0-9.]+|\w+) und am (?:heutigen )?Sonntag weitere ([0-9.]+|\w+) neue Coronafälle")
_saarbruecken_c = re.compile(r"Insgesamt liegen im Regionalverband ([0-9.]+)")
_saarbruecken_d = re.compile(r"Die Anzahl der Todesfälle, die im Zusammenhang mit dem Coronavirus stehen, (?:liegt bei |steigt (?:damit )?auf )(?:insgesamt )?([0-9.]+)")
_saarbruecken_dd = re.compile(r"([0-9.]+|\w+) weiterer?n? Todesf(?:a|ä)lle? gemeldet")

def saarbruecken(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    domain = "https://www.regionalverband-saarbruecken.de"
    soup = get_soup(domain)

    for item in soup.find_all("div", {"class":"col-sm-4"}):
        if "Fallzahl-Statistik aus dem Regionalverband" in item.text:
            link_url = item.find("a")["href"]
            break

    link_soup = get_soup(link_url)
    date = link_soup.find("time").get("datetime")
    check_date(date, "Saarbruecken")

    weekday = datetime.datetime.today().weekday()
    _saarbruecken_cc = _saarbruecken_cc2 if weekday == 6 else _saarbruecken_cc1

    content = link_soup.text
    #print(content)
    cc = force_int(_saarbruecken_cc.search(content).group(1))
    c = force_int(_saarbruecken_c.search(content).group(1))
    d = force_int(_saarbruecken_d.search(content).group(1)) if _saarbruecken_d.search(content) else None
    dd = force_int(_saarbruecken_dd.search(content).group(1)) if _saarbruecken_dd.search(content) and d is not None else None
    comment = "Bot ohne D" if d is None else "Bot"

    update(sheets, 10041, c=c, cc=cc, d=d, dd=dd, comment=comment)
    return True

schedule.append(Task(15, 41, 18, 11, 360, saarbruecken, 10041))
if __name__ == '__main__': saarbruecken(googlesheets())
