import json

from src.common.manifest import (
    build_manifest,
    build_manifest_record,
    calculate_checksum,
    save_manifest,
)


def test_checksum_is_deterministic(
    tmp_path,
):

    file_path = (
        tmp_path
        / "test.csv"
    )

    file_path.write_text(
        "id,name\n1,test\n",
        encoding="utf-8",
    )

    checksum_one = calculate_checksum(
        file_path
    )

    checksum_two = calculate_checksum(
        file_path
    )

    assert (
        checksum_one
        == checksum_two
    )


def test_checksum_changes_when_file_changes(
    tmp_path,
):

    file_path = (
        tmp_path
        / "test.csv"
    )

    file_path.write_text(
        "id,name\n1,test\n",
        encoding="utf-8",
    )

    checksum_one = calculate_checksum(
        file_path
    )

    file_path.write_text(
        "id,name\n1,changed\n",
        encoding="utf-8",
    )

    checksum_two = calculate_checksum(
        file_path
    )

    assert (
        checksum_one
        != checksum_two
    )


def test_valid_manifest_record(
    tmp_path,
):

    file_path = (
        tmp_path
        / "customers.csv"
    )

    file_path.write_text(
        "customer_id\nCUST-000001\n",
        encoding="utf-8",
    )

    record = build_manifest_record(
        dataset_name="customers",
        file_path=file_path,
        row_count=1,
        validation_errors=[],
    )

    assert (
        record["dataset_name"]
        == "customers"
    )

    assert (
        record["row_count"]
        == 1
    )

    assert (
        record["validation_status"]
        == "valid"
    )

    assert (
        record["checksum_sha256"]
    )


def test_invalid_manifest_record(
    tmp_path,
):

    file_path = (
        tmp_path
        / "customers.csv"
    )

    file_path.write_text(
        "bad_column\nvalue\n",
        encoding="utf-8",
    )

    record = build_manifest_record(
        dataset_name="customers",
        file_path=file_path,
        row_count=1,
        validation_errors=[
            "Missing columns"
        ],
    )

    assert (
        record["validation_status"]
        == "invalid"
    )

    assert (
        len(
            record[
                "validation_errors"
            ]
        )
        == 1
    )


def test_build_manifest():

    records = [
        {
            "dataset_name": "customers",
        },
        {
            "dataset_name": "products",
        },
    ]

    manifest = build_manifest(
        records=records,
        run_date="2026-08-31",
    )

    assert (
        manifest["run_date"]
        == "2026-08-31"
    )

    assert (
        manifest["dataset_count"]
        == 2
    )


def test_save_manifest(
    tmp_path,
):

    manifest = {
        "run_date": "2026-08-31",
        "dataset_count": 0,
        "datasets": [],
    }

    output_path = (
        tmp_path
        / "manifest.json"
    )

    save_manifest(
        manifest,
        output_path,
    )

    assert output_path.exists()

    with open(
        output_path,
        "r",
        encoding="utf-8",
    ) as file:

        saved_manifest = json.load(
            file
        )

    assert (
        saved_manifest["run_date"]
        == "2026-08-31"
    )