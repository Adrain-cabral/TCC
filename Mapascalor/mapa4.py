import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import os

# 1. Extrair o shapefile do ZIP
caminho_zip = r"C:\Users\USER\Downloads\SIRGAS_SHP_subprefeitura.zip"  # Corrigi o caminho
pasta_destino = r"C:\Users\USER\Downloads\SIRGAS_SHP_extracted"  # Corrigi o nome da pasta

if not os.path.exists(pasta_destino):
    os.makedirs(pasta_destino)
    with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:  # Corrigi a sintaxe
        zip_ref.extractall(pasta_destino)  # Corrigi o método

# 2. Carregar o shapefile
bairros = gpd.read_file(os.path.join(pasta_destino, "SIRGAS_SHP_subprefeitura.shp"))  # Corrigi para .shp

# Verificar e definir CRS se necessário
if bairros.crs is None:
    bairros = bairros.set_crs("EPSG:31983")  # SIRGAS 2000 para SP (suposição)

# Converter para WGS84 (lat/long)
bairros = bairros.to_crs("EPSG:4326")  # Corrigi "PSG4326" para "EPSG:4326"

# 3. Carregar as ocorrências
ocorrencias = pd.read_excel(r"C:\Users\USER\Downloads\Trabalho 2.xlsx")  # Corrigi o caminho

# 4. Criar GeoDataFrame das ocorrências
ocorrencias_gdf = gpd.GeoDataFrame(
    ocorrencias,
    geometry=gpd.points_from_xy(ocorrencias.Longitude, ocorrencias.Latitude),
    crs="EPSG:4326"  # Corrigi "PSG4326" para "EPSG:4326"
)

# 5. Contar ocorrências por subprefeitura
ocorrencias_por_bairro = gpd.sjoin(
    ocorrencias_gdf,
    bairros,
    how="left",
    predicate="within"
).groupby("index_right").size()

bairros["ocorrencias"] = bairros.index.map(ocorrencias_por_bairro).fillna(0)

# 6. Plotar o mapa
fig, ax = plt.subplots(figsize=(12, 10))
bairros.plot(
    column="ocorrencias",
    cmap="Reds",
    legend=True,
    edgecolor="black",
    linewidth=0.5,
    ax=ax
)

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# [...] (código anterior de carregamento dos dados mantido igual)

# 6. Criar um gradiente de vermelho mais intenso
# Definir um colormap vermelho personalizado (de branco para vermelho escuro)
reds = LinearSegmentedColormap.from_list('reds_intense', 
                                       ['#FFEEEE', '#FF0000', '#800000'], 
                                       N=256)

# 7. Plotar o mapa com maior contraste
fig, ax = plt.subplots(figsize=(12, 10))

# Usar escala logarítmica se houver muita variação nos valores
# (remove valores zero para evitar problemas com log)
ocorrencias_nonzero = bairros[bairros['ocorrencias'] > 0]['ocorrencias']
if len(ocorrencias_nonzero) > 0:
    vmin = ocorrencias_nonzero.min()
    vmax = ocorrencias_nonzero.max()
    norm = plt.colors.LogNorm(vmin=vmin, vmax=vmax) if vmax/vmin > 100 else None
else:
    norm = None

bairros.plot(column='ocorrencias',
            cmap=reds,
            legend=True,
            edgecolor='black',
            linewidth=0.3,
            ax=ax,
            norm=norm,  # Usar normalização logarítmica se necessário
            legend_kwds={'label': "Número de Ocorrências",
                        'orientation': "horizontal",
                        'shrink': 0.6})

# Destacar bairros com zero ocorrências em cinza
if 0 in bairros['ocorrencias'].values:
    bairros[bairros['ocorrencias'] == 0].plot(color='#f0f0f0', 
                                             ax=ax, 
                                             edgecolor='black', 
                                             linewidth=0.3)

plt.title("Densidade de Ocorrências por Subprefeitura", fontsize=14)
plt.axis('off')  # Remover eixos

# Ajustar layout para evitar cortes
plt.tight_layout()
plt.show()

plt.title("Ocorrências por Subprefeitura")
plt.show()