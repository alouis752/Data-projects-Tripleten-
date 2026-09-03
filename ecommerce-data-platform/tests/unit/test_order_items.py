import pandas as pd

from src.generator.order_items import generate_order_items


def create_test_orders():

    return pd.DataFrame(
        {
            "order_id": [
                "ORD-0000001",
                "ORD-0000002",
                "ORD-0000003",
            ]
        }
    )


def create_test_products():

    return pd.DataFrame(
        {
            "product_id": [
                "PROD-00001",
                "PROD-00002",
                "PROD-00003",
                "PROD-00004",
                "PROD-00005",
            ],
            "price": [
                10.00,
                25.00,
                50.00,
                75.00,
                100.00,
            ],
        }
    )


def test_order_item_ids_are_unique():

    orders_df = create_test_orders()
    products_df = create_test_products()

    items_df = generate_order_items(
        orders_df,
        products_df,
    )

    assert items_df["order_item_id"].is_unique


def test_order_items_reference_valid_orders():

    orders_df = create_test_orders()
    products_df = create_test_products()

    items_df = generate_order_items(
        orders_df,
        products_df,
    )

    valid_order_ids = set(
        orders_df["order_id"]
    )

    assert items_df["order_id"].isin(
        valid_order_ids
    ).all()


def test_order_items_reference_valid_products():

    orders_df = create_test_orders()
    products_df = create_test_products()

    items_df = generate_order_items(
        orders_df,
        products_df,
    )

    valid_product_ids = set(
        products_df["product_id"]
    )

    assert items_df["product_id"].isin(
        valid_product_ids
    ).all()


def test_order_item_quantity_is_positive():

    orders_df = create_test_orders()
    products_df = create_test_products()

    items_df = generate_order_items(
        orders_df,
        products_df,
    )

    assert (
        items_df["quantity"] > 0
    ).all()


def test_order_item_discount_is_valid():

    orders_df = create_test_orders()
    products_df = create_test_products()

    items_df = generate_order_items(
        orders_df,
        products_df,
    )

    assert (
        (items_df["discount"] >= 0)
        & (items_df["discount"] <= 1)
    ).all()