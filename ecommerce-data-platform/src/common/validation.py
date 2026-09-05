from pathlib import Path

import pandas as pd


EXPECTED_COLUMNS = {
    "customers": {
        "customer_id",
        "customer_name",
        "email",
        "created_at",
        "region",
        "segment",
        "status",
    },
    "products": {
        "product_id",
        "product_name",
        "category",
        "price",
        "cost",
        "active_flag",
    },
    "orders": {
        "order_id",
        "customer_id",
        "order_ts",
        "status",
        "channel",
    },
    "order_items": {
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
        "discount",
    },
    "payments": {
        "payment_id",
        "order_id",
        "amount",
        "payment_method",
        "payment_status",
        "payment_ts",
    },
    "shipments": {
        "shipment_id",
        "order_id",
        "shipped_at",
        "delivered_at",
        "carrier",
    },
    "returns": {
        "return_id",
        "order_id",
        "returned_at",
        "return_amount",
        "return_reason",
    },
    "inventory": {
        "product_id",
        "snapshot_ts",
        "quantity_on_hand",
        "reorder_point",
    },
    "web_events": {
        "event_id",
        "session_id",
        "event_type",
        "product_id",
        "traffic_source",
        "event_ts",
    },
}


REQUIRED_FIELDS = {
    "customers": {
        "customer_id",
        "customer_name",
        "email",
        "created_at",
    },
    "products": {
        "product_id",
        "product_name",
        "price",
        "cost",
    },
    "orders": {
        "order_id",
        "customer_id",
        "order_ts",
        "status",
    },
    "order_items": {
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
    },
    "payments": {
        "payment_id",
        "order_id",
        "payment_status",
        "payment_ts",
    },
    "shipments": {
        "shipment_id",
        "order_id",
        "shipped_at",
    },
    "returns": {
        "return_id",
        "order_id",
        "returned_at",
        "return_amount",
    },
    "inventory": {
        "product_id",
        "snapshot_ts",
        "quantity_on_hand",
    },
    "web_events": {
        "event_id",
        "session_id",
        "event_type",
        "traffic_source",
        "event_ts",
    },
}


def validate_columns(
    df: pd.DataFrame,
    dataset_name: str,
) -> list[str]:

    errors = []

    expected = EXPECTED_COLUMNS.get(
        dataset_name
    )

    if expected is None:
        errors.append(
            f"Unknown dataset: {dataset_name}"
        )
        return errors

    actual = set(df.columns)

    missing_columns = expected - actual
    unexpected_columns = actual - expected

    if missing_columns:
        errors.append(
            f"Missing columns: "
            f"{sorted(missing_columns)}"
        )

    if unexpected_columns:
        errors.append(
            f"Unexpected columns: "
            f"{sorted(unexpected_columns)}"
        )

    return errors


def validate_not_empty(
    df: pd.DataFrame,
) -> list[str]:

    if df.empty:
        return [
            "Dataset contains no records."
        ]

    return []


def validate_required_fields(
    df: pd.DataFrame,
    dataset_name: str,
) -> list[str]:

    errors = []

    required_fields = REQUIRED_FIELDS.get(
        dataset_name,
        set(),
    )

    for field in required_fields:

        if field not in df.columns:
            continue

        null_count = df[field].isna().sum()

        if null_count > 0:
            errors.append(
                f"Required field '{field}' "
                f"contains {null_count} null value(s)."
            )

    return errors


def validate_file_exists(
    file_path: Path,
) -> list[str]:

    if not file_path.exists():
        return [
            f"File does not exist: {file_path}"
        ]

    return []


def validate_dataset(
    df: pd.DataFrame,
    dataset_name: str,
) -> list[str]:

    errors = []

    errors.extend(
        validate_not_empty(df)
    )

    errors.extend(
        validate_columns(
            df,
            dataset_name,
        )
    )

    errors.extend(
        validate_required_fields(
            df,
            dataset_name,
        )
    )

    return errors