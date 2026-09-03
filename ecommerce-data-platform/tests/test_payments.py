from datetime import datetime

import pandas as pd

from src.generator.payments import generate_payments


def create_test_orders():

    return pd.DataFrame(
        {
            "order_id": [
                "ORD-0000001",
                "ORD-0000002",
                "ORD-0000003",
            ],
            "order_ts": [
                datetime(2026, 8, 1, 10, 0),
                datetime(2026, 8, 2, 11, 0),
                datetime(2026, 8, 3, 12, 0),
            ],
            "status": [
                "delivered",
                "shipped",
                "cancelled",
            ],
        }
    )


def create_test_order_items():

    return pd.DataFrame(
        {
            "order_item_id": [
                "ITEM-00000001",
                "ITEM-00000002",
                "ITEM-00000003",
            ],
            "order_id": [
                "ORD-0000001",
                "ORD-0000002",
                "ORD-0000003",
            ],
            "product_id": [
                "PROD-00001",
                "PROD-00002",
                "PROD-00003",
            ],
            "quantity": [
                2,
                1,
                3,
            ],
            "unit_price": [
                50.00,
                100.00,
                25.00,
            ],
            "discount": [
                0.00,
                0.10,
                0.00,
            ],
        }
    )


def test_cancelled_orders_do_not_have_payments():

    orders_df = create_test_orders()
    order_items_df = create_test_order_items()

    payments_df = generate_payments(
        orders_df,
        order_items_df,
    )

    assert "ORD-0000003" not in set(
        payments_df["order_id"]
    )


def test_payment_ids_are_unique():

    orders_df = create_test_orders()
    order_items_df = create_test_order_items()

    payments_df = generate_payments(
        orders_df,
        order_items_df,
    )

    assert payments_df[
        "payment_id"
    ].is_unique


def test_payments_reference_valid_orders():

    orders_df = create_test_orders()
    order_items_df = create_test_order_items()

    payments_df = generate_payments(
        orders_df,
        order_items_df,
    )

    valid_order_ids = set(
        orders_df["order_id"]
    )

    assert payments_df["order_id"].isin(
        valid_order_ids
    ).all()


def test_payment_timestamp_is_after_order():

    orders_df = create_test_orders()
    order_items_df = create_test_order_items()

    payments_df = generate_payments(
        orders_df,
        order_items_df,
    )

    merged_df = payments_df.merge(
        orders_df[
            [
                "order_id",
                "order_ts",
            ]
        ],
        on="order_id",
        how="left",
    )

    assert (
        merged_df["payment_ts"]
        >= merged_df["order_ts"]
    ).all()


def test_failed_payments_have_zero_amount():

    orders_df = create_test_orders()
    order_items_df = create_test_order_items()

    payments_df = generate_payments(
        orders_df,
        order_items_df,
    )

    failed_payments = payments_df[
        payments_df["payment_status"]
        == "failed"
    ]

    if failed_payments.empty:
        return

    assert (
        failed_payments["amount"] == 0
    ).all()


def test_successful_payment_matches_order_value():

    orders_df = create_test_orders()
    order_items_df = create_test_order_items()

    payments_df = generate_payments(
        orders_df,
        order_items_df,
    )

    successful_payments = payments_df[
        payments_df["payment_status"]
        == "successful"
    ]

    if successful_payments.empty:
        return

    items_df = order_items_df.copy()

    items_df["line_value"] = (
        items_df["quantity"]
        * items_df["unit_price"]
        * (1 - items_df["discount"])
    )

    order_values = (
        items_df
        .groupby(
            "order_id",
            as_index=False,
        )["line_value"]
        .sum()
        .rename(
            columns={
                "line_value": "order_value"
            }
        )
    )

    merged_df = successful_payments.merge(
        order_values,
        on="order_id",
        how="left",
    )

    assert (
        merged_df["amount"].round(2)
        == merged_df["order_value"].round(2)
    ).all()