from pathlib import Path

import pandas as pd

from src.common.config import RAW_DATA_DIR
from src.common.manifest import (
    build_manifest,
    build_manifest_record,
    save_manifest,
)
from src.common.validation import validate_dataset


RUN_DATE = "2026-08-31"


def get_datasets(
    run_date: str,
) -> dict[str, Path]:

    return {
        "customers": RAW_DATA_DIR / "customers.csv",
        "products": RAW_DATA_DIR / "products.csv",
        "orders": RAW_DATA_DIR / "orders.json",
        "order_items": RAW_DATA_DIR / "order_items.json",
        "payments": RAW_DATA_DIR / "payments.csv",
        "shipments": RAW_DATA_DIR / "shipments.csv",
        "returns": RAW_DATA_DIR / "returns.csv",
        "inventory": (
            RAW_DATA_DIR
            / "inventory"
            / f"snapshot_date={run_date}"
            / f"inventory_{run_date}.csv"
        ),
        "web_events": (
            RAW_DATA_DIR
            / "web_events"
            / f"event_date={run_date}"
            / f"web_events_{run_date}.json"
        ),
    }


def read_dataset(
    file_path: Path,
) -> pd.DataFrame:

    if file_path.suffix == ".csv":
        return pd.read_csv(file_path)

    if file_path.suffix == ".json":
        return pd.read_json(
            file_path,
            lines=True,
        )

    raise ValueError(
        f"Unsupported file type: {file_path.suffix}"
    )


def validate_batch(
    run_date: str = RUN_DATE,
) -> dict:

    manifest_records = []

    print(
        f"Validating batch for {run_date}"
    )
    print("-" * 60)

    for dataset_name, file_path in get_datasets(run_date).items():

        if not file_path.exists():

            errors = [
                f"File does not exist: {file_path}"
            ]

            manifest_records.append(
                {
                    "dataset_name": dataset_name,
                    "file_name": file_path.name,
                    "file_path": str(file_path),
                    "row_count": 0,
                    "file_size_bytes": 0,
                    "checksum_sha256": None,
                    "validation_status": "invalid",
                    "validation_errors": errors,
                }
            )

            print(
                f"{dataset_name:<15} "
                f"INVALID - file missing"
            )

            continue

        df = read_dataset(
            file_path
        )

        validation_errors = validate_dataset(
            df,
            dataset_name,
        )

        manifest_record = build_manifest_record(
            dataset_name=dataset_name,
            file_path=file_path,
            row_count=len(df),
            validation_errors=validation_errors,
        )

        manifest_records.append(
            manifest_record
        )

        status = manifest_record[
            "validation_status"
        ].upper()

        print(
            f"{dataset_name:<15} "
            f"{status:<8} "
            f"{len(df):>8,} rows"
        )

        if validation_errors:

            for error in validation_errors:
                print(
                    f"    - {error}"
                )

    manifest = build_manifest(
        records=manifest_records,
        run_date=run_date,
    )

    manifest_path = (
        RAW_DATA_DIR
        / "manifests"
        / f"run_date={run_date}"
        / "manifest.json"
    )

    save_manifest(
        manifest,
        manifest_path,
    )

    print("-" * 60)
    print("Manifest saved to:")
    print(manifest_path)

    return manifest


if __name__ == "__main__":
    validate_batch()