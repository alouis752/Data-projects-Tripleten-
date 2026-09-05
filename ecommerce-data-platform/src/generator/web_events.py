import random
from datetime import datetime, timedelta

import pandas as pd
from pathlib import Path
from src.common.config import (
    DEFAULT_WEB_EVENT_COUNT,
    RANDOM_SEED,
    RAW_DATA_DIR,
)


EVENT_TYPES = [
    "view",
    "search",
    "add_to_cart",
    "checkout",
    "purchase",
]

EVENT_WEIGHTS = [
    0.55,
    0.15,
    0.15,
    0.10,
    0.05,
]

TRAFFIC_SOURCES = [
    "direct",
    "organic_search",
    "paid_search",
    "social",
    "email",
]

TRAFFIC_SOURCE_WEIGHTS = [
    0.25,
    0.30,
    0.20,
    0.15,
    0.10,
]


def generate_web_events(
    products_df: pd.DataFrame,
    count: int = DEFAULT_WEB_EVENT_COUNT,
    run_date: str = "2026-08-31",
) -> pd.DataFrame:

    random.seed(RANDOM_SEED + 4)

    events = []

    product_ids = products_df["product_id"].tolist()

    start_time = datetime.fromisoformat(
        f"{run_date}T00:00:00"
    )

    end_time = datetime.fromisoformat(
        f"{run_date}T23:59:59"
    )

    range_seconds = int(
        (end_time - start_time).total_seconds()
    )

    date_key = datetime.fromisoformat(
        run_date
    ).strftime("%Y%m%d")
    
    session_count = max(1, count // 5)

    session_ids = [
        f"SESSION-{date_key}-{number:06d}"
        for number in range(1, session_count + 1)
    ]

    for event_number in range(1, count + 1):

        event_type = random.choices(
            EVENT_TYPES,
            weights=EVENT_WEIGHTS,
            k=1,
        )[0]

        event_ts = start_time + timedelta(
            seconds=random.randint(
                0,
                range_seconds,
            )
        )

        product_id = None

        if event_type != "search":
            product_id = random.choice(product_ids)

        event = {
            "event_id": f"EVENT-{date_key}-{event_number:06d}",
            "session_id": random.choice(session_ids),
            "event_type": event_type,
            "product_id": product_id,
            "traffic_source": random.choices(
                TRAFFIC_SOURCES,
                weights=TRAFFIC_SOURCE_WEIGHTS,
                k=1,
            )[0],
            "event_ts": event_ts,
        }

        events.append(event)

    return pd.DataFrame(events)


def save_web_events(
    df: pd.DataFrame,
    output_dir: Path = RAW_DATA_DIR,
) -> None:

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_dir
        / "web_events.json"
    )

    df.to_json(
        output_path,
        orient="records",
        lines=True,
        date_format="iso",
    )

    print(
        f"Saved {len(df):,} web events to:"
    )
    print(output_path)


if __name__ == "__main__":

    products_path = RAW_DATA_DIR / "products.csv"

    products_df = pd.read_csv(products_path)

    web_events_df = generate_web_events(
        products_df
    )

    save_web_events(web_events_df)

    print()
    print(web_events_df.head())

    print()
    print("Event counts:")
    print(
        web_events_df["event_type"]
        .value_counts()
    )