import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# Carregar planilha
planilha = r"C:\Users\USER\Downloads\Carnaval.xlsx"
df = pd.read_excel(planilha)

# Inicializar geolocalizador com timeout maior
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

# Aplicar função
df[['Latitude', 'Longitude']] = df['Bairro'].apply(obter_coordenadas)

# Salvar resultado
df.to_excel("Carnaval_com_coordenadas.xlsx", index=False)

