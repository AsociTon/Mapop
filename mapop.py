import folium
import pandas
import geopy
import random
from geopy.geocoders import Nominatim

df1 = pandas.read_json("095 supermarkets.json")
#categorising the data set found from the file
df1["Co"] = df1["Address"]+","+df1["City"]+","+df1["Country"]
g = geopy.Nominatim(scheme = "http")
df1["Coa"] = df1["Co"].apply(g.geocode)
df1["latitude"] = df1["Coa"].apply(lambda x: x.latitude if x != None else None)
df1["longitude"] = df1["Coa"].apply(lambda x: x.longitude if x != None else None)

map = folium.Map(location = [27,77],zoom_start=7)

fgs = folium.FeatureGroup(name = "SuperMarkets")
fgs.add_child(folium.Marker(location = [27,77], popup = "Hey this should be Delhi",icon = folium.Icon(color = "black")))
la = 27.0
lo = 77.0
for i in range(10):
    lo += 0.2
    fgs.add_child(folium.Marker(location = [la,lo], popup  = "loc"+str(i),icon = folium.Icon(color = "red")))
las = df1["latitude"]
los = df1["longitude"]
def rcolor():
        return random.choice(["black","blue"])
for i in range(len(las)):
    fgs.add_child(folium.Marker(location = [las[i],los[i]], popup = "json super loc"+str(i),icon = folium.Icon(color = rcolor())))

#appending a GeoJson file to the map that basically draws the boundary for various countries via the below statement
fg = folium.FeatureGroup(name = "Map Fill")
fg.add_child(folium.GeoJson(data = open("world.json","r",encoding  = "utf-8-sig").read(),style_function = lambda x:{"fillColor":"yellow"}))

map.add_child(fgs)
map.add_child(fg)
map.add_child(folium.LayerControl())
map.save("dmap.html")
