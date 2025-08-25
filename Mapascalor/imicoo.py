import pandas as pd
import folium
from folium.plugins import HeatMap
 
# Corrigindo o caminho do arquivo
caminho = r"C:\Users\USER\Desktop\TCC\Trabalho.xlsx"  # Usando raw string
# OU: caminho = "C:\\Users\\Aluno\\Downloads\\Trabalho.xlsx"
 
try:
    df = pd.read_excel(caminho)
   
    # Verificando colunas (case insensitive)
    required_columns = {'latitude', 'longitude'}
    if not all(col.lower() in (c.lower() for c in df.columns) for col in required_columns):
        raise ValueError("O arquivo Excel precisa ter as colunas 'latitude' e 'longitude' (case insensitive).")
   
    # Padronizando nomes das colunas para minúsculo
    df.columns = df.columns.str.lower()
   
    dados = df[['latitude', 'longitude']].values.tolist()
   
    if not dados:
        raise ValueError("Nenhum dado encontrado para plotar.")
   
    # Pega o centro dos dados para localização inicial
    centro = [sum(x)/len(x) for x in zip(*dados)][:2]
   
    mapa = folium.Map(location=centro, zoom_start=10)
    HeatMap(dados).add_to(mapa)
   
    mapa.save("final.html2")
    print("Mapa de calor gerado com sucesso e salvo como 'final.html'")
 
except FileNotFoundError:
    print(f"Erro: Arquivo não encontrado em {caminho}")
except Exception as e:
    print(f"Erro: {str(e)}")