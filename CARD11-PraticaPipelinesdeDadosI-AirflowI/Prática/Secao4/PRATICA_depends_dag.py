# MATERIAL_DO_CURSO_airflow-materials\airflow-section-4\mnt\airflow\dags
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from datetime import datetime, timedelta

default_args = {
    'start_date': datetime(2025, 1, 1),  # Data de início da DAG
    'owner': 'Airflow'  # Proprietário da DAG
}

# Tarefa dummy para representar uma tarefa que não faz nada

def second_task():
    print('Olá do segundo task')  # Mensagem de saída da segunda tarefa
    # raise ValueError('Isso transformará a tarefa Python em estado de falha')

def third_task():
    print('Olá da terceira task')  # Mensagem de saída da terceira tarefa
    # raise ValueError('Isso transformará a tarefa Python em estado de falha')

with DAG(dag_id='depends_task', schedule_interval="3 4 * * *", default_args=default_args) as dag:
    
    # Task
    # 1
    bash_task_1 = BashOperator(
        task_id='bash_task_1', 
        bash_command="echo 'primeira tarefa'",  # Comando Bash que será executado
    )
    
    # Task 2
    python_task_2 = PythonOperator(
        task_id='python_task_2', 
        python_callable=second_task, 
        wait_for_downstream=True  # Faz esta tarefa esperar a conclusão da tarefa anterior antes de executar
    )

    # Task 3
    python_task_3 = PythonOperator(
        task_id='python_task_3', 
        python_callable=third_task, 
        wait_for_downstream=True  # Faz esta tarefa esperar a conclusão da tarefa anterior antes de executar
    )

    # Definição da ordem de execução das tarefas
    bash_task_1 >> python_task_2 >> python_task_3