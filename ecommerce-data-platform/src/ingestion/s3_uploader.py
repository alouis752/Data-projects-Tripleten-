from pathlib import Path
import json

import boto3
from botocore.exceptions import ClientError

from src.common.manifest import calculate_checksum


S3_BUCKET_NAME = "ecommerce-data-platform-2026-752"
AWS_REGION = "us-east-2"


def get_s3_client():
    return boto3.client(
        "s3",
        region_name=AWS_REGION,
    )


def build_s3_key(
    dataset_name: str,
    run_date: str,
    file_path: Path,
) -> str:

    return (
        f"raw/{dataset_name}/"
        f"run_date={run_date}/"
        f"{file_path.name}"
    )


def build_quarantine_s3_key(
    dataset_name: str,
    run_date: str,
    file_path: Path,
) -> str:

    return (
        f"quarantine/{dataset_name}/"
        f"run_date={run_date}/"
        f"{file_path.name}"
    )


def build_manifest_s3_key(
    run_date: str,
) -> str:

    return (
        f"manifests/"
        f"run_date={run_date}/"
        f"manifest.json"
    )


def get_existing_object_checksum(
    s3_client,
    bucket_name: str,
    s3_key: str,
) -> str | None:

    try:
        response = s3_client.head_object(
            Bucket=bucket_name,
            Key=s3_key,
        )

        return response.get(
            "Metadata",
            {},
        ).get(
            "checksum_sha256"
        )

    except ClientError as error:

        error_code = error.response[
            "Error"
        ]["Code"]

        if error_code in {
            "404",
            "NoSuchKey",
            "NotFound",
        }:
            return None

        raise


def upload_file_idempotent(
    s3_client,
    file_path: Path,
    bucket_name: str,
    s3_key: str,
) -> str:

    local_checksum = calculate_checksum(
        file_path
    )

    existing_checksum = (
        get_existing_object_checksum(
            s3_client=s3_client,
            bucket_name=bucket_name,
            s3_key=s3_key,
        )
    )

    if existing_checksum is None:

        s3_client.upload_file(
            Filename=str(file_path),
            Bucket=bucket_name,
            Key=s3_key,
            ExtraArgs={
                "Metadata": {
                    "checksum_sha256": local_checksum
                }
            },
        )

        return "uploaded"

    if existing_checksum == local_checksum:
        return "skipped"

    raise ValueError(
        "S3 object already exists "
        "with different content: "
        f"s3://{bucket_name}/{s3_key}"
    )


def upload_validated_batch(
    manifest_path: Path,
    bucket_name: str = S3_BUCKET_NAME,
) -> dict:

    with open(
        manifest_path,
        "r",
        encoding="utf-8",
    ) as file:
        manifest = json.load(file)

    run_date = manifest["run_date"]

    s3_client = get_s3_client()

    results = []

    for dataset in manifest["datasets"]:

        dataset_name = dataset["dataset_name"]
        validation_status = dataset[
            "validation_status"
        ]

        if validation_status != "valid":

            file_path = Path(
                dataset["file_path"]
            )

            if file_path.exists():

                quarantine_s3_key = (
                    build_quarantine_s3_key(
                        dataset_name=dataset_name,
                        run_date=run_date,
                        file_path=file_path,
                    )
                )

                quarantine_status = (
                    upload_file_idempotent(
                        s3_client=s3_client,
                        file_path=file_path,
                        bucket_name=bucket_name,
                        s3_key=quarantine_s3_key,
                    )
                )

                results.append(
                    {
                        "dataset_name": dataset_name,
                        "status": quarantine_status,
                        "destination": "quarantine",
                        "s3_key": quarantine_s3_key,
                        "validation_errors": dataset[
                            "validation_errors"
                        ],
                    }
                )

                print(
                    f"{dataset_name:<15} "
                    f"{'QUARANTINED':<12} "
                    f"{quarantine_s3_key}"
                )

            else:

                results.append(
                    {
                        "dataset_name": dataset_name,
                        "status": "not_uploaded",
                        "destination": "none",
                        "reason": "file_missing",
                        "validation_errors": dataset[
                            "validation_errors"
                        ],
                    }
                )

                print(
                    f"{dataset_name:<15} "
                    f"{'NOT UPLOADED':<12} "
                    "file missing"
                )

            continue

        file_path = Path(
            dataset["file_path"]
        )

        s3_key = build_s3_key(
            dataset_name=dataset_name,
            run_date=run_date,
            file_path=file_path,
        )

        upload_status = upload_file_idempotent(
            s3_client=s3_client,
            file_path=file_path,
            bucket_name=bucket_name,
            s3_key=s3_key,
        )

        results.append(
            {
                "dataset_name": dataset_name,
                "status": upload_status,
                "destination": "raw",
                "s3_key": s3_key,
            }
        )

        print(
            f"{dataset_name:<15} "
            f"{upload_status.upper():<10} "
            f"{s3_key}"
        )

    manifest_s3_key = build_manifest_s3_key(
        run_date=run_date,
    )

    manifest_upload_status = (
        upload_file_idempotent(
            s3_client=s3_client,
            file_path=manifest_path,
            bucket_name=bucket_name,
            s3_key=manifest_s3_key,
        )
    )

    print(
        f"{'manifest':<15} "
        f"{manifest_upload_status.upper():<10} "
        f"{manifest_s3_key}"
    )

    return {
        "run_date": run_date,
        "bucket_name": bucket_name,
        "results": results,
        "manifest": {
            "status": manifest_upload_status,
            "s3_key": manifest_s3_key,
        },
    }


if __name__ == "__main__":

    manifest_path = (
        Path("data")
        / "raw"
        / "manifests"
        / "run_date=2026-08-31"
        / "manifest.json"
    )

def upload_batch(
    run_date: str = "2026-08-31",
) -> dict:
    """
    Build the manifest path for a specific batch date
    and upload that validated batch to S3.

    This wrapper is useful because Airflow can call it
    directly without needing to manually construct a Path.
    """

    manifest_path = (
        Path("data")
        / "raw"
        / "manifests"
        / f"run_date={run_date}"
        / "manifest.json"
    )

    return upload_validated_batch(
        manifest_path=manifest_path
    )


def main():
    """
    Manual command-line entry point.
    """

    upload_batch()


if __name__ == "__main__":
    main()