import pandas as pd

from src.common.validation import (
    validate_columns,
    validate_dataset,
    validate_not_empty,
)


def test_valid_customer_columns_pass():

    df = pd.DataFrame(
        {
            "customer_id": ["CUST-000001"],
            "customer_name": ["Test Customer"],
            "email": ["test@example.com"],
            "created_at": ["2026-01-01"],
            "region": ["Northeast"],
            "segment": ["Consumer"],
            "status": ["active"],
        }
    )

    errors = validate_columns(
        df,
        "customers",
    )

    assert errors == []


def test_missing_column_fails():

    df = pd.DataFrame(
        {
            "customer_id": ["CUST-000001"],
            "customer_name": ["Test Customer"],
        }
    )

    errors = validate_columns(
        df,
        "customers",
    )

    assert len(errors) > 0

    assert "Missing columns" in errors[0]


def test_unexpected_column_fails():

    df = pd.DataFrame(
        {
            "customer_id": ["CUST-000001"],
            "customer_name": ["Test Customer"],
            "email": ["test@example.com"],
            "created_at": ["2026-01-01"],
            "region": ["Northeast"],
            "segment": ["Consumer"],
            "status": ["active"],
            "random_column": ["bad"],
        }
    )

    errors = validate_columns(
        df,
        "customers",
    )

    assert any(
        "Unexpected columns" in error
        for error in errors
    )


def test_empty_dataframe_fails():

    df = pd.DataFrame()

    errors = validate_not_empty(df)

    assert len(errors) == 1


def test_valid_dataset_passes():

    df = pd.DataFrame(
        {
            "product_id": ["PROD-00001"],
            "product_name": ["Test Product"],
            "category": ["Electronics"],
            "price": [100.00],
            "cost": [50.00],
            "active_flag": [True],
        }
    )

    errors = validate_dataset(
        df,
        "products",
    )

    assert errors == []