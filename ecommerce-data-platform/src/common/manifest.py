import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def calculate_checksum(
    file_path: Path,
) -> str:

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        for chunk in iter(
            lambda: file.read(8192),
            b"",
        ):
            sha256.update(chunk)

    return sha256.hexdigest()


def build_manifest_record(
    dataset_name: str,
    file_path: Path,
    row_count: int,
    validation_errors: list[str],
) -> dict:

    return {
        "dataset_name": dataset_name,
        "file_name": file_path.name,
        "file_path": str(file_path),
        "row_count": row_count,
        "file_size_bytes": file_path.stat().st_size,
        "checksum_sha256": calculate_checksum(
            file_path
        ),
        "validation_status": (
            "valid"
            if not validation_errors
            else "invalid"
        ),
        "validation_errors": validation_errors,
    }


def build_manifest(
    records: list[dict],
    run_date: str,
) -> dict:

    return {
        "run_date": run_date,
        "generated_at_utc": (
            datetime.now(
                timezone.utc
            ).isoformat()
        ),
        "dataset_count": len(records),
        "datasets": records,
    }


def save_manifest(
    manifest: dict,
    output_path: Path,
) -> None:

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            manifest,
            file,
            indent=4,
        )