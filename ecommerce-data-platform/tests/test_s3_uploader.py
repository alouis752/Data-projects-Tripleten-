from pathlib import Path

from src.ingestion.s3_uploader import (
    build_manifest_s3_key,
    build_quarantine_s3_key,
    build_s3_key,
)

def test_build_s3_key():

    file_path = Path(
        "customers.csv"
    )

    result = build_s3_key(
        dataset_name="customers",
        run_date="2026-08-31",
        file_path=file_path,
    )

    assert result == (
        "raw/customers/"
        "run_date=2026-08-31/"
        "customers.csv"
    )

def test_build_manifest_s3_key():

    result = build_manifest_s3_key(
        run_date="2026-08-31",
    )

    assert result == (
        "manifests/"
        "run_date=2026-08-31/"
        "manifest.json"
    )

def test_build_quarantine_s3_key():

    file_path = Path(
        "customers.csv"
    )

    result = build_quarantine_s3_key(
        dataset_name="customers",
        run_date="2026-08-31",
        file_path=file_path,
    )

    assert result == (
        "quarantine/customers/"
        "run_date=2026-08-31/"
        "customers.csv"
    )