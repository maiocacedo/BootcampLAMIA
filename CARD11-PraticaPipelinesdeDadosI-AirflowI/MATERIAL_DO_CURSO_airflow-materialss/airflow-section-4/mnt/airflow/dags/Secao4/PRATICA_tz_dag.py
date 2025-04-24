# MATERIAL_DO_CURSO_airflow-materials\airflow-section-4\mnt\airflow\dags
import pendulum
from airflow import DAG
from airflow.utils import timezone
from airflow.operators.dummy_operator import DummyOperator

from datetime import timedelta, datetime

# definindo a timezone local
local_tz = pendulum.timezone('America/Sao_Paulo') 

default_args = {
    'start_date': datetime(2025, 2, 29, 12), # '2019-03-29 12:00:00',
    'owner': 'Airflow'
}


# definindo a DAG
with DAG(dag_id='tz_dag', schedule_interval="5 4 * * 3", default_args=default_args) as dag: 
    dummy_task = DummyOperator(task_id='dummy_task') # task dummy_task
    
    run_dates = dag.get_run_dates(start_date=dag.start_date) # get_run_dates() retorna uma lista de datas
    next_execution_date = run_dates[-1] if len(run_dates) != 0 else None 
    
    # Exibindo informações sobre a DAG
    print('datetime from Python is Naive: {0}'.format(timezone.is_naive(datetime(2019, 9, 19)))) # impriminto datetime sem timezone
    print('datetime from Airflow is Aware: {0}'.format(timezone.is_naive(timezone.datetime(2019, 9, 19)) == False)) # imprimindo datetime com timezone
    print('[DAG:tz_dag] timezone: {0} - start_date: {1} - schedule_interval: {2} - Last execution_date: {3} - next execution_date {4} in UTC - next execution_date {5} in local time'.format(
        dag.timezone, 
        dag.default_args['start_date'], 
        dag._schedule_interval, 
        dag.latest_execution_date, 
        next_execution_date,
        local_tz.convert(next_execution_date) if next_execution_date is not None else None
        ))