from geopy.distance import geodesic
import pandas as pd

def tratamento_data(df):
    """
    Função para tratar e formatar os dados de data e hora em um DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame contendo as colunas 'data_completa' e 'hora'.
    
    Returns:
        pd.DataFrame: DataFrame com a coluna 'data_hora_completa' formatada e linhas filtradas.
    """
    # Remover ' UTC' da coluna de hora, se existir
    df['hora'] = df['hora'].str.replace(' UTC', '')

    # Adicionar dois pontos ':' para o formato correto de hora, se necessário
    df['hora'] = df['hora'].apply(lambda x: x[:2] + ':' + x[2:] if len(x) == 4 else x)

    # Combinar data_completa e hora em uma nova coluna
    df['data_hora_completa'] = df['data_completa'] + ' ' + df['hora']

    # Substituir '-' por '/' na coluna 'data_hora_completa'
    df['data_hora_completa'] = df['data_hora_completa'].str.replace('-', '/')

    # Converter a coluna 'data_hora_completa' para o tipo datetime
    df['data_hora_completa'] = pd.to_datetime(df['data_hora_completa'], format='%Y/%m/%d %H:%M')

    # Filtrar linhas para manter apenas dados entre os anos de 2019 e 2023
    df = df[(df['data_hora_completa'].dt.year >= 2019) & (df['data_hora_completa'].dt.year <= 2023)]

    # Remover colunas desnecessárias
    df.drop(columns=['data_completa', 'hora'], inplace=True)

    return df

def calcular_distancia(coord1, coord2):
    """
    Função para calcular a distância geográfica entre duas coordenadas.
    
    Args:
        coord1 (tuple): Primeira coordenada (latitude, longitude).
        coord2 (tuple): Segunda coordenada (latitude, longitude).
    
    Returns:
        float: Distância em quilômetros entre as duas coordenadas.
    """
    return geodesic(coord1, coord2).kilometers