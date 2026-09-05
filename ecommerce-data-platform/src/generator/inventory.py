import random
from datetime import datetime

import pandas as pd
from pathlib import Path
from src.common.config import (
    DEFAULT_INVENTORY_MAX_QUANTITY,
    DEFAULT_INVENTORY_MIN_QUANTITY,
    RANDOM_SEED,
    RAW_DATA_DIR,
)


def generate_inventory_snapshot(
    products_df: pd.DataFrame,
    snapshot_ts: datetime,
) -> pd.DataFrame:

    random.seed(RANDOM_SEED + 5)

    inventory_records = []

    for _, product in products_df.iterrows():

        quantity_on_hand = random.randint(
            DEFAULT_INVENTORY_MIN_QUANTITY,
            DEFAULT_INVENTORY_MAX_QUANTITY,
        )

        reorder_point = random.randint(
            10,
            40,
        )

        inventory_record = {
            "product_id": product["product_id"],
            "snapshot_ts": snapshot_ts,
            "quantity_on_hand": quantity_on_hand,
            "reorder_point": reorder_point,
        }

        inventory_records.append(
            inventory_record
        )

    return pd.DataFrame(
        inventory_records
    )


def save_inventory_snapshot(
    df: pd.DataFrame,
    output_dir: Path = RAW_DATA_DIR,
) -> None:

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_dir
        / "inventory.csv"
    )

    df.to_csv(
        output_path,
        index=False,
        lineterminator="\n",
    )

    print(
        f"Saved {len(df):,} inventory records to:"
    )
    print(output_path)


if __name__ == "__main__":

    products_path = (
        RAW_DATA_DIR
        / "products.csv"
    )

    products_df = pd.read_csv(
        products_path
    )

    snapshot_ts = datetime(
        2026,
        8,
        31,
        23,
        0,
        0,
    )

    inventory_df = (
        generate_inventory_snapshot(
            products_df,
            snapshot_ts,
        )
    )

    save_inventory_snapshot(
        inventory_df
    )

    print()
    print(inventory_df.head())