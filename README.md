Requirements
============
Pretty standard python, except for the Google API client libraries.

```
pip install google-auth-oauthlib google-api-python-client
pip install beautifulsoup4 python-dateutil lxml pandas dateparser pdfminer.six
```

Register Google Sheets Application
==================================

Go to <https://console.cloud.google.com/>
and create credentials following the instructions from
<https://developers.google.com/workspace/guides/create-credentials>

Create a project, enable the Spreadsheets API,
create a new set of OAuth WEB application credentials.
As callback URI, configure http://localhost:8080/

Download the credentials, save as `credentials.json`.
Do not commit credentials to the repository.


Run
===

To run the scheduler, use `python3 scheduler.py`.

To run everything once (independent of the schedule), use `python3 scheduler.py --all --once`.

To manually run a single crawler, use, e.g., `python3 -m nds.nienburg`.


Adding new crawlers
===================

Each site crawler lives in its own file, e.g., `bayern/muenchen.py`.
To load them into the scheduler, they must be imported in one of the toplevel files, e.g., `bayern/__init__.py`.

Many crawlers will either use regular expressions, or directly access JSON APIs.

Crawlers tend to *break* quite often when a site layout changes, unfortunately.
Current code is designed to rather not fill the spreadsheet then, but leave it for humans.


Update and extend - ArcGIS example
==================================

As website change, updates will be necessary. To crawl the common arcgis
Dashboard, navigate to the dashboard in your browser and open the console
(in Firefox with Ctrl+Shift+I).
Go to the network monitor, reload the page, and filter the networks
accesses for `query` URLs. By stripping the parameters of these URLs
(everything after `/query`), you usually can access a query interface.
Dashboards may have multiple data sources, so try different of these URLs
until you find what you need. These can be set to return JSON (some dashboard
load the data in protobuf format, do not be scared away by this).
Or use the existing query, and just replace the format `f=` parameter
with `f=html`.

Example:
<https://services2.arcgis.com/mL26ZKdlhFJH9AoM/arcgis/rest/services/es_corona/FeatureServer/0/query>

Then fill *Where* with `1=1` (trivially true condition),
set *Out Fields* to `*`, and *Return Geometry* (if present) to false:

<https://services2.arcgis.com/mL26ZKdlhFJH9AoM/arcgis/rest/services/es_corona/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false>

Sometimes you can select a single record this way (e.g., by some ID or name,
using the *where* parameter). In other cases, you can have arcgis aggregate
the data for you. The syntax is quite messy, though.
Aggregation is done in the field *Output Statistics*.
The syntax is a JSON array. You seem to need one entry per field you want to
sum. For example:
```
[{"statisticType":"sum","onStatisticField":"inf_ges","outStatisticFieldName":"inf_ges"},
{"statisticType":"sum","onStatisticField":"inf_neu","outStatisticFieldName":"inf_neu"},
{"statisticType":"sum","onStatisticField":"tod_ins","outStatisticFieldName":"tod_ins"},
{"statisticType":"sum","onStatisticField":"tod_neu","outStatisticFieldName":"tod_neu"},
{"statisticType":"sum","onStatisticField":"pers_qua","outStatisticFieldName":"pers_qua"},
{"statisticType":"sum","onStatisticField":"verm_gen","outStatisticFieldName":"verm_gen"}]
```
In this particular dashboard, it turns out only `inf_ges` and `pers_qua`
are used, the others are 0. Furthermore, we need to *group by* `dat_text`
(per day), and *order by* `dat_text DESC` to get the *result record count* 2
latest values only. This allows us to compute the total and the active cases
as well as their change, but not yet the number of deaths.

The final URI then is the query: <https://services2.arcgis.com/mL26ZKdlhFJH9AoM/arcgis/rest/services/es_corona/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&orderByFields=dat_text+desc&groupByFieldsForStatistics=dat_text&outStatistics=[{"statisticType"%3A"sum"%2C"onStatisticField"%3A"inf_ges"%2C"outStatisticFieldName"%3A"inf_ges"}%2C{"statisticType"%3A"sum"%2C"onStatisticField"%3A"pers_qua"%2C"outStatisticFieldName"%3A"pers_qua"}]&resultRecordCount=2&f=json>

To get the deaths, we need another data source,
<https://services2.arcgis.com/mL26ZKdlhFJH9AoM/ArcGIS/rest/services/LGA_pandemie_daten_formel/FeatureServer/0/query>.
This one is easier to use, we only need to sort by date and get the last two:
<https://services2.arcgis.com/mL26ZKdlhFJH9AoM/ArcGIS/rest/services/LGA_pandemie_daten_formel/FeatureServer/0/query?where=1%3D1&outFields=*&orderByFields=Meldedatum+DESC&resultRecordCount=2&f=json>

License
=======

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
