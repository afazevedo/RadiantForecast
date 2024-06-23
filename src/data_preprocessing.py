import pandas as pd

def plot_daily_energy_profile(df, year, energy_col='val_geracao'):
    """
    Filtra os dados para o ano específico, agrupa por hora do dia e calcula a média da geração de energia,
    e plota o perfil diário de geração de energia.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados de energia.
        year (int): Ano para filtrar os dados.
        energy_col (str): Nome da coluna que contém os valores de geração de energia. Padrão é 'val_geracao'.

    Returns:
        None
    """
    # Transformar data_hora_completa em datetime, se necessário
    if not pd.api.types.is_datetime64_any_dtype(df['data_hora_completa']):
        df['data_hora_completa'] = pd.to_datetime(df['data_hora_completa'])

    # Filtrar dados para o ano específico
    df_year = df[df['data_hora_completa'].dt.year == year]

    # Verificar se há dados para o ano especificado
    if df_year.empty:
        print(f"Não há dados para o ano {year}.")
        return