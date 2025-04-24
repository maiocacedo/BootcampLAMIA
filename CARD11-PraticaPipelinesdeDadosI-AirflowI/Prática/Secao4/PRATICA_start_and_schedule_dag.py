# MATERIAL_DO_CURSO_airflow-materials\airflow-section-4\mnt\airflow\dags
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

from datetime import datetime, timedelta

# Definindo os argumentos padrão, start_date como 29 de março de 2019, 01:00 UTC
default_args = {
    'start_date': datetime(2025, 2, 29, 2), # start_date UTC
    'owner': 'Airflow'
}

# Definindo uma dag com schedule_interval semanal, toda sexta-feira às 03:00 UTC
with DAG(dag_id='start_and_schedule_dag', schedule_interval="0 3 * * 5", default_args=default_args) as dag:
    
    # Task 1
    dummy_task_1 = DummyOperator(task_id='dummy_task_1')
    
    # Task 2
    dummy_task_2 = DummyOperator(task_id='dummy_task_2')
    
    dummy_task_3 = DummyOperator(task_id='dummy_task_2')
    
    # Dependências
    dummy_task_1 >> dummy_task_2 >> dummy_task_3
    
    # Dependências
    dummy_task_1 >> dummy_task_3
    
    # Inicia a DAG    
    run_dates = dag.get_run_dates(start_date=dag.start_date)
    next_execution_date = run_dates[-1] if len(run_dates) != 0 else None
    print('[DAG:start_and_schedule_dag] start_date: {0} - schedule_interval: {1} - Last execution_date: {2} - next execution_date {3} in UTC'.format(
        dag.default_args['start_date'], 
        dag._schedule_interval, 
        dag.latest_execution_date, 
        next_execution_date
        ))