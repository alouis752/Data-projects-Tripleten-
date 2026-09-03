from datetime import datetime

import pandas as pd

from src.generator.shipments import generate_shipments


def create_test_orders():

    return pd.DataFrame(
        {
            "order_id": [
                "ORD-0000001",
                "ORD-0000002",
                "ORD-0000003",
                "ORD-0000004",
                "ORD-0000005",
            ],
            "order_ts": [
                datetime(2026, 8, 1, 10, 0),
                datetime(2026, 8, 2, 11, 0),
                datetime(2026, 8, 3, 12, 0),
                datetime(2026, 8, 4, 13, 0),
                datetime(2026, 8, 5, 14, 0),
            ],
            "status": [
                "pending",
                "processing",
                "cancelled",
                "shipped",
                "delivered",
            ],
        }
    )


def test_only_shippable_orders_create_shipments():

    orders_df = create_test_orders()

    shipments_df = generate_shipments(
        orders_df
    )

    expected_order_ids = {
        "ORD-0000004",
        "ORD-0000005",
    }

    assert set(
        shipments_df["order_id"]
    ) == expected_order_ids


def test_shipment_ids_are_unique():

    orders_df = create_test_orders()

    shipments_df = generate_shipments(
        orders_df
    )

    assert shipments_df[
        "shipment_id"
    ].is_unique


def test_shipments_reference_valid_orders():

    orders_df = create_test_orders()

    shipments_df = generate_shipments(
        orders_df
    )

    valid_order_ids = set(
        orders_df["order_id"]
    )

    assert shipments_df["order_id"].isin(
        valid_order_ids
    ).all()


def test_shipped_at_is_after_order_ts():

    orders_df = create_test_orders()

    shipments_df = generate_shipments(
        orders_df
    )

    merged_df = shipments_df.merge(
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
        merged_df["shipped_at"]
        >= merged_df["order_ts"]
    ).all()


def test_delivered_orders_have_delivery_timestamp():

    orders_df = create_test_orders()

    shipments_df = generate_shipments(
        orders_df
    )

    delivered_orders = orders_df[
        orders_df["status"]
        == "delivered"
    ][
        [
            "order_id",
        ]
    ]

    delivered_shipments = (
        shipments_df.merge(
            delivered_orders,
            on="order_id",
            how="inner",
        )
    )

    assert delivered_shipments[
        "delivered_at"
    ].notna().all()


def test_shipped_orders_have_null_delivery_timestamp():

    orders_df = create_test_orders()

    shipments_df = generate_shipments(
        orders_df
    )

    shipped_orders = orders_df[
        orders_df["status"]
        == "shipped"
    ][
        [
            "order_id",
        ]
    ]

    shipped_shipments = (
        shipments_df.merge(
            shipped_orders,
            on="order_id",
            how="inner",
        )
    )

    assert shipped_shipments[
        "delivered_at"
    ].isna().all()


def test_delivery_is_after_shipment():

    orders_df = create_test_orders()

    shipments_df = generate_shipments(
        orders_df
    )

    delivered_shipments = shipments_df[
        shipments_df["delivered_at"]
        .notna()
    ]

    assert (
        delivered_shipments["delivered_at"]
        >= delivered_shipments["shipped_at"]
    ).all()