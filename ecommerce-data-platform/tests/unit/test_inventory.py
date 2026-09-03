from datetime import datetime

import pandas as pd

from src.generator.inventory import generate_inventory_snapshot


def create_test_products():

    return pd.DataFrame(
        {
            "product_id": [
                "PROD-00001",
                "PROD-00002",
                "PROD-00003",
                "PROD-00004",
                "PROD-00005",
            ]
        }
    )


def test_inventory_row_count_matches_products():

    products_df = create_test_products()

    snapshot_ts = datetime(
        2026,
        8,
        31,
        23,
        0,
        0,
    )

    inventory_df = generate_inventory_snapshot(
        products_df,
        snapshot_ts,
    )

    assert len(inventory_df) == len(products_df)


def test_inventory_references_valid_products():

    products_df = create_test_products()

    snapshot_ts = datetime(
        2026,
        8,
        31,
        23,
        0,
        0,
    )

    inventory_df = generate_inventory_snapshot(
        products_df,
        snapshot_ts,
    )

    valid_product_ids = set(
        products_df["product_id"]
    )

    assert inventory_df["product_id"].isin(
        valid_product_ids
    ).all()


def test_inventory_quantity_is_not_negative():

    products_df = create_test_products()

    snapshot_ts = datetime(
        2026,
        8,
        31,
        23,
        0,
        0,
    )

    inventory_df = generate_inventory_snapshot(
        products_df,
        snapshot_ts,
    )

    assert (
        inventory_df["quantity_on_hand"] >= 0
    ).all()


def test_inventory_reorder_point_is_positive():

    products_df = create_test_products()

    snapshot_ts = datetime(
        2026,
        8,
        31,
        23,
        0,
        0,
    )

    inventory_df = generate_inventory_snapshot(
        products_df,
        snapshot_ts,
    )

    assert (
        inventory_df["reorder_point"] > 0
    ).all()


def test_inventory_snapshot_timestamp_is_correct():

    products_df = create_test_products()

    snapshot_ts = datetime(
        2026,
        8,
        31,
        23,
        0,
        0,
    )

    inventory_df = generate_inventory_snapshot(
        products_df,
        snapshot_ts,
    )

    assert (
        inventory_df["snapshot_ts"]
        == snapshot_ts
    ).all()


def test_inventory_product_snapshot_grain_is_unique():

    products_df = create_test_products()

    snapshot_ts = datetime(
        2026,
        8,
        31,
        23,
        0,
        0,
    )

    inventory_df = generate_inventory_snapshot(
        products_df,
        snapshot_ts,
    )

    duplicate_count = (
        inventory_df
        .duplicated(
            subset=[
                "product_id",
                "snapshot_ts",
            ]
        )
        .sum()
    )

    assert duplicate_count == 0