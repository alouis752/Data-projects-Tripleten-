import random
from datetime import datetime, timedelta

import pandas as pd
from pathlib import Path
from src.common.config import (
    DEFAULT_ORDER_COUNT,
    RANDOM_SEED,
    RAW_DATA_DIR,
)


ORDER_STATUSES = [
    "pending",
    "processing",
    "shipped",
    "delivered",
    "cancelled",
]

STATUS_WEIGHTS = [
    0.05,
    0.10,
    0.10,
    0.70,
    0.05,
]

CHANNELS = [
    "web",
    "mobile",
]


def generate_orders(
    customers_df: pd.DataFrame,
    count: int = DEFAULT_ORDER_COUNT,
    run_date: str = "2026-08-31",
) -> pd.DataFrame:

    random.seed(RANDOM_SEED + 2)

    orders = []

    customer_ids = customers_df["customer_id"].tolist()

    # Generate orders only for the requested batch date.
    start_date = datetime.fromisoformat(
        f"{run_date}T00:00:00"
    )

    end_date = datetime.fromisoformat(
        f"{run_date}T23:59:59"
    )

    date_range_seconds = int(
        (end_date - start_date).total_seconds()
    )

    # Used in the order ID so IDs remain unique across batch dates.
    date_key = datetime.fromisoformat(
        run_date
    ).strftime("%Y%m%d")

    for order_number in range(1, count + 1):

        order_ts = start_date + timedelta(
            seconds=random.randint(
                0,
                date_range_seconds,
            )
        )

        order = {
            "order_id": (
                f"ORD-{date_key}-{order_number:04d}"
            ),
            "customer_id": random.choice(
                customer_ids
            ),
            "order_ts": order_ts,
            "status": random.choices(
                ORDER_STATUSES,
                weights=STATUS_WEIGHTS,
                k=1,
            )[0],
            "channel": random.choices(
                CHANNELS,
                weights=[0.70, 0.30],
                k=1,
            )[0],
        }

        orders.append(order)

    return pd.DataFrame(orders)


def save_orders(
    df: pd.DataFrame,
    output_dir: Path = RAW_DATA_DIR,
) -> None:

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = output_dir / "orders.json"

    df.to_json(
        output_path,
        orient="records",
        lines=True,
        date_format="iso",
    )

    print(f"Saved {len(df):,} orders to:")
    print(output_path)


if __name__ == "__main__":

    customers_path = (
        RAW_DATA_DIR
        / "customers.csv"
    )

    customers_df = pd.read_csv(
        customers_path
    )

    orders_df = generate_orders(
        customers_df
    )

    save_orders(
        orders_df
    )

    print()
    print(orders_df.head())