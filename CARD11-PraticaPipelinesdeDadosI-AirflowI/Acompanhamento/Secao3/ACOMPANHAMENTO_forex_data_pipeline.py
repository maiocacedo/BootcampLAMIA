# Local: MATERIAL_DO_CURSO_airflow-materials\airflow-section-3\mnt\airflow\dags\ACOMPANHAMENTO_forex_data_pipeline.py

from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.http.sensors.http import HttpSensor
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.hive_operator import HiveOperator
from airflow.operators.email_operator import EmailOperator
from airflow.operators.slack_operator import SlackAPIPostOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator

from datetime import datetime, timedelta

import csv
import requests
import json

# Definindo a função para baixar as taxas de câmbio do Forex
def download_rates():
    with open('/usr/local/airflow/dags/files/forex_currencies.csv') as forex_currencies: # Caminho do arquivo CSV
        reader = csv.DictReader(forex_currencies, delimiter=';') # Lendo o arquivo CSV
        for row in reader: # Iterando sobre cada linha do arquivo
            base = row['base'] # Moeda base
            with_pairs = row['with_pairs'].split(' ') # Moedas com as quais a base será comparada
            indata = requests.get('https://api.exchangeratesapi.io/latest?base=' + base).json() # Requisição à API do Forex
            outdata = {'base': base, 'rates': {}, 'last_update': indata['date']} # Estrutura de dados para armazenar os resultados
            for pair in with_pairs:
                outdata['rates'][pair] = indata['rates'][pair] # Adicionando as taxas de câmbio ao dicionário
            with open('/usr/local/airflow/dags/files/forex_rates.json', 'a') as outfile: # Caminho do arquivo JSON, arquivo de saida
                json.dump(outdata, outfile)
                outfile.write('\n')
                
API_KEY = 'c0a3cba72ba75f0b30fc0e68591833ed' # Chave de API para acessar os dados do Forex

# Definindo os argumentos padrão para a posterior definição da DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 1, 1), # data de início
    'depends_on_past': False, # Não depende da execução passada
    'email_on_failure': False, # Não envia e-mail em caso de falha
    'email_on_retry': False, # Não envia e-mail em caso de retentativa
    'email' : 'emailbrabo@superemailinsano.com', # E-mail para envio de mensagens
    'retries': 1, # Número de retentativas
    'retry_delay': timedelta(minutes=5), # Intervalo entre as retentativas
}

# Definindo a DAG
with DAG('forex_data_pipeline',
         schedule_interval='@daily', # Intervalo de execução: diário
         default_args=default_args, # Argumentos padrão
         catchup=False # Não executa tarefas em atraso
         ) as dag: 
    
    # HttpSensor para verificar a disponibilidade dos dados do Forex
    is_forex_data_available = HttpSensor(
        task_id='is_forex_data_available',
        method='GET', # Método HTTP
        http_conn_id='forex_api', # Conexão com a API do Forex
        endpoint=f'/latest?access_key={API_KEY}', # Endpoint da API
        response_check=lambda response: "rates" in response.text, # Verifica se a resposta contém "rates"
        poke_interval=5, # Intervalo entre as verificações
        timeout=20, # Tempo máximo de espera
    )
    
    # FileSensor para verificar a disponibilidade do arquivo de moedas do Forex
    is_forex_currencies_file_available = FileSensor(
        task_id="is_forex_currencies_file_available", # ID da tarefa
        fs_conn_id="forex_path", # Conexão com o sistema de arquivos
        filepath="forex_currencies.csv", # Caminho do arquivo
        poke_interval=5, # Intervalo entre as verificações
        timeout=20 # Tempo máximo de espera
    )
    
    # PythonOperator para baixar os dados do Forex
    downloading_rates = PythonOperator(
            task_id="downloading_rates", # ID da tarefa
            python_callable=download_rates # Função a ser chamada
    )
    
    # BashOperator para salvar os dados do Forex no HDFS
    saving_rates = BashOperator(
        task_id="saving_rates", # ID da tarefa
        bash_command=""" 
            hdfs dfs -mkdir -p /forex && \
            hdfs dfs -put -f $AIRFLOW_HOME/dags/files/forex_rates.json /forex
            """ # Comando bash para criar diretório e salvar arquivo no HDFS
    )
    
    # SparkSubmitOperator para processar os dados do Forex
    creating_forex_rates_table = HiveOperator(
        task_id="creating_forex_rates_table", # ID da tarefa
        hive_cli_conn_id="hive_conn", # Conexão com o Hive
        hql="""
            CREATE EXTERNAL TABLE IF NOT EXISTS forex_rates(
                base STRING,
                last_update DATE,
                eur DOUBLE,
                usd DOUBLE,
                nzd DOUBLE,
                gbp DOUBLE,
                jpy DOUBLE,
                cad DOUBLE
                )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """ # Comando Hive para criar a tabela externa
    )
    
    # SparkSubmitOperator para processar os dados do Forex
    forex_processing = SparkSubmitOperator(
        task_id="forex_processing", # ID da tarefa
        conn_id="spark_conn", # Conexão com o Spark
        application="/usr/local/airflow/dags/scripts/forex_processing.py", # Caminho do script de processamento
        verbose=False # Não exibe logs detalhados
    )

    # Definindo a ordem de execução das tarefas
    sending_email_notification = EmailOperator(
            task_id="sending_email", # ID da tarefa
            to="airflow_course@yopmail.com", # E-mail do destinatário
            subject="forex_data_pipeline", # Assunto do e-mail
            html_content="""
                <h3>forex_data_pipeline succeeded</h3>
            """ # Conteúdo HTML do e-mail
            )
    
    # SlackAPIPostOperator para enviar notificações para o Slack
    sending_slack_notification = SlackAPIPostOperator(
        task_id="sending_slack", # ID da tarefa
        token="xoxp-753801195270-740121926339-751642514144-8391b800988bed43247926b03742459e", # Token de autenticação do Slack
        slack_conn_id="slack_conn", # Conexão com o Slack
        username="airflow", # Nome de usuário do Slack
        text="DAG forex_data_pipeline: DONE", # Texto da mensagem
        channel="#airflow-exploit" # Canal do Slack onde a mensagem será enviada
    )
    
    # Definindo as dependencias 
    is_forex_data_available >> is_forex_currencies_file_available >> downloading_rates >> saving_rates 
    saving_rates >> creating_forex_rates_table >> forex_processing 
    forex_processing >> sending_email_notification >> sending_slack_notification
