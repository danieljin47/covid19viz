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
country_boundaries=f'{url}/world-countries.json

folium.Choropleth(
    geo_data=country_boundaries,
    name='Covid-19',
    data=covidSummary2,
    columns=['Country','TotalConfirmed'],
    key_on='feature.properties.name',
    fill_color='PuBuGn',
    nan_fill_color='black',
    legend_name='Total Confirmed Covid Cases',
).add_to(worldmap)

#map total confirmed figures to 'Total Confirmed:{}' interpolated format
covidSummary2.update(covidSummary2['TotalConfirmed'].map('Total Confirmed:{}'.format))
covidSummary2.update(covidSummary2['TotalRecovered'].map('Total Recovered:{}'.format))

countryCoordinates=pd.read_csv('https://gist.githubusercontent.com/tadast/8827699/raw/3cd639fa34eec5067080a61c69e3ae25e3076abb/countries_codes_and_coordinates.csv')

covidSummary3=pd.merge(covidSummary2,countryCoordinates,on='Country')
covid_final=covidSummary3.drop(columns=['Alpha-2 code', 'Alpha-3 code', 'Numeric code'])

def plotDot(point):
    folium.CircleMarker(location=[point.latitude,point.longitude],
                       radius=5,
                       weight=2,
                       popup=[point.Country,point.TotalConfirmed,point.TotalRecovered],
                       fill_color='#000000').add_to(worldmap)
    
covid_final.apply(plotDot,axis='columns')
