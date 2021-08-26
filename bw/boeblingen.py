
#!/usr/bin/python3
from botbase import *

def boeblingen(sheets):
    import datetime
    data = get_json('https://services3.arcgis.com/0D1xncFOntHD7LQz/ArcGIS/rest/services/Dash_Octo/FeatureServer/1/query?where=1%3D1&outFields=*&returnGeometry=false&groupByFieldsForStatistics=F_datetime&outStatistics=[{"statisticType"%3A"sum"%2C"onStatisticField"%3A"gene_heu"%2C"outStatisticFieldName"%3A"gene_heu"}%2C{"statisticType"%3A"sum"%2C"onStatisticField"%3A"gene_diff"%2C"outStatisticFieldName"%3A"gene_diff"}%2C{"statisticType"%3A"sum"%2C"onStatisticField"%3A"tot_diff"%2C"outStatisticFieldName"%3A"tot_diff"}%2C{"statisticType"%3A"sum"%2C"onStatisticField"%3A"tot_heu"%2C"outStatisticFieldName"%3A"tot_heu"}%2C{"statisticType"%3A"sum"%2C"onStatisticField"%3A"ges_heu"%2C"outStatisticFieldName"%3A"ges_heu"}%2C{"statisticType"%3A"sum"%2C"onStatisticField"%3A"ges_diff"%2C"outStatisticFieldName"%3A"ges_diff"}]&f=json')
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    ags, date = 8115, data["F_datetime"]
    date = datetime.date(year=date//10000, month=(date//100)%100, day=date%100)
    if date < datetime.date.today(): raise Exception("Böblingen noch alt: "+str(date))
    date = date.strftime("%d.%m.%Y")
    c, cc = data["ges_heu"], data["ges_diff"]
    d, dd = data["tot_heu"], data["tot_diff"]
    g, gg = data["gene_heu"], data["gene_diff"]
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, d=d, dd=dd, sig="Bot", date=date)
    return True

schedule.append(Task(9, 00, 10, 30, 300, boeblingen, 8115))
if __name__ == '__main__': boeblingen(googlesheets())
