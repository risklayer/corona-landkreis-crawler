#!/usr/bin/python3
from botbase import *

_odenwaldkreis_st = re.compile(r"Stand: (\d\d?\.\d\d?\.20\d\d) // (\d\d?:\d\d)")

def odenwaldkreis(sheets):
    soup = get_soup("https://corona.odenwaldkreis.de/")
    #print(soup)
    stand = soup.find(attrs={"data-id":"fd96d12"}).get_text()
    stand = _odenwaldkreis_st.search(stand) or stand
    date = check_date(" ".join(stand.groups()) if not isinstance(stand, str) else stand, "Odenwaldkreis", datetime.timedelta(hours=12))
    c = force_int(soup.find(attrs={"data-id":"22de67f"}).get_text())
    d = force_int(soup.find(attrs={"data-id":"3de5323"}).get_text())
    g = force_int(soup.find(attrs={"data-id":"a4d22e5"}).get_text())
    s = force_int(soup.find(attrs={"data-id":"720ae37"}).get_text())
    i = force_int(soup.find(attrs={"data-id":"0f76b38"}).get_text())
    update(sheets, 6437, c=c, d=d, g=g, s=s, i=i, date=date)
    return True

schedule.append(Task(8, 30, 11, 35, 600, odenwaldkreis, 6437))
if __name__ == '__main__': odenwaldkreis(googlesheets())
