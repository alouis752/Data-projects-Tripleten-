from pathlib import Path

import pandas as pd

from src.common.config import get_batch_raw_dir


def inject_bad_customer(
    run_date: str,
) -> Path:
    """
    Intentionally corrupt one customer record for pipeline testing.

    This is used to demonstrate validation and quarantine behavior.
    """

    batch_dir = get_batch_raw_dir(run_date)
    customers_path = batch_dir / "customers.csv"

    if not customers_path.exists():
        raise FileNotFoundError(
            f"Customers file not found: {customers_path}"
        )

    customers_df = pd.read_csv(
        customers_path
    )

    if customers_df.empty:
        raise ValueError(
            "Customers dataset is empty."
        )

    # Intentionally remove a required business key.
    customers_df.loc[
        customers_df.index[0],
        "customer_id",
    ] = None

    customers_df.to_csv(
        customers_path,
        index=False,
        lineterminator="\n",
    )

    print(
        f"Injected bad customer record into: "
        f"{customers_path}"
    )

    return customers_path


def main():
    inject_bad_customer(
        run_date="2026-09-03"
    )


if __name__ == "__main__":
    main()