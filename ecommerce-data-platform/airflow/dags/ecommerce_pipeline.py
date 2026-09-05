from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import (
    SQLExecuteQueryOperator,
)
from airflow.providers.standard.operators.bash import (
    BashOperator,
)
from src.generator.inject_bad_data import inject_bad_customer
from src.generator.generate_batch import generate_batch
from src.ingestion.validate_batch import (
    validate_batch,
    enforce_batch_quality,
)
from src.ingestion.s3_uploader import upload_batch


def optionally_inject_bad_data(
    run_date: str,
    inject_bad_data=False,
) -> None:

    should_inject = (
        inject_bad_data is True
        or str(inject_bad_data).lower() == "true"
    )

    if not should_inject:
        print("Bad-data injection disabled.")
        return

    print(
        f"Bad-data injection enabled for {run_date}."
    )

    inject_bad_customer(run_date)



with DAG(
    dag_id="ecommerce_pipeline",
    start_date=datetime(2026, 9, 1),
    schedule=None,
    catchup=False,
    template_searchpath=["/opt/airflow/sql"],
    params={
        "run_date": "2026-09-04",
        "inject_bad_data": False,
    },
    tags=["portfolio", "ecommerce"],
) as dag:

    # ---------------------------------------------------------
    # 1. Generate source data
    # ---------------------------------------------------------

    generate = PythonOperator(
        task_id="generate_data",
        python_callable=generate_batch,
        op_kwargs={
            "run_date": "{{ params.run_date }}",
        },
    )

    # ---------------------------------------------------------
    # 1.5.  Inject Bad Data
    # ---------------------------------------------------------

    inject_bad_data = PythonOperator(
    task_id="inject_bad_data",
    python_callable=optionally_inject_bad_data,
    op_kwargs={
        "run_date": "{{ params.run_date }}",
        "inject_bad_data": "{{ params.inject_bad_data }}",
    },
)

    # ---------------------------------------------------------
    # 2. Validate batch and create manifest
    # ---------------------------------------------------------

    validate = PythonOperator(
        task_id="validate_batch",
        python_callable=validate_batch,
        op_kwargs={
            "run_date": "{{ params.run_date }}",
        },
    )

    # ---------------------------------------------------------
    # 3. Upload validated batch to S3 and Quality Gate
    # ---------------------------------------------------------

    upload = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_batch,
        op_kwargs={
            "run_date": "{{ params.run_date }}",
        },
    )

    quality_gate = PythonOperator(
    task_id="quality_gate",
    python_callable=enforce_batch_quality,
    op_kwargs={
        "run_date": "{{ params.run_date }}",
    },
)
    # ---------------------------------------------------------
    # 4. Load customers into Snowflake RAW
    # ---------------------------------------------------------

    load_customers = SQLExecuteQueryOperator(
        task_id="load_customers",
        conn_id="snowflake_default",
        sql="raw_tables/02_load_customers.sql",
        split_statements=True,
    )

    # ---------------------------------------------------------
    # 5. Load CSV datasets into Snowflake RAW
    # ---------------------------------------------------------

    load_csv_tables = SQLExecuteQueryOperator(
        task_id="load_csv_tables",
        conn_id="snowflake_default",
        sql="raw_tables/03_load_csv_tables.sql",
        split_statements=True,
    )

    # ---------------------------------------------------------
    # 6. Load JSON datasets into Snowflake RAW
    # ---------------------------------------------------------

    load_json_tables = SQLExecuteQueryOperator(
        task_id="load_json_tables",
        conn_id="snowflake_default",
        sql="raw_tables/04_load_json_tables.sql",
        split_statements=True,
    )

    # ---------------------------------------------------------
    # 7. Refresh pipeline audit metadata
    # ---------------------------------------------------------

    refresh_audit = SQLExecuteQueryOperator(
        task_id="refresh_pipeline_audit",
        conn_id="snowflake_default",
        sql="audit_tables/04_refresh_pipeline_audit.sql",
        split_statements=True,
    )

    # ---------------------------------------------------------
    # 8. Build and test dbt models
    # ---------------------------------------------------------

    run_dbt_build = BashOperator(
        task_id="run_dbt_build",
        bash_command="""
            dbt build \
            --project-dir /opt/airflow/dbt/ecommerce_analytics \
            --profiles-dir /opt/airflow/.dbt
        """,
    )

    # ---------------------------------------------------------
    # Pipeline dependency chain
    # ---------------------------------------------------------

    (
        generate
        >> inject_bad_data
        >> validate
        >> upload
        >> quality_gate
        >> load_customers
        >> load_csv_tables
        >> load_json_tables
        >> refresh_audit
        >> run_dbt_build
    )