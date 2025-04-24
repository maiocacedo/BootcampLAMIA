# Imagem base
FROM python:3.11
LABEL maintainer="MarcLamberti"

# Argumentos que podem ser definidos com o comando docker build
ARG AIRFLOW_VERSION=2.9.0
ARG AIRFLOW_HOME=/usr/local/airflow

# Exporta a variável de ambiente AIRFLOW_HOME onde o Airflow será instalado
ENV AIRFLOW_HOME=${AIRFLOW_HOME}

# Instala dependências e ferramentas
RUN apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq --no-install-recommends \ 
    wget \
    libczmq-dev \
    curl \
    libssl-dev \
    git \
    inetutils-telnet \
    bind9utils freetds-dev \
    libkrb5-dev \
    libsasl2-dev \
    libffi-dev libpq-dev \
    freetds-bin build-essential \
    default-libmysqlclient-dev \
    apt-utils \
    rsync \
    zip \
    unzip \
    gcc \
    vim \
    locales \
    && apt-get clean

COPY ./requirements-python3.5.txt /requirements-python3.5.txt

# Atualiza o pip
# Cria o usuário airflow
# Instala o Apache Airflow com subpacotes
RUN pip install --upgrade pip && \
    useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow && \
    pip install apache-airflow[crypto,celery,postgres,hive,mysql,ssh,docker,hdfs,kubernetes,redis,rabbitmq,slack]==${AIRFLOW_VERSION} --constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.9.0/constraints-3.11.txt

# Copia o arquivo entrypoint.sh do host para o container (no caminho AIRFLOW_HOME)
COPY ./entrypoint.sh ./entrypoint.sh

# Define o arquivo entrypoint.sh como executável
RUN chmod +x ./entrypoint.sh

# Define o proprietário dos arquivos em AIRFLOW_HOME como o usuário airflow
RUN chown -R airflow: ${AIRFLOW_HOME}

# Define o nome de usuário a ser usado
USER airflow

# Define o diretório de trabalho (é como um comando cd dentro do container)
WORKDIR ${AIRFLOW_HOME}

# Cria a pasta dags que conterá os DAGs
RUN mkdir dags

# Expõe as portas (apenas para indicar que este container precisa mapear a porta)
EXPOSE 8080

# Executa o entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]


