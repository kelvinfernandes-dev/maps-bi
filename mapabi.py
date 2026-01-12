import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import os

# Utilizaremos o Nominatim pois é um serviço gratuito, para isso precisamos nomear o 'user_agent'
# É uma exigência do serviço

geolocator = Nominatim(user_agent="meu_rastreador_logistico")

# RateLimiter ajuda a não ser banido do serviço com muitas solicitações de vez

geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def buscar_coordenadas(row):
    try:
        cep_str = str(row['CEP'])
        query_cep = f"{row['CEP']}, Brasil"
        location = geocode(query_cep)

        # Se falhou ou é o CEP -999, -000 ou -899, tenta por cidade ou estado
        ceps_problema = ["-999", "-000", "-899"]
        if location is None or any(p in cep_str for p in ceps_problema):
            query_fallback = f"{row['Cidade']}, {row['Estado']}, Brasil"
            location = geocode(query_fallback)

        if location:
            return pd.Series([location.latitude, location.longitude, 'Sucesso'])
    except Exception as e:
        print(f"Erro ao processar linha: {e}")
        pass

    return pd.Series([None, None, 'Falha'])

#Carrega seu arquivo csv ou xlsx, de preferência pelo fator do projeto, utilize sempre csv

arquivo_entrada = "teste.xlsx"

if os.path.exists(arquivo_entrada):
    df = pd.read_excel("teste.xlsx")

    print("Iniciando geolocalização... Isso pode demorar 1 linha por segundo")

    # Aplica a função criando 03 novas colunas
    df[['Latitude', 'Longitude', 'Status_Geocod']] = df.apply(buscar_coordenadas, axis=1)

    # Salva o resultado
    df.to_csv("dados_geolocalizados.csv", index=False)
    print("Processamento concluído! Arquivo 'dados_geolocalizados.csv' gerado.")
 
else:
    print(f"ERRO: O arquivo '{arquivo_entrada}' não foi encontrado na pasta.")

