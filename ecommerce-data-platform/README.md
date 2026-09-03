# Northstar Commerce Data Platform

An end-to-end data engineering and analytics engineering portfolio project that simulates a modern e-commerce data platform.

## Project Goals

This project demonstrates:

- Python-based source data generation
- AWS S3 raw data lake ingestion
- Snowflake cloud data warehousing
- Apache Airflow orchestration
- dbt transformation and dimensional modeling
- Incremental data processing
- Data quality testing and quarantine workflows
- CI/CD with GitHub Actions
- Observability and audit logging
- Power BI analytics

## Architecture

Python Source Data
        |
        v
AWS S3 Raw Data Lake
        |
        v
Snowflake RAW
        |
        v
dbt
Staging -> Intermediate -> Dimensions/Facts -> Marts
        |
        v
Power BI

Apache Airflow orchestrates the pipeline.

## Status

Project currently under development.