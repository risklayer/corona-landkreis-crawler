#!/usr/bin/python3
from botbase import *

_oldenburglk_q = re.compile(r"strong>(\d+)</strong")

def oldenburglk(sheets):
    data = get_json("https://oldenburg-kreis.maps.arcgis.com/sharing/rest/content/items/901f1a7844ef401790b44f85cad0ebc7/data?f=json")
    layers = [x for x in data["operationalLayers"] if "Fälle" in x.get("title", "")]
    todaystr = today().strftime("%Y%m%d")
    d, dd, g, gg, a, aa, q, date = None, None, None, None, None, None, None, None
    for layer in layers:
        l = layer["featureCollection"]["layers"][0]["featureSet"]["features"]
        v = [[y for y in x["attributes"].items() if (y[0].startswith("202"))][-1] for x in l]
        vv = [[y for y in x["attributes"].items() if y[0] < todaystr][-1] for x in l]
        date = max(date, v[-1][0]) if date else v[-1][0]
        v = sum(x[1] for x in v)
        vv = sum(x[1] for x in vv)
        #print(layer["title"], todaystr, v, vv)
        if "verstorb" in layer["title"]: d, dd = v, v - vv
        if "genesen" in layer["title"]: g, gg = v, v - vv
        if "bestätigt" in layer["title"]: a, aa = v, v - vv
    date = check_date(date, "Oldenburg")
    c, cc = d + g + a, dd + gg + aa
    dataq = get_json("https://oldenburg-kreis.maps.arcgis.com/sharing/rest/content/items/d628b46803a6477d969ff9336bcafcdd/data?f=json")
    try:
        #for w in dataq["widgets"]: print(w.get("text").strip("\n"))
        widg = next(x["text"] for x in dataq["widgets"] if "Quarant" in x.get("text",""))
        q = int(_oldenburglk_q.search(widg).group(1))
    except Exception as e: raise(e)
    update(sheets, 3458, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, q=q, sig="Bot", comment="Bot Dashboard", date=date, ignore_delta=True)
    return True

schedule.append(Task(12, 25, 19, 30, 600, oldenburglk, 3458))
if __name__ == '__main__': oldenburglk(googlesheets())
