import requests
import pandas as pd
from datetime import datetime
import telebot
import time

bot_token = 'token'
bot = telebot.TeleBot(bot_token)
mes = str(time.strftime("%m"))
url_abastecimento = 'digite-aqui-a-url-do-calendario-de-abastecimento'
url_manutencao = 'digite-aqui-a-url-do-calendario-de-manutenção'
nome_do_arquivo_de_abastecimento = 'ultimo_calendario_abastecimento.csv'
nome_do_arquivo_de_manutencao = 'ultimo_calendario_manutencao.csv'
lista_id_usuarios_telegram = [01, 02] 


def main():
    df_calendario_abastecimento = extrai_calendario(url_abastecimento)
    df_calendario_abastecimento['attributes.Inicio']  = aplica_fuso_horario_em_coluna_tempo(df_calendario_abastecimento['attributes.Inicio'])
    df_calendario_abastecimento['attributes.Termino'] = aplica_fuso_horario_em_coluna_tempo(df_calendario_abastecimento['attributes.Termino'])
    df_calendario_abastecimento['attributes.Inicio']  = converte_coluna_tempo_para_timestamp(df_calendario_abastecimento['attributes.Inicio'])
    df_calendario_abastecimento['attributes.Termino'] = converte_coluna_tempo_para_timestamp(df_calendario_abastecimento['attributes.Termino'])
    df_calendario_abastecimento.rename(columns={'attributes.Inicio': 'Inicio', 'attributes.Termino': 'Termino'}, inplace=True)
    df_calendario_abastecimento.drop('attributes.colapso', axis=1, inplace=True)
    df_calendario_abastecimento['Inicio'] = remove_minutos_segundos_em_coluna_tempo(df_calendario_abastecimento['Inicio'])
    df_calendario_abastecimento['Termino'] = remove_minutos_segundos_em_coluna_tempo(df_calendario_abastecimento['Termino'])

    df_calendario_manutencao = extrai_calendario(url_manutencao)
    df_calendario_manutencao['attributes.INICIO_PREVISTO']  = aplica_fuso_horario_em_coluna_tempo(df_calendario_manutencao['attributes.INICIO_PREVISTO'])
    df_calendario_manutencao['attributes.TERMINO_PREVISTO'] = aplica_fuso_horario_em_coluna_tempo(df_calendario_manutencao['attributes.TERMINO_PREVISTO'])
    df_calendario_manutencao['attributes.INICIO_PREVISTO']  = converte_coluna_tempo_para_timestamp(df_calendario_manutencao['attributes.INICIO_PREVISTO'])
    df_calendario_manutencao['attributes.TERMINO_PREVISTO'] = converte_coluna_tempo_para_timestamp(df_calendario_manutencao['attributes.TERMINO_PREVISTO'])
    df_calendario_manutencao.rename(columns={'attributes.INICIO_PREVISTO': 'Inicio', 'attributes.TERMINO_PREVISTO': 'Termino',
                                            'attributes.DESCRICAO_SERVICO': 'Serviço'}, inplace=True)
    df_calendario_manutencao['Inicio'] = remove_minutos_segundos_em_coluna_tempo(df_calendario_manutencao['Inicio'])
    df_calendario_manutencao['Termino'] = remove_minutos_segundos_em_coluna_tempo(df_calendario_manutencao['Termino'])

    ultimo_calendario_abastecimento_extraido = pd.read_csv(nome_do_arquivo_de_abastecimento)
    ultimo_calendario_manutencao_extraido = pd.read_csv(nome_do_arquivo_de_manutencao)

    if df_calendario_abastecimento.equals(ultimo_calendario_abastecimento_extraido) and df_calendario_manutencao.equals(ultimo_calendario_manutencao_extraido):
        print('Os calendários atuais são iguais aos últimos extraídos!')
    else:
        texto_telegram_abastecimento = cria_texto_para_envio_pelo_telegram('CALENDÁRIO DE ABASTECIMENTO: \n', df_calendario_abastecimento)
        texto_telegram_manutencao = cria_texto_para_envio_pelo_telegram('CALENDÁRIO DE MANUTENÇÃO: \n', df_calendario_manutencao)

        for id in lista_id_usuarios_telegram:
            envia_mensagem_pelo_telegram(id, texto_telegram_abastecimento)
            envia_mensagem_pelo_telegram(id, texto_telegram_manutencao)

            armazena_calendario_em_csv(df_calendario_abastecimento, nome_do_arquivo_de_abastecimento)
            armazena_calendario_em_csv(df_calendario_manutencao, nome_do_arquivo_de_manutencao)


    

def extrai_calendario(url):
    df_calendario = requests.get(url)
    df_calendario = df_calendario.json()
    df_calendario = pd.json_normalize(df_calendario['features'])

    return df_calendario

def aplica_fuso_horario_em_coluna_tempo(coluna):
    coluna = coluna + 10800000

    return coluna

def converte_coluna_tempo_para_timestamp(coluna):
    coluna = coluna.apply(lambda d: datetime.fromtimestamp(int(d)/1000).strftime('%d/%m/%Y %H:%M:%S'))

    return coluna

def remove_minutos_segundos_em_coluna_tempo(coluna):
    coluna = coluna.str[0:10] + ' ' + coluna.str[11:13] + 'h'

    return coluna

def armazena_calendario_em_csv(df_calendario, nome_do_arquivo):
    df_calendario.to_csv(nome_do_arquivo, index=False)

def cria_texto_para_envio_pelo_telegram(cabecalho, df_calendario):
    texto_para_envio_no_telegram = cabecalho
    texto_para_envio_no_telegram += df_calendario.columns[0] + ' -- ' + df_calendario.columns[1] + '\n'

    for linha in range(0,df_calendario.shape[0]):
        texto_para_envio_no_telegram += df_calendario['Inicio'].values[linha] + ' -- ' + df_calendario['Termino'].values[linha] + '\n\n'
    
    return texto_para_envio_no_telegram

def envia_mensagem_pelo_telegram(id_usuario, texto_para_envio_no_telegram):
    bot.send_message(id_usuario, texto_para_envio_no_telegram) 



main()