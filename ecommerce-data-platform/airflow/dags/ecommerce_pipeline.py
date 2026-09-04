from datetime import datetime
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow import DAG
from airflow.operators.python import PythonOperator

from src.ingestion.validate_batch import validate_batch
from src.ingestion.s3_uploader import upload_batch


with DAG(
    dag_id="ecommerce_pipeline",
    start_date=datetime(2026, 9, 1),
    schedule=None,
    catchup=False,
    template_searchpath=["/opt/airflow/sql"],
    tags=["portfolio", "ecommerce"],
) as dag:

    validate = PythonOperator(
        task_id="validate_batch",
        python_callable=validate_batch,
    )

    upload = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_batch,
    )
    load_customers = SQLExecuteQueryOperator(
        task_id="load_customers",
        conn_id="snowflake_default",
        sql="raw_tables/02_load_customers.sql",
        split_statements=True,
    )

    load_csv_tables = SQLExecuteQueryOperator(
        task_id="load_csv_tables",
        conn_id="snowflake_default",
        sql="raw_tables/03_load_csv_tables.sql",
        split_statements=True,
    )

    load_json_tables = SQLExecuteQueryOperator(
        task_id="load_json_tables",
        conn_id="snowflake_default",
        sql="raw_tables/04_load_json_tables.sql",
        split_statements=True,
    )

    refresh_audit = SQLExecuteQueryOperator(
        task_id="refresh_pipeline_audit",
        conn_id="snowflake_default",
        sql="audit_tables/04_refresh_pipeline_audit.sql",
        split_statements=True,
    )



    validate >> upload >> load_customers >> load_csv_tables >> load_json_tables >> refresh_audit