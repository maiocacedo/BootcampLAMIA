# MATERIAL_DO_CURSO_airflow-materials\airflow-section-4\mnt\airflow\dags
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator 
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta

# Definição dos argumentos padrão do DAG
default_args = {
    'start_date': datetime(2019, 1, 1)
}

# Definição da função de processamento exemplo.
def process():
    return 'process'

# Definição do DAG
# O DAG é definido como um contexto gerenciado
with DAG(dag_id='tst_dag', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:
    
    task_1 = DummyOperator(task_id='task_1')

    task_2 = PythonOperator(task_id='task_2', python_callable=process)

    # Tasks dynamically generated 
    tasks = [DummyOperator(task_id='task_{0}'.format(t)) for t in range(3, 6)]

    task_6 = DummyOperator(task_id='task_6')

    task_1 >> task_2 >> tasks >> task_6 # Definindo a ordem de execução das tasks
        