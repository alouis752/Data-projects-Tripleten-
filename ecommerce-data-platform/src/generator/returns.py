import random
from datetime import timedelta

import pandas as pd

from src.common.config import (
    RANDOM_SEED,
    RAW_DATA_DIR,
)


RETURN_REASONS = [
    "damaged",
    "wrong_item",
    "not_as_expected",
    "changed_mind",
    "late_delivery",
]


def generate_returns(
    shipments_df: pd.DataFrame,
    order_items_df: pd.DataFrame,
) -> pd.DataFrame:

    random.seed(RANDOM_SEED + 7)

    returns = []

    shipments_df = shipments_df.copy()
    shipments_df["delivered_at"] = pd.to_datetime(
        shipments_df["delivered_at"]
    )

    delivered_shipments = shipments_df[
        shipments_df["delivered_at"].notna()
    ]

    for _, shipment in delivered_shipments.iterrows():

        should_return = random.choices(
            [True, False],
            weights=[0.08, 0.92],
            k=1,
        )[0]

        if not should_return:
            continue

        order_items = order_items_df[
            order_items_df["order_id"]
            == shipment["order_id"]
        ]

        if order_items.empty:
            continue

        gross_value = (
            order_items["quantity"]
            * order_items["unit_price"]
        )

        discounted_value = gross_value * (
            1 - order_items["discount"]
        )

        order_value = round(
            discounted_value.sum(),
            2,
        )

        return_percentage = random.choice(
            [
                0.25,
                0.50,
                0.75,
                1.00,
            ]
        )

        return_amount = round(
            order_value * return_percentage,
            2,
        )

        returned_at = (
            shipment["delivered_at"]
            + timedelta(
                days=random.randint(
                    1,
                    30,
                )
            )
        )

        return_record = {
            "return_id": (
                f"RET-{len(returns) + 1:07d}"
            ),
            "order_id": shipment["order_id"],
            "returned_at": returned_at,
            "return_amount": return_amount,
            "return_reason": random.choice(
                RETURN_REASONS
            ),
        }

        returns.append(
            return_record
        )

    return pd.DataFrame(
        returns
    )


def save_returns(
    df: pd.DataFrame,
) -> None:

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        RAW_DATA_DIR
        / "returns.csv"
    )

    df.to_csv(
        output_path,
        index=False,
    )

    print(
        f"Saved {len(df):,} returns to:"
    )
    print(output_path)


if __name__ == "__main__":

    shipments_path = (
        RAW_DATA_DIR
        / "shipments.csv"
    )

    order_items_path = (
        RAW_DATA_DIR
        / "order_items.json"
    )

    shipments_df = pd.read_csv(
        shipments_path
    )

    order_items_df = pd.read_json(
        order_items_path,
        lines=True,
    )

    returns_df = generate_returns(
        shipments_df,
        order_items_df,
    )

    save_returns(
        returns_df
    )

    print()
    print(returns_df.head())