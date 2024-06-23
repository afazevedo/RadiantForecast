import os
import requests
import zipfile
from io import BytesIO
import pandas as pd
from requests.exceptions import HTTPError

def baixar_e_extrair_zip(url, extrair_em='.'):
    """
    Baixa e extrai um arquivo ZIP da URL fornecida.

    Args:
        url (str): URL do arquivo ZIP a ser baixado.
        extrair_em (str): Diretório onde os arquivos serão extraídos.
    """
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(extrair_em)
    else:
        print(f"Falha ao baixar {url}")

def ler_csv_com_metadados(caminho_arquivo):
    """
    Lê um arquivo CSV com metadados nas primeiras linhas e retorna um DataFrame.

    Args:
        caminho_arquivo (str): Caminho para o arquivo CSV.

    Returns:
        pd.DataFrame: DataFrame com dados e metadados como colunas.
    """
    try:
        with open(caminho_arquivo, 'r', encoding='latin1') as f:
            linhas = f.readlines()

        # Extrair metadados das primeiras linhas
        metadados = {}
        for i in range(7):
            chave, valor = linhas[i].strip().split(';')
            metadados[chave] = valor

        # Ler o resto do arquivo como DataFrame
        df = pd.read_csv(caminho_arquivo, delimiter=';', encoding='latin1', skiprows=8)
        
        # Adicionar metadados como colunas
        for chave, valor in metadados.items():
            df[chave] = valor
        
        return df
    except Exception as e:
        print(f"Erro ao ler o arquivo {caminho_arquivo}: {e}")
        return None

def filtrar_colunas(df):
    """
    Filtra as colunas importantes de um DataFrame.

    Args:
        df (pd.DataFrame): DataFrame original.

    Returns:
        pd.DataFrame: DataFrame com apenas as colunas importantes.
        list: Lista de colunas importantes.
    """
    # Definir índices das colunas importantes
    indices_colunas_importantes = [0, 1, 6, 7, 15, 18, 22, 24, 25, 26]
    colunas_importantes = df.columns[indices_colunas_importantes]

    return df[colunas_importantes], colunas_importantes

def renomear_colunas(df, colunas_importantes):
    """
    Renomeia as colunas de um DataFrame de acordo com um dicionário de mapeamento.

    Args:
        df (pd.DataFrame): DataFrame original.
        colunas_importantes (list): Lista de colunas importantes.

    Returns:
        pd.DataFrame: DataFrame com colunas renomeadas e reordenadas.
    """
    dicionario_colunas = {
        0: 'data_completa',
        1: 'hora',
        2: 'radiacao_global',
        3: 'temperatura_ar',
        4: 'umidade_relativa',
        5: 'velocidade_vento',
        6: 'estacao',
        7: 'latitude',
        8: 'longitude',
        9: 'altitude',
    }

    for i in range(len(colunas_importantes)):
        df.rename(columns={colunas_importantes[i]: dicionario_colunas[i]}, inplace=True)
     
    # Reordenar colunas
    df = df[[
        'estacao',
        'data_completa',
        'hora',
        'radiacao_global',
        'temperatura_ar',
        'umidade_relativa',
        'velocidade_vento',
        'latitude',
        'longitude',
        'altitude',
    ]]

    return df

def baixar_e_ler_excel(url, caminho_arquivo):
    """
    Baixa e lê um arquivo Excel da URL fornecida.

    Args:
        url (str): URL do arquivo Excel.
        caminho_arquivo (str): Caminho para salvar o arquivo baixado.

    Returns:
        pd.DataFrame: DataFrame com os dados do arquivo Excel.
    """
    try:
        r = requests.get(url, allow_redirects=True)
        open(caminho_arquivo, 'wb').write(r.content)
        return pd.read_excel(caminho_arquivo)
    except HTTPError as err:
        if err.code == 404:
            print(f"Arquivo não encontrado em {url}. Ignorando e continuando.")
        else:
            raise
    except Exception as e:
        print(f"Erro ao ler o arquivo {caminho_arquivo}: {e}")
    return None

def baixar_e_ler_csv(url, caminho_arquivo):
    """
    Baixa e lê um arquivo CSV da URL fornecida.

    Args:
        url (str): URL do arquivo CSV.
        caminho_arquivo (str): Caminho para salvar o arquivo baixado.

    Returns:
        pd.DataFrame: DataFrame com os dados do arquivo CSV.
    """
    try:
        r = requests.get(url, allow_redirects=True)
        open(caminho_arquivo, 'wb').write(r.content)
        return pd.read_csv(caminho_arquivo, sep=";")
    except HTTPError as err:
        if err.code == 404:
            print(f"Arquivo não encontrado em {url}. Ignorando e continuando.")
        else:
            raise
    except Exception as e:
        print(f"Erro ao ler o arquivo {caminho_arquivo}: {e}")
    return None

def processar_dataframe(df):
    """
    Processa e limpa um DataFrame, removendo colunas irrelevantes e filtrando dados específicos.

    Args:
        df (pd.DataFrame): DataFrame original.

    Returns:
        pd.DataFrame: DataFrame processado e limpo.
    """
    colunas_para_remover = ["id_subsistema", "nom_estado", "cod_modalidadeoperacao", "nom_tipocombustivel"]
    df.drop(columns=colunas_para_remover, inplace=True)
    df = df[df["nom_tipousina"] == "FOTOVOLTAICA"]
    df = df[df["id_estado"] == 'MG']
    return df

def processar_dados_geracao(ano_inicial, ano_final, dest_dir):
    """
    Processa os dados de geração de energia solar da ONS.

    Args:
        ano_inicial (int): Ano inicial para coleta de dados.
        ano_final (int): Ano final para coleta de dados.

    Returns:
        pd.DataFrame: DataFrame com os dados processados.
    """
    dfs = []  # Lista para armazenar dataframes temporários
    data_atual = pd.Timestamp.now()  # Data e hora atual
    ano_atual = data_atual.year  # Ano atual
    mes_atual = data_atual.month  # Mês atual

    for ano in range(ano_inicial, ano_atual):
        print(f"Geração por Fonte: processando ano {ano}")

        if ano >= 2022:  # Dados a partir de 2022 são fornecidos em formato Excel
            for mes in range(1, 13):
                url = f'https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/geracao_usina_2_ho/GERACAO_USINA-2_{ano}_{str(mes).zfill(2)}.xlsx'
                caminho_arquivo = dest_dir + f"/GERACAO_USINA-2_{ano}_{str(mes).zfill(2)}.xlsx"
                df = baixar_e_ler_excel(url, caminho_arquivo)  # Baixa e lê o arquivo Excel
                if df is not None:
                    dfs.append(processar_dataframe(df))  # Processa o dataframe e adiciona à lista
        else:  # Dados antes de 2022 são fornecidos em formato CSV
            url = f'https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/geracao_usina_2_ho/GERACAO_USINA_{ano}.csv'
            caminho_arquivo = dest_dir + f"/GERACAO_USINA_{ano}.csv"
            df = baixar_e_ler_csv(url, caminho_arquivo)  # Baixa e lê o arquivo CSV
            if df is not None:
                dfs.append(processar_dataframe(df))  # Processa o dataframe e adiciona à lista

    return pd.concat(dfs)  # Concatena todos os dataframes em um único dataframe