from src.generator.products import generate_products


def test_generate_product_count():
    df = generate_products(25)

    assert len(df) == 25


def test_product_ids_are_unique():
    df = generate_products(100)

    assert df["product_id"].is_unique


def test_product_ids_are_not_null():
    df = generate_products(100)

    assert df["product_id"].notna().all()


def test_product_prices_are_positive():
    df = generate_products(100)

    assert (df["price"] > 0).all()


def test_product_costs_are_positive():
    df = generate_products(100)

    assert (df["cost"] > 0).all()


def test_product_cost_does_not_exceed_price():
    df = generate_products(100)

    assert (df["cost"] <= df["price"]).all()


def test_product_categories_are_valid():
    df = generate_products(100)

    valid_categories = {
        "Electronics",
        "Home",
        "Fitness",
        "Outdoor",
        "Office",
    }

    assert df["category"].isin(valid_categories).all()