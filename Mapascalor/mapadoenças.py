import pandas as pd
import folium
from folium.plugins import HeatMap

caminho = r"C:\Users\USER\Desktop\TCC\Doençascood.xlsx"

try:
    df = pd.read_excel(caminho)

    # Padronizar colunas
    df.columns = df.columns.str.lower()

    # Verifica se colunas esperadas existem
    required_columns = ['latitude', 'longitude']
    if not all(col.lower() in df.columns for col in required_columns):
        raise ValueError("O arquivo precisa ter as colunas 'latitude' e 'longitude'.")

    # Remover linhas com NaN
    df = df.dropna(subset=['latitude', 'longitude'])

    # Extrair coordenadas
    dados = df[['latitude', 'longitude']].values.tolist()

    if not dados:
        raise ValueError("Nenhum dado encontrado para plotar.")

    # Ponto central para iniciar o mapa
    centro = [sum(x)/len(x) for x in zip(*dados)][0:2]

    # Criar e salvar mapa
    mapa = folium.Map(location=centro, zoom_start=10)
    HeatMap(dados).add_to(mapa)
    mapa.save("final5.html")
    print("Mapa de calor gerado com sucesso e salvo como 'final5.html'")

except FileNotFoundError:
    print(f"Erro: Arquivo não encontrado em {caminho}")
except Exception as e:
    print(f"Erro: {e}")