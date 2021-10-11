#!/usr/bin/python3
from botbase import *
import re, time

_csvbreak = re.compile(r"\r?\n;{10,}\r?\n",re.M)
_sanhalt = re.compile(r"verbraucherschutz.sachsen-anhalt.de").search

def sanhalt(sheets):
    import pandas, io, dateparser
    data = get_raw("https://lavst.azurewebsites.net/Corona/Verlauf/COVID19_Aktuell_Sachsen_Anhalt.csv").decode("iso-8859-1")
    data = _csvbreak.split(data)
    date = dateparser.parse(data[0].split("Stand:")[1].split(";")[0], locales=["de"])
    date = check_date(date, "Sachsen-Anhalt")
    d1 = pandas.read_csv(io.StringIO(data[5]), sep=";", thousands=".", decimal=",", skiprows=2)
    d2 = pandas.read_csv(io.StringIO(data[7]), sep=";", thousands=".", decimal=",")
    #print(d1, d2)
    assert (d2.columns[1:4] == ["Anzahl Fälle","verstorben","Genesene"]).all(), d2.columns[1:5]
    dom = d1.columns.get_loc(today().strftime("%d.%m.%Y")) # day of month
    todo=[]
    for i, row in d2.iterrows():
        if row[0] == "Sachsen-Anhalt": continue # Land
        ags = ags_from_name(row[0])
        #print(ags, i, *row.values[:4], d1.values[i,dom])
        c, d, g = row.values[1:4]
        cc = d1.values[i,dom]
        if ags == 15088: continue # Saalekreis
        if ags == 15089: d = None # Salzlandkreis
        #if ags == 15090: d, g = d + 8, g - 8 # Stendal
        #update(sheets, ags, c=c, cc=cc, d=d, g=g, sig="Land", comment="Land", date=date, check=_sanhalt, batch=batch)
        #time.sleep(5)
        todo.append([ags,c,cc,g,d])
    rows = fetch_rows(sheets, [x[0] for x in todo])
    batch = []
    for i,x in enumerate(todo):
        ags,c,cc,g,d = x
        update(sheets, ags, c=c, cc=cc, d=d, g=g, sig="Land", comment="Land", date=date, check=_sanhalt, batch=batch, row=rows[i], ignore_delta="sachsen-anhalt" in rows[i][14])
    do_batch(sheets, batch)
    return True

schedule.append(Task(11, 30, 17, 00, 720, sanhalt, 15087))
if __name__ == '__main__': sanhalt(googlesheets())
