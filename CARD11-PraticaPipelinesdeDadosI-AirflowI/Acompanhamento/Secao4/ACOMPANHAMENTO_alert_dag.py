# MATERIAL_DO_CURSO_airflow-materials\airflow-section-4\mnt\airflow\dags
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

from datetime import datetime, timedelta

# Definindo os argumentos padrão do DAG
default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow'
}

# Definindo o DAG
with DAG(dag_id='alert_dag', schedule_interval="0 0 * * *", default_args=default_args, catchup=True) as dag:
    
    # Task 1
    t1 = BashOperator(task_id='t1', bash_command="exit 1") # simulando um erro
    
    # Task 2
    t2 = BashOperator(task_id='t2', bash_command="echo 'second task'") # task de sucesso

    t1 >> t2