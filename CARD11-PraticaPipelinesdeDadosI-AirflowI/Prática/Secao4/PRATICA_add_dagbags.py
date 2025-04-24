# MATERIAL_DO_CURSO_airflow-materials\airflow-section-4\mnt\airflow\dags
# Script to add new DAGs folders using 
# the class DagBag
# Paths must be absolute
import os
from airflow.models import DagBag

# Definindo os diretórios onde estão os DAGs
# que queremos carregar.
dags_dirs = [
                '/usr/local/airflow/project_a', 
                '/usr/local/airflow/project_b'
            ]
# A DagBag é uma classe que carrega DAGs de um diretório
# ou de um arquivo específico.
for dir in dags_dirs:
   dag_bag = DagBag(os.path.expanduser(dir)) # Carrega as DAGs do diretório
   
   # Verifica se houve algum erro
   if dag_bag.import_errors:
      print(f"Erro ao carregar DAGs do diretório {dir}: {dag_bag.import_errors}")
   else:
      print(f"DAGs carregadas com sucesso do diretório {dir}: {list(dag_bag.dags.keys())}")
      
   # Adiciona as DAGs carregadas ao globals()
   if dag_bag:
      for dag_id, dag in dag_bag.dags.items():
         globals()[dag_id] = dag