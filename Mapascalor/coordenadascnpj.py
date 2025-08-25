import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm
import time

# Carregar planilha
planilha = r"C:\Users\USER\Downloads\Porfavordeus.xlsx"
df = pd.read_excel(planilha)

# Limitar o número de linhas para teste (remova depois)


# Inicializar geolocalizador com timeout e controle de taxa
geolocator = Nominatim(user_agent="meu_tcc_geocoder", timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Função com tratamento de erro
def obter_coordenadas(endereco):
    try:
        local = geocode(endereco + ", São Paulo, SP, Brasil")
        if local:
            return pd.Series([local.latitude, local.longitude])
        else:
            return pd.Series([None, None])
    except Exception as e:
        print(f"Erro com endereço: {endereco} -> {e}")
        return pd.Series([None, None])

# Usar tqdm para barra de progresso
tqdm.pandas()

# Gerar coordenadas únicas por bairro
coordenadas_cache = {}
for bairro in tqdm(df['Bairro'].unique(), desc="Geocodificando"):
    coordenadas_cache[bairro] = obter_coordenadas(bairro)

# Mapear as coordenadas de volta para o DataFrame
# Mapear as coordenadas de volta para o DataFrame
df[['Latitude', 'Longitude']] = df['Bairro'].map(coordenadas_cache).apply(pd.Series)


# Salvar resultado
df.to_excel("Cnpj_com_coordenadas2.xlsx", index=False)
