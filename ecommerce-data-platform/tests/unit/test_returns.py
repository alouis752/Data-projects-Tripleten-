from datetime import datetime

import pandas as pd

from src.generator.returns import generate_returns


def create_test_shipments():

    return pd.DataFrame(
        {
            "shipment_id": [
                "SHIP-0000001",
                "SHIP-0000002",
                "SHIP-0000003",
            ],
            "order_id": [
                "ORD-0000001",
                "ORD-0000002",
                "ORD-0000003",
            ],
            "shipped_at": [
                datetime(2026, 8, 1),
                datetime(2026, 8, 2),
                datetime(2026, 8, 3),
            ],
            "delivered_at": [
                datetime(2026, 8, 5),
                datetime(2026, 8, 6),
                None,
            ],
            "carrier": [
                "UPS",
                "FedEx",
                "USPS",
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


def test_returns_reference_valid_orders():

    shipments_df = create_test_shipments()
    order_items_df = create_test_order_items()

    returns_df = generate_returns(
        shipments_df,
        order_items_df,
    )

    if returns_df.empty:
        return

    valid_order_ids = set(
        shipments_df["order_id"]
    )

    assert returns_df["order_id"].isin(
        valid_order_ids
    ).all()


def test_returns_only_reference_delivered_orders():

    shipments_df = create_test_shipments()
    order_items_df = create_test_order_items()

    returns_df = generate_returns(
        shipments_df,
        order_items_df,
    )

    if returns_df.empty:
        return

    delivered_order_ids = set(
        shipments_df[
            shipments_df["delivered_at"].notna()
        ]["order_id"]
    )

    assert returns_df["order_id"].isin(
        delivered_order_ids
    ).all()


def test_return_timestamp_is_after_delivery():

    shipments_df = create_test_shipments()
    order_items_df = create_test_order_items()

    returns_df = generate_returns(
        shipments_df,
        order_items_df,
    )

    if returns_df.empty:
        return

    merged_df = returns_df.merge(
        shipments_df[
            [
                "order_id",
                "delivered_at",
            ]
        ],
        on="order_id",
        how="left",
    )

    merged_df["returned_at"] = pd.to_datetime(
        merged_df["returned_at"]
    )

    merged_df["delivered_at"] = pd.to_datetime(
        merged_df["delivered_at"]
    )

    assert (
        merged_df["returned_at"]
        >= merged_df["delivered_at"]
    ).all()


def test_return_amount_is_positive():

    shipments_df = create_test_shipments()
    order_items_df = create_test_order_items()

    returns_df = generate_returns(
        shipments_df,
        order_items_df,
    )

    if returns_df.empty:
        return

    assert (
        returns_df["return_amount"] > 0
    ).all()


def test_return_amount_does_not_exceed_order_value():

    shipments_df = create_test_shipments()
    order_items_df = create_test_order_items()

    returns_df = generate_returns(
        shipments_df,
        order_items_df,
    )

    if returns_df.empty:
        return

    order_items_df = order_items_df.copy()

    order_items_df["line_value"] = (
        order_items_df["quantity"]
        * order_items_df["unit_price"]
        * (1 - order_items_df["discount"])
    )

    order_values = (
        order_items_df
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

    merged_df = returns_df.merge(
        order_values,
        on="order_id",
        how="left",
    )

    assert (
        merged_df["return_amount"]
        <= merged_df["order_value"]
    ).all()