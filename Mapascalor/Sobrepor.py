import folium
from folium import plugins
import pandas as pd

imigrante = pd.read_excel(r"C:\Users\USER\Desktop\Trabalho.xlsx")
carnaval = pd.read_excel(r"C:\Users\USER\Downloads\Carnavaltra.xlsx")

m = folium.Map(location=[-23.55, -46.63], zoom_start=11)

# Exemplo de recriação das camadas
folium.Choropleth(
    geo_data='imigrante.geojson',
    data= imigrante,  # dataframe com os dados
    columns=['bairro', 'valor'],
    key_on='feature.properties.bairro',
    fill_color='YlOrRd',
    name='imigrante',
    fill_opacity=0.6,
    line_opacity=0.2,
).add_to(m)

folium.Choropleth(
    geo_data='carnaval.geojson',
    data=carnaval,  # dataframe com os dados
    columns=['bairro', 'valor'],
    key_on='feature.properties.bairro',
    fill_color='PuBu',
    name='Festividade',
    fill_opacity=0.6,
    line_opacity=0.2,
).add_to(m)

folium.LayerControl().add_to(m)
m.save("mapa_com_camadas.html")
