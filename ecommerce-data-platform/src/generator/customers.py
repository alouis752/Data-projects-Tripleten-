import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from faker import Faker

from src.common.config import (
    DEFAULT_CUSTOMER_COUNT,
    RANDOM_SEED,
    RAW_DATA_DIR,
)


fake = Faker()
fake.seed_instance(RANDOM_SEED)
random.seed(RANDOM_SEED)


REGIONS = [
    "Northeast",
    "Southeast",
    "Midwest",
    "Southwest",
    "West",
]

SEGMENTS = [
    "Consumer",
    "Small Business",
    "Enterprise",
]

STATUSES = [
    "active",
    "inactive",
]


def generate_customers(
    count: int = DEFAULT_CUSTOMER_COUNT,
    run_date: str = "2026-08-31",
) -> pd.DataFrame:
    customers = []

    start_date = datetime(2023, 1, 1)
    end_date = datetime.fromisoformat(run_date)

    
    date_range_days = (end_date - start_date).days

    for customer_number in range(1, count + 1):
        created_at = start_date + timedelta(
            days=random.randint(0, date_range_days)
        )

        customer = {
            "customer_id": f"CUST-{customer_number:06d}",
            "customer_name": fake.name(),
            "email": fake.unique.email(),
            "created_at": created_at,
            "region": random.choice(REGIONS),
            "segment": random.choices(
                SEGMENTS,
                weights=[0.75, 0.20, 0.05],
                k=1,
            )[0],
            "status": random.choices(
                STATUSES,
                weights=[0.95, 0.05],
                k=1,
            )[0],
        }

        customers.append(customer)

    return pd.DataFrame(customers)


def save_customers(
    df: pd.DataFrame,
    output_dir: Path = RAW_DATA_DIR,
) -> None:

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_dir
        / "customers.csv"
    )

    df.to_csv(
        output_path,
        index=False,
        lineterminator="\n",
    )

    print(
        f"Saved {len(df):,} customers to:"
    )
    print(output_path)


if __name__ == "__main__":
    customer_df = generate_customers()
    save_customers(customer_df)

    print()
    print(customer_df.head())