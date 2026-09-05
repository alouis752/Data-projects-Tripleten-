import random

import pandas as pd
from pathlib import Path
from src.common.config import (
    RANDOM_SEED,
    RAW_DATA_DIR,
)


def generate_order_items(
    orders_df: pd.DataFrame,
    products_df: pd.DataFrame,
) -> pd.DataFrame:

    random.seed(RANDOM_SEED + 3)

    order_items = []

    product_records = products_df.to_dict("records")

    for _, order in orders_df.iterrows():

        number_of_items = random.choices(
            [1, 2, 3, 4, 5],
            weights=[0.40, 0.30, 0.15, 0.10, 0.05],
            k=1,
        )[0]

        selected_products = random.sample(
            product_records,
            k=number_of_items,
        )

        for item_number, product in enumerate(
            selected_products,
            start=1,
        ):

            quantity = random.choices(
                [1, 2, 3, 4],
                weights=[0.70, 0.20, 0.07, 0.03],
                k=1,
            )[0]

            discount = random.choices(
                [0.00, 0.05, 0.10, 0.15, 0.20],
                weights=[0.60, 0.15, 0.15, 0.07, 0.03],
                k=1,
            )[0]

            order_item = {
                "order_item_id": (
                    f"ITEM-{order['order_id']}-{item_number:02d}"
                ),
                "order_id": order["order_id"],
                "product_id": product["product_id"],
                "quantity": quantity,
                "unit_price": product["price"],
                "discount": discount,
            }

            order_items.append(order_item)

    return pd.DataFrame(order_items)


def save_order_items(
    df: pd.DataFrame,
    output_dir: Path = RAW_DATA_DIR,
) -> None:

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = output_dir / "order_items.json"

    df.to_json(
        output_path,
        orient="records",
        lines=True,
    )

    print(f"Saved {len(df):,} order items to:")
    print(output_path)


if __name__ == "__main__":

    orders_path = RAW_DATA_DIR / "orders.json"
    products_path = RAW_DATA_DIR / "products.csv"

    orders_df = pd.read_json(
        orders_path,
        lines=True,
    )

    products_df = pd.read_csv(
        products_path
    )

    order_items_df = generate_order_items(
        orders_df=orders_df,
        products_df=products_df,
    )

    save_order_items(
        order_items_df
    )

    print()
    print(order_items_df.head())