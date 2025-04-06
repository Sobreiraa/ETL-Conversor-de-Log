import os
import pandas as pd
import csv
import glob
from datetime import datetime


def extrair_e_transformar_dados(pasta: str) -> pd.DataFrame:
    arquivos_log = glob.glob(os.path.join(pasta, '*.log'))
    
    if not arquivos_log:
        print('Nenhum arquivo .log encontrado na pasta especificada.')
        exit()

    with open('log.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        field = ['data', 'horario', 'ping', 'sucesso']
        writer.writerow(field)  
        for caminho_arquivo in arquivos_log: 
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo_log:
                for i, linha in enumerate(arquivo_log, start=1):
                    if i == 2:
                        data = linha[0:10]
                    if i > 3:
                        horario = linha[0:8]
                        if 'error' in linha.lower():
                            ping = 2000
                            sucesso = 'Não'
                        else:
                            ping = int(linha.strip()[-5:-2])
                            sucesso = 'Sim'

                        writer.writerow([data, horario, ping, sucesso])

    df = pd.read_csv('log.csv')
    return df
    

def ordenar_dados(df: pd.DataFrame) -> pd.DataFrame:
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df_ordenado = df.sort_values(by=['data', 'horario'], ascending=[True, True]).reset_index(drop=True)
    df_ordenado['data'] = df_ordenado['data'].dt.strftime('%d/%m/%Y')
    df_ordenado.to_csv('log-ordenado.csv', index=False, date_format='%d/%m/%Y')
    return df_ordenado


def coletar_informacoes(df: pd.DataFrame):
    count_pings_errors = 0
    count_pings_sucess = 0
    soma_pings = 0

    for _, linha in df.iterrows():  
        ping = int(linha['ping'])
        sucesso = linha['sucesso']

        soma_pings += ping
        if sucesso == 'Não':
            count_pings_errors += 1
        else:
            count_pings_sucess += 1

    media = soma_pings / len(df)

    with open('informacoes_uteis.csv', 'w', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        field = ['pings com erros', 'pings com sucesso', 'media de ping']
        writer.writerow(field)
        writer.writerow([count_pings_errors, count_pings_sucess, round(media, 2)])


if __name__ == "__main__":
    pasta = r'C:\Users\Estudos\Desktop\DATA ENGINEER\03-ETL\ETL-Conversor-de-Log\data'
    data_frame = extrair_e_transformar_dados(pasta)
    data_frame_ordenado = ordenar_dados(data_frame)
    coletar_informacoes(data_frame_ordenado)
