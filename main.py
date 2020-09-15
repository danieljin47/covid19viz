import json
import folium
import requests
import mimetypes
import http.client
import pandas as pd
from folium.plugins import HeatMap
from pandas.io.json import json_normalize

conn=http.client.HTTPSConnection("api.covid19api.com")
payload=''
headers={}
conn.request("GET","/summary",payload,headers)
res=conn.getresponse()
data=res.read().decode('UTF-8')

covidSummary = json.loads(data)
df=pd.Dataframe(covidSummary['Country'])
covidSummary2=df.drop(columns=['CountryCode','Slug','Date','Premium'])

worldmap=folium.Map(tiles='Stamen Terrain')
url='http://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
country_shapes=f'{url}/world-countries.json



