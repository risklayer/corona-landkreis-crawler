class NotYetAvailableException(Exception): pass

_zahlen = {"niemand":0, "keinerlei":0, "kein": 0, "keine": 0, "keinen":0, "ein":1, "eine":1, "einen":1, "zwei":2, "drei":3, "vier":4, "fünf":5, "sechs":6, "sieben":7, "acht":8, "neun":9, "zehn":10, "elf":11, "zwölf": 12}

# Parsing utility, ignores whitespace and dots
def force_int(x, fallback=None):
    if x is None: return fallback
    if isinstance(x, int): return x
    if isinstance(x, str) and x.lower() in _zahlen: return _zahlen[x.lower()]
    try:
        return int(x.replace(".","").replace(" ","").lstrip("+"))
    except ValueError: return fallback

import datetime
def check_date(d, lk, offset=datetime.timedelta(0)):
    import datetime, dateutil.parser
    if d == None: raise NotYetAvailableException(lk+" noch alt: date is None")
    if isinstance(d, datetime.datetime):
        if (d + offset).date() < datetime.date.today(): raise NotYetAvailableException(lk+" noch alt: "+str(d))
        return d
    if isinstance(d, datetime.date):
        if (d + offset) < datetime.date.today(): raise NotYetAvailableException(lk+" noch alt: "+str(d))
        return d
    if isinstance(d, int):
        if d >= 20210101 and d <= 20230101:
            d = datetime.datetime(year=d//10000, month=(d//100)%100, day=d%100)
        elif d > 1e10:
            d = datetime.datetime.utcfromtimestamp(d / 1000) # arcgis dashboard timestamps
        else:
            d = datetime.datetime.utcfromtimestamp(d)
        if (d + offset).date() < datetime.date.today(): raise NotYetAvailableException(lk+" noch alt: "+str(d))
        return d
    d = d.replace("Uhr","").replace(","," ").replace("  "," ").strip()
    pd = dateutil.parser.parse(d, dayfirst="-" not in d)
    if (pd + offset).date() < datetime.date.today(): raise NotYetAvailableException(lk+" noch alt: "+str(d))
    return pd

