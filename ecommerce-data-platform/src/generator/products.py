import random

import pandas as pd
from faker import Faker
from pathlib import Path
from src.common.config import (
    DEFAULT_PRODUCT_COUNT,
    RANDOM_SEED,
    RAW_DATA_DIR,
)


fake = Faker()
fake.seed_instance(RANDOM_SEED + 1)
random.seed(RANDOM_SEED + 1)


CATEGORIES = {
    "Electronics": [
        "Wireless Headphones",
        "Bluetooth Speaker",
        "Mechanical Keyboard",
        "Gaming Mouse",
        "USB-C Hub",
    ],
    "Home": [
        "Coffee Maker",
        "Desk Lamp",
        "Air Purifier",
        "Storage Organizer",
        "Electric Kettle",
    ],
    "Fitness": [
        "Yoga Mat",
        "Resistance Bands",
        "Adjustable Dumbbell",
        "Foam Roller",
        "Fitness Tracker",
    ],
    "Outdoor": [
        "Camping Lantern",
        "Hiking Backpack",
        "Water Bottle",
        "Portable Cooler",
        "Camping Chair",
    ],
    "Office": [
        "Office Chair",
        "Laptop Stand",
        "Desk Organizer",
        "Webcam",
        "Wireless Mouse",
    ],
}


CATEGORY_WEIGHTS = {
    "Electronics": 0.30,
    "Home": 0.25,
    "Fitness": 0.15,
    "Outdoor": 0.10,
    "Office": 0.20,
}


PRICE_RANGES = {
    "Electronics": (25, 350),
    "Home": (20, 250),
    "Fitness": (15, 300),
    "Outdoor": (15, 225),
    "Office": (20, 400),
}


def generate_products(count: int = DEFAULT_PRODUCT_COUNT) -> pd.DataFrame:
    products = []

    categories = list(CATEGORIES.keys())
    category_weights = [
        CATEGORY_WEIGHTS[category]
        for category in categories
    ]

    for product_number in range(1, count + 1):
        category = random.choices(
            categories,
            weights=category_weights,
            k=1,
        )[0]

        base_name = random.choice(CATEGORIES[category])

        price_min, price_max = PRICE_RANGES[category]

        price = round(
            random.uniform(price_min, price_max),
            2,
        )

        cost_percentage = random.uniform(0.40, 0.70)

        cost = round(
            price * cost_percentage,
            2,
        )

        product = {
            "product_id": f"PROD-{product_number:05d}",
            "product_name": f"{fake.word().title()} {base_name}",
            "category": category,
            "price": price,
            "cost": cost,
            "active_flag": random.choices(
                [True, False],
                weights=[0.97, 0.03],
                k=1,
            )[0],
        }

        products.append(product)

    return pd.DataFrame(products)


def save_products(
    df: pd.DataFrame,
    output_dir: Path = RAW_DATA_DIR,
) -> None:

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = output_dir / "products.csv"

    df.to_csv(
        output_path,
        index=False,
        lineterminator="\n",
    )

    print(f"Saved {len(df):,} products to:")
    print(output_path)


if __name__ == "__main__":
    product_df = generate_products()
    save_products(product_df)

    print()
    print(product_df.head())