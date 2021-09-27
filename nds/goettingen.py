#!/usr/bin/python3
from botbase import *

_goettingen_c = re.compile(r"Landkreis Göttingen beträgt\s+([0-9.]+)\s*\.", re.U)
_goettingen_d = re.compile(r"([0-9.]+) Menschen sind in Verbindung mit Covid-19 gestorben")
_goettingen_g = re.compile(r"gelten ([0-9.]+) Personen als wieder von der Infektion genesen")

def goettingen(sheets):
    from urllib.parse import urljoin
    soup = get_soup("https://www.goettingen.de/leben/aktuelles-leben-in-goettingen.html")
    articles = soup.find(id="content").findAll(class_="teaser1")
    article = next(a for a in articles if "aktuelle Infektionen" in a.get_text())
    date = article.find(class_="magazinedate").text if article else None
    date = check_date(date, "Göttingen")
    url = urljoin("https://www.goettingen.de/", article.find("a")["href"])
    print("Getting", url)
    assert url
    soup = get_soup(url)
    text = soup.find(id="content").get_text()
    #print(text)
    c = force_int(_goettingen_c.search(text).group(1))
    d = force_int(_goettingen_d.search(text).group(1))
    g = force_int(_goettingen_g.search(text).group(1))
    update(sheets, 3159, c=c, d=d, g=g, sig="Bot")
    return True

schedule.append(Task(13, 30, 15, 35, 360, goettingen, 3159))
if __name__ == '__main__': goettingen(googlesheets())
