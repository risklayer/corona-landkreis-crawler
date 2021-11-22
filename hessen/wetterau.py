
#!/usr/bin/python3
from botbase import *

_wetterau_c = re.compile(r"bei *([0-9.]+) *, ([0-9.]+) *mehr als")
_wetterau_a = re.compile(r"Aktuell *([0-9.]+) *aktive")
_wetterau_gg = re.compile(r"([0-9.]+) Menschen haben sich bei der Behörde als genesen")
_wetterau_g = re.compile(r"Genesene: ([0-9.]+)")
_wetterau_d = re.compile(r"Verstorbene: ([0-9.]+)")

def wetterau(sheets):
    soup = get_soup("https://wetteraukreis.de/aktuelles/pressemitteilungen/?no_cache=1")
    li = next(x for x in soup.find("main").findAll(class_="article") if "nachgewiesenen Fälle" in x.get_text())
    check_date(li.find(class_="news-list-date").get_text(), "Wetteraukreis")
    link = li.find(href=True)["href"] if li else None
    from urllib.parse import urljoin
    link = urljoin("https://wetteraukreis.de/aktuelles/pressemitteilungen/?no_cache=1", link)
    print("Getting", link)
    soup = get_soup(link)
    text = soup.find("main").find(class_="news").get_text(" ").strip()
    #print(text)
    c, cc = map(force_int, _wetterau_c.search(text).groups())
    a = force_int(_wetterau_a.search(text).group(1))
    update(sheets, 6440, c=c, cc=cc, sig=str(a), comment="Bot ohne DG aktiv: "+str(a), ignore_delta=True)
    return True

schedule.append(Task(12, 0, 14, 35, 360, wetterau, 6440))
if __name__ == '__main__': wetterau(googlesheets())
