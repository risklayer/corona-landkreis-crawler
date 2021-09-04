#!/usr/bin/python3
from botbase import *
import re, time

_csvbreak = re.compile(r"\r?\n;{10,}\r?\n",re.M)
_sanhalt = re.compile(r"verbraucherschutz.sachsen-anhalt.de").search

def sanhalt(sheets):
    import pandas, io
    data = get_raw("https://lavst.azurewebsites.net/Corona/Verlauf/COVID19_Aktuell_Sachsen_Anhalt.csv").decode("iso-8859-1")
    data = _csvbreak.split(data)
    date = check_date(data[0].split("Stand:")[1].split(";")[0], "Sachsen-Anhalt")
    d1 = pandas.read_csv(io.StringIO(data[3]), sep=";", thousands=".", decimal=",", skiprows=2)
    #print(d1.columns, d1.columns.get_loc("31.08.2021"))
    d2 = pandas.read_csv(io.StringIO(data[5]), sep=";", thousands=".", decimal=",")
    assert (d2.columns[1:4] == ["Anzahl Fälle","verstorben","Genesene"]).all(), d2.columns[1:5]
    dom = d1.columns.get_loc(today().strftime("%d.%m.%Y")) # day of month
    todo=[]
    for i, row in d2.iterrows():
        if row[0] == "Sachsen-Anhalt": continue # Land
        ags = ags_from_name(row[0])
        #print(ags, i, *row.values[:4], d1.values[i,dom])
        c, d, g = row.values[1:4]
        cc = d1.values[i,dom]
        if ags == 15090: d, g = d + 8, g - 8 # Stendal
        #update(sheets, ags, c=c, cc=cc, d=d, g=g, sig="Land", comment="Land", date=date, check=_sanhalt, batch=batch)
        #time.sleep(5)
        todo.append([ags,c,cc,g,d])
    rows = fetch_rows(sheets, [x[0] for x in todo])
    batch = []
    for i,x in enumerate(todo):
        ags,c,cc,g,d = x
        update(sheets, ags, c=c, cc=cc, d=d, g=g, sig="Land", comment="Land", date=date, check=_sanhalt, batch=batch, row=rows[i])
    do_batch(sheets, batch)
    return True

schedule.append(Task(11, 30, 16, 00, 720, sanhalt, 15087))
if __name__ == '__main__': sanhalt(googlesheets())
