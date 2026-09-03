import random
from datetime import timedelta

import pandas as pd

from src.common.config import (
    RANDOM_SEED,
    RAW_DATA_DIR,
)


def generate_shipments(
    orders_df: pd.DataFrame,
) -> pd.DataFrame:

    random.seed(RANDOM_SEED + 6)

    orders_df = orders_df.copy()

    orders_df["order_ts"] = pd.to_datetime(
    orders_df["order_ts"]
)

    shipment_records = []

    shippable_orders = orders_df[
        orders_df["status"].isin(
            [
                "shipped",
                "delivered",
            ]
        )
    ]

    for _, order in shippable_orders.iterrows():

        shipped_at = (
            order["order_ts"]
            + timedelta(
                hours=random.randint(
                    6,
                    72,
                )
            )
        )

        delivered_at = None

        if order["status"] == "delivered":
            delivered_at = (
                shipped_at
                + timedelta(
                    hours=random.randint(
                        24,
                        120,
                    )
                )
            )

        shipment = {
            "shipment_id": (
                f"SHIP-{len(shipment_records) + 1:07d}"
            ),
            "order_id": order["order_id"],
            "shipped_at": shipped_at,
            "delivered_at": delivered_at,
            "carrier": random.choice(
                [
                    "UPS",
                    "FedEx",
                    "USPS",
                ]
            ),
        }

        shipment_records.append(
            shipment
        )

    return pd.DataFrame(
        shipment_records
    )


def save_shipments(
    df: pd.DataFrame,
) -> None:

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        RAW_DATA_DIR
        / "shipments.csv"
    )

    df.to_csv(
        output_path,
        index=False,
    )

    print(
        f"Saved {len(df):,} shipments to:"
    )

    print(output_path)


if __name__ == "__main__":

    orders_path = (
        RAW_DATA_DIR
        / "orders.json"
    )

    orders_df = pd.read_json(
        orders_path,
        lines=True,
    )

    shipments_df = generate_shipments(
        orders_df
    )

    save_shipments(
        shipments_df
    )

    print()

    print(
        shipments_df.head()
    )