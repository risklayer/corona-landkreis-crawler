#!/usr/bin/python3
from botbase import *

def bernkastel(sheets):
    data = get_json('https://services.arcgis.com/qM5y4YzEV3zw2IHA/arcgis/rest/services/lk_bkw_corona_werte_%C3%B6ffentlich/FeatureServer/0/query?f=json&where=1%3D1&outFields=*&returnGeometry=false')
    data = data["features"][0]["attributes"]
    #for k,v in data.items(): print(k,v,sep="\t")
    date = check_date(data["Stand"].split(" ",2)[1], "Bernkastel")
    data2 = get_json('https://services.arcgis.com/qM5y4YzEV3zw2IHA/arcgis/rest/services/COVID19_F%C3%A4lle__neu_Juli_2021_%C3%B6ffentlich/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outStatistics=[{"onStatisticField"%3A"Faelle"%2C"outStatisticFieldName"%3A"Faelle"%2C"statisticType"%3A"sum"}%2C{"onStatisticField"%3A"Veraenderu"%2C"outStatisticFieldName"%3A"Veraenderu"%2C"statisticType"%3A"sum"}%2C{"onStatisticField"%3A"Genesene"%2C"outStatisticFieldName"%3A"Genesene"%2C"statisticType"%3A"sum"}%2C{"onStatisticField"%3A"Veraende_1"%2C"outStatisticFieldName"%3A"Veraende_1"%2C"statisticType"%3A"sum"}%2C{"onStatisticField"%3A"Todesfaell"%2C"outStatisticFieldName"%3A"Todesfaell"%2C"statisticType"%3A"sum"}]&f=json')
    data2 = data2["features"][0]["attributes"]
    c, cc = data["Infizierte"], data2["Veraenderu"]
    d = data["Todesfaelle"]
    g, gg = data["Genesene"], data["Genesene_Vortag"]
    update(sheets, 7231, c=c, cc=cc, g=g, gg=gg, d=d, sig="Bot", ignore_delta=today().weekday()==0) # Delta nur Montags?
    return True

schedule.append(Task(12, 30, 12, 40, 360, bernkastel, 7231)) # Wochenede früher
schedule.append(Task(16, 00, 17, 30, 360, bernkastel, 7231))
if __name__ == '__main__': bernkastel(googlesheets())
