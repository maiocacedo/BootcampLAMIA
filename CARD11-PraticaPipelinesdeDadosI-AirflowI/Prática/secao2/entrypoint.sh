#!/usr/bin/env bash

# Inicializa o metastore
airflow db init

# Executa o scheduler em segundo plano
airflow scheduler &> /dev/null &

# Executa o servidor web em primeiro plano (para os logs do Docker)
exec airflow webserver