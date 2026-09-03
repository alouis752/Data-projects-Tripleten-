import random
from datetime import timedelta

import pandas as pd

from src.common.config import (
    RANDOM_SEED,
    RAW_DATA_DIR,
)


PAYMENT_METHODS = [
    "credit_card",
    "paypal",
    "apple_pay",
    "google_pay",
]

PAYMENT_METHOD_WEIGHTS = [
    0.60,
    0.20,
    0.10,
    0.10,
]


def generate_payments(
    orders_df: pd.DataFrame,
    order_items_df: pd.DataFrame,
) -> pd.DataFrame:

    random.seed(RANDOM_SEED + 8)

    orders_df = orders_df.copy()

    orders_df["order_ts"] = pd.to_datetime(
        orders_df["order_ts"]
    )

    payments = []

    payable_orders = orders_df[
        orders_df["status"] != "cancelled"
    ]

    for _, order in payable_orders.iterrows():

        order_items = order_items_df[
            order_items_df["order_id"]
            == order["order_id"]
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

        payment_status = random.choices(
            [
                "successful",
                "failed",
            ],
            weights=[
                0.96,
                0.04,
            ],
            k=1,
        )[0]

        payment_amount = (
            order_value
            if payment_status == "successful"
            else 0.00
        )

        payment_ts = (
            order["order_ts"]
            + timedelta(
                minutes=random.randint(
                    1,
                    30,
                )
            )
        )

        payment = {
            "payment_id": (
                f"PAY-{len(payments) + 1:08d}"
            ),
            "order_id": order["order_id"],
            "amount": payment_amount,
            "payment_method": random.choices(
                PAYMENT_METHODS,
                weights=PAYMENT_METHOD_WEIGHTS,
                k=1,
            )[0],
            "payment_status": payment_status,
            "payment_ts": payment_ts,
        }

        payments.append(
            payment
        )

    return pd.DataFrame(
        payments
    )


def save_payments(
    df: pd.DataFrame,
) -> None:

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        RAW_DATA_DIR
        / "payments.csv"
    )

    df.to_csv(
        output_path,
        index=False,
    )

    print(
        f"Saved {len(df):,} payments to:"
    )

    print(output_path)


if __name__ == "__main__":

    orders_path = (
        RAW_DATA_DIR
        / "orders.json"
    )

    order_items_path = (
        RAW_DATA_DIR
        / "order_items.json"
    )

    orders_df = pd.read_json(
        orders_path,
        lines=True,
    )

    order_items_df = pd.read_json(
        order_items_path,
        lines=True,
    )

    payments_df = generate_payments(
        orders_df,
        order_items_df,
    )

    save_payments(
        payments_df
    )

    print()
    print(payments_df.head())

    print()
    print("Payment status counts:")
    print(
        payments_df[
            "payment_status"
        ].value_counts()
    )