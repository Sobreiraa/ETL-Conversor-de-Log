import os
import pandas as pd
import csv
import glob
from datetime import datetime


def extrair_e_transformar_dados(pasta: str) -> pd.DataFrame:
    """
    Função para extrair de uma pasta os LOGs, transformar em um arquivo CSV e retornar o DF com as informações do arquivo CSV
    """
    arquivos_log = glob.glob(os.path.join(pasta, '*.log')) # Lista com os caminhos completos de todos os arquivos LOG dentro da pasta desejada
    
    if not arquivos_log: # Verifica se tem algum arquivo no caminho dos logs
        print('Nenhum arquivo .log encontrado na pasta especificada.')
        exit() # Sai caso não tenha nenhum arquivo na pasta informada

    with open('log.csv', 'w', newline='', encoding='utf-8') as csv_file: # Criando o arquivo CSV dos LOGs informados
        writer = csv.writer(csv_file) # Criando o objeto writer para escrever as informações no CSV
        field = ['data', 'horario', 'ping', 'sucesso'] # Definindo o nome das colunas do arquivo CSV
        writer.writerow(field)   # Escrevendo uma linha no CSV
        for caminho_arquivo in arquivos_log: # For para iterar todos os arquivos do caminho informado onde tem os LOG
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo_log: # Abrindo os arquivos de LOG
                for i, linha in enumerate(arquivo_log, start=1): # Iterando linha por linha dos LOG
                    if i == 2: # Como os arquivos são iguais e sei que a linha 2 é data, aqui coletamos a informação da data
                        data = linha[0:10]
                    if i > 3: # Da linha 3 em diante é a informação dos logs
                        horario = linha[0:8] # Coletando o horário do ping
                        if 'error' in linha.lower(): # Verificando se o ping foi perdido
                            ping = 2000 
                            sucesso = 'Não' # Definindo como 'Não' pois o ping foi perdido
                        else:
                            ping = int(linha.strip()[-5:-2]) # Coletando o ping que teve sucesso
                            sucesso = 'Sim' # Definindo como 'Sim' pois o ping foi não teve perca

                        writer.writerow([data, horario, ping, sucesso]) # Adicionando no arquivo todas as informações coletadas

    df = pd.read_csv('log.csv') # Definindo um DF como o arquivo LOG gerado
    return df # Retornando o LOG como um DF
    

def ordenar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Função para ordernar os dados de LOG em ordem crescende pelas colunas DATA e HORÁRIO.
    """
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y') # Converte os dados da coluna DATA de STR para o formato DATE
    df_ordenado = df.sort_values(by=['data', 'horario'], ascending=[True, True]).reset_index(drop=True) # Criando o DF ordenado por ordem crescente das colunas DATA e HORÁRIO
    df_ordenado['data'] = df_ordenado['data'].dt.strftime('%d/%m/%Y') # Convertendo a coluna DATA para STR para manter o ofrmato original do arquivo CSV
    df_ordenado.to_csv('log-ordenado.csv', index=False, date_format='%d/%m/%Y') # Exportando o DF ordenado para um arquivo CSV
    return df_ordenado # Retornando o DF ordenado


def coletar_informacoes(df: pd.DataFrame) -> None:
    """"""
    count_pings_errors = 0 # Variável para contar quantos pings foram perdidos
    count_pings_sucess = 0 # Variável para contar quantos pings tiveram sucesso
    soma_pings = 0 # Soma dos pings para depois calcular a média

    for _, linha in df.iterrows():  # Iternado linha por linha do DF passado
        ping = int(linha['ping']) # Coletando o ping para somar e extrair a média
        sucesso = linha['sucesso'] # Coletando os pings com sucesso ou não 

        if sucesso == 'Não': # Verificando se o ping foi perdido
            count_pings_errors += 1 # Contagem dos pings perdidos
        else: # Verificando se o ping teve sucesso
            count_pings_sucess += 1 # Contagem dos pings com sucesso
            soma_pings += ping # Somando os pings coletados
            media = soma_pings / len(df) # Calculando a média dos pings

    with open('informacoes_uteis.csv', 'w', newline='', encoding='utf-8') as arquivo: # Criando o arquivo com as informações coletadas dos pings
        writer = csv.writer(arquivo) # Criando o objeto writer para escrever no CSV
        field = ['pings com erros', 'pings com sucesso', 'media de ping'] # Nome das colunas do arquivo CSV
        writer.writerow(field) # Escrevendo no arquivo CSV com o nome das colunas
        writer.writerow([count_pings_errors, count_pings_sucess, round(media, 2)]) # Adicionando as informações coletadas no CSV


if __name__ == "__main__":
    pasta = r'C:\Users\Estudos\Desktop\DATA ENGINEER\03-ETL\ETL-Conversor-de-Log\data'
    data_frame = extrair_e_transformar_dados(pasta)
    data_frame_ordenado = ordenar_dados(data_frame)
    coletar_informacoes(data_frame_ordenado)
