#!/usr/bin/python3
from botbase import *

_kitzingen_c = re.compile(r"([0-9.]+) bestätigte Corona-Fälle")
_kitzingen_d = re.compile(r"([0-9.]+) Personen davon sind gestorben")
_kitzingen_g = re.compile(r"([0-9.]+) Personen (?:gesund|sind genesen)")
_kitzingen_q = re.compile(r"([0-9.]+) Personen sind als enge Kontaktpersonen")
_kitzingen_st = re.compile(r"Stand:? (\d\d?\. \w+ 20\d\d), (\d\d(?:\.\d\d)?)")

def kitzingen(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.kitzingen.de/buergerservice/aktuelles/aktuelles-2020/uebersichtsseite-corona/")
    text = soup.find(id="maincontent").find(class_="text").get_text(" ").strip()
    text = re.sub("\s+", " ", text)
    #print(text)
    stand = _kitzingen_st.search(text).groups()
    stand = stand[0] + " " + stand[1].replace(".",":") + (":00" if len(stand[1]) == 2 else "")
    if "2021" in stand: stand = stand.replace("2021","2022") # falsch anfang des Jahres
    date = check_date(stand, "Kitzingen") #, datetime.timedelta(hours=14))
    #if not today().strftime("%-d. %B %Y") in text: raise NotYetAvailableException("Kitzingen: "+text[:50])
    c = force_int(_kitzingen_c.search(text).group(1))
    d = force_int(_kitzingen_d.search(text).group(1))
    g = force_int(_kitzingen_g.search(text).group(1)) if _kitzingen_g.search(text) else None
    q = force_int(_kitzingen_q.search(text).group(1)) + c - d - g if g else None
    update(sheets, 9675, c=c, d=d, g=g, q=q, sig="Bot", date=date)
    return True

schedule.append(Task(10, 2, 14, 35, 600, kitzingen, 9675))
if __name__ == '__main__': kitzingen(googlesheets())
