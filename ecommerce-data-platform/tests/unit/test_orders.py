import pandas as pd

from src.generator.orders import generate_orders


def test_generate_order_count():

    customers_df = pd.DataFrame(
        {
            "customer_id": [
                "CUST-000001",
                "CUST-000002",
                "CUST-000003",
            ]
        }
    )

    df = generate_orders(
        customers_df,
        count=50,
    )

    assert len(df) == 50


def test_order_ids_are_unique():

    customers_df = pd.DataFrame(
        {
            "customer_id": [
                "CUST-000001",
                "CUST-000002",
                "CUST-000003",
            ]
        }
    )

    df = generate_orders(
        customers_df,
        count=100,
    )

    assert df["order_id"].is_unique


def test_order_customer_ids_are_valid():

    customers_df = pd.DataFrame(
        {
            "customer_id": [
                "CUST-000001",
                "CUST-000002",
                "CUST-000003",
            ]
        }
    )

    orders_df = generate_orders(
        customers_df,
        count=100,
    )

    valid_customer_ids = set(
        customers_df["customer_id"]
    )

    assert orders_df["customer_id"].isin(
        valid_customer_ids
    ).all()


def test_order_statuses_are_valid():

    customers_df = pd.DataFrame(
        {
            "customer_id": [
                "CUST-000001",
                "CUST-000002",
            ]
        }
    )

    orders_df = generate_orders(
        customers_df,
        count=100,
    )

    valid_statuses = {
        "pending",
        "processing",
        "shipped",
        "delivered",
        "cancelled",
    }

    assert orders_df["status"].isin(
        valid_statuses
    ).all()