# MATERIAL_DO_CURSO_airflow-materials\airflow-section-4\mnt\airflow\dags
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta

# Função que será executada pela primeira tarefa
def first_task():
    print("Hello from first task")  # Mensagem de saída da primeira tarefa

# Função que será executada pela segunda tarefa
def second_task():
    print("Hello from second task")  # Mensagem de saída da segunda tarefa

# Função que será executada pela terceira tarefa
def third_task():
    print("Hello from third task")  # Mensagem de saída da terceira tarefa

# Argumentos padrão para a DAG
default_args = {
    'start_date': datetime(2019, 1, 1),  # Data de início da DAG
    'owner': 'Airflow'  # Proprietário da DAG
}

# Definição da DAG
with DAG(dag_id='packaged_dag', schedule_interval="0 0 * * *", default_args=default_args) as dag:

    # Tarefa 1
    python_task_1 = PythonOperator(
        task_id='python_task_1',  # Identificador da tarefa
        python_callable=first_task  # Função Python que será executada
    )

    # Tarefa 2
    python_task_2 = PythonOperator(
        task_id='python_task_2',  # Identificador da tarefa
        python_callable=second_task  # Função Python que será executada
    )

    # Tarefa 3
    python_task_3 = PythonOperator(
        task_id='python_task_3',  # Identificador da tarefa
        python_callable=third_task  # Função Python que será executada
    )

    # Definição da ordem de execução das tarefas
    python_task_1 >> python_task_2 >> python_task_3  # python_task_1 executa antes de python_task_2, que executa antes de python_task_3