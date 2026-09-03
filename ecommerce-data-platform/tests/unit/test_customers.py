from src.generator.customers import generate_customers


def test_generate_customer_count():
    df = generate_customers(25)

    assert len(df) == 25


def test_customer_ids_are_unique():
    df = generate_customers(100)

    assert df["customer_id"].is_unique


def test_customer_ids_are_not_null():
    df = generate_customers(100)

    assert df["customer_id"].notna().all()


def test_customer_segments_are_valid():
    df = generate_customers(100)

    valid_segments = {
        "Consumer",
        "Small Business",
        "Enterprise",
    }

    assert df["segment"].isin(valid_segments).all()


def test_customer_statuses_are_valid():
    df = generate_customers(100)

    valid_statuses = {
        "active",
        "inactive",
    }

    assert df["status"].isin(valid_statuses).all()