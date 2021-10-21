#!/usr/bin/python3
from botbase import *
import re, time
_landpat = re.compile(r"baden-w").search

def land(sheets):
    data = get_csv("http://www.gesundheitsatlas-bw.de/data/csv?inline=true&viewId=211&viewName=Coronavirus-Nachweise+-+t%c3%a4glich&geoId=1&subsetId=&instances=", sep=",")
    cols = [x for x in data.columns if not "pro 100.000" in x]
    cols = cols[:2] + [x for x in cols if "Fälle" in x][-2:] + [x for x in cols if "Todesfälle" in x][-2:]
    data = data.filter(items=cols, axis=1)
    #print(data.head())
    #print(data.columns)
    if not today().strftime("%d-%m-%y") in data.columns[-3]: raise NotYetAvailableException("Land noch alt? " + data.columns[-3])
    todo=[]
    for row in data.itertuples(index=False):
        #print(row)
        ags, name, cc, c, dd, d = row
        if ags == 8: continue # Land
        cc, dd = c - cc, d - dd
        if ags == 8111: c += 103 # Stuttgart
        todo.append( (ags,c,cc,d,dd) )
    rows = fetch_rows(sheets, [x[0] for x in todo])
    batch=[]
    for i,x in enumerate(todo):
        ags,c,cc,d,dd = x
        update(sheets, ags, c=c, cc=cc, d=d, dd=dd, sig="Land", comment="Land", check=_landpat, batch=batch, row=rows[i])
        #time.sleep(5) # to reduce rate limit problems
    do_batch(sheets, batch)
    return True

schedule.append(Task(17, 00, 21, 00, 360, land, 8317))
if __name__ == '__main__': land(googlesheets())
