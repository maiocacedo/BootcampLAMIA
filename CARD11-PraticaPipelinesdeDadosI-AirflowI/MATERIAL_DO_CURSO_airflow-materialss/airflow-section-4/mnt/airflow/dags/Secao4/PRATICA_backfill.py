# MATERIAL_DO_CURSO_airflow-materials\airflow-section-4\mnt\airflow\dags
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

from datetime import datetime, timedelta

# Definindo os argumentos padrão
default_args = {
    'start_date': datetime(2025, 1, 1),
    'owner': 'Airflow'
}

# Definindo a DAG
with DAG(dag_id='backfill', schedule_interval="0 0 * * *", default_args=default_args, catchup=True) as dag:
    
    # Task 1
    bash_task_1 = BashOperator(task_id='bash_task_1', bash_command="echo 'first task'") # task bash_task_1
    
    # Task 2
    bash_task_2 = BashOperator(task_id='bash_task_2', bash_command="echo 'second task'") # task bash_task_2

    bash_task_1 >> bash_task_2 # Definindo a ordem de execução das tasks