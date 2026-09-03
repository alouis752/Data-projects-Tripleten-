import pandas as pd

from src.generator.web_events import generate_web_events


def create_test_products():

    return pd.DataFrame(
        {
            "product_id": [
                "PROD-00001",
                "PROD-00002",
                "PROD-00003",
                "PROD-00004",
                "PROD-00005",
            ]
        }
    )


def test_generate_web_event_count():

    products_df = create_test_products()

    events_df = generate_web_events(
        products_df,
        count=500,
    )

    assert len(events_df) == 500


def test_event_ids_are_unique():

    products_df = create_test_products()

    events_df = generate_web_events(
        products_df,
        count=500,
    )

    assert events_df["event_id"].is_unique


def test_event_ids_are_not_null():

    products_df = create_test_products()

    events_df = generate_web_events(
        products_df,
        count=500,
    )

    assert events_df["event_id"].notna().all()


def test_session_ids_are_not_null():

    products_df = create_test_products()

    events_df = generate_web_events(
        products_df,
        count=500,
    )

    assert events_df["session_id"].notna().all()


def test_event_types_are_valid():

    products_df = create_test_products()

    events_df = generate_web_events(
        products_df,
        count=500,
    )

    valid_event_types = {
        "view",
        "search",
        "add_to_cart",
        "checkout",
        "purchase",
    }

    assert events_df["event_type"].isin(
        valid_event_types
    ).all()


def test_non_search_events_reference_valid_products():

    products_df = create_test_products()

    events_df = generate_web_events(
        products_df,
        count=500,
    )

    valid_product_ids = set(
        products_df["product_id"]
    )

    non_search_events = events_df[
        events_df["event_type"] != "search"
    ]

    assert non_search_events["product_id"].isin(
        valid_product_ids
    ).all()


def test_search_events_have_no_product():

    products_df = create_test_products()

    events_df = generate_web_events(
        products_df,
        count=500,
    )

    search_events = events_df[
        events_df["event_type"] == "search"
    ]

    assert search_events["product_id"].isna().all()