from datetime import datetime
from src.common.config import get_batch_raw_dir

from src.generator.customers import (
    generate_customers,
    save_customers,
)
from src.generator.products import (
    generate_products,
    save_products,
)
from src.generator.orders import (
    generate_orders,
    save_orders,
)
from src.generator.order_items import (
    generate_order_items,
    save_order_items,
)
from src.generator.web_events import (
    generate_web_events,
    save_web_events,
)
from src.generator.inventory import (
    generate_inventory_snapshot,
    save_inventory_snapshot,
)
from src.generator.payments import (
    generate_payments,
    save_payments,
)
from src.generator.shipments import (
    generate_shipments,
    save_shipments,
)
from src.generator.returns import (
    generate_returns,
    save_returns,
)


def generate_batch(
    run_date: str = "2026-08-31",
) -> dict:
    """
    Generate all source datasets required for one pipeline batch.

    The generators are executed in dependency order so downstream
    datasets can reference upstream records.
    """

    print(
        f"Starting data generation for run_date={run_date}"
    )

    batch_dir = get_batch_raw_dir(run_date)

    batch_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        f"Batch output directory: {batch_dir}"
    )
    # ---------------------------------------------------------
    # 1. Customers
    # ---------------------------------------------------------

    customers_df = generate_customers(
        run_date=run_date,
    )
    save_customers(
        customers_df,
        output_dir=batch_dir,
    )

    # ---------------------------------------------------------
    # 2. Products
    # ---------------------------------------------------------

    products_df = generate_products()
    save_products(
        products_df,
        output_dir=batch_dir,
    )

    # ---------------------------------------------------------
    # 3. Orders
    # ---------------------------------------------------------

    orders_df = generate_orders(
        customers_df=customers_df,
        run_date=run_date,
    )
    save_orders(
        orders_df,
        output_dir=batch_dir,
    )

    # ---------------------------------------------------------
    # 4. Order Items
    # ---------------------------------------------------------

    order_items_df = generate_order_items(
        orders_df=orders_df,
        products_df=products_df,
    )
    save_order_items(
        order_items_df,
        output_dir=batch_dir,
        )

    # ---------------------------------------------------------
    # 5. Web Events
    # ---------------------------------------------------------

    web_events_df = generate_web_events(
        products_df=products_df,
        run_date=run_date,
    )

    save_web_events(
        web_events_df,
        output_dir=batch_dir,
    )

    # ---------------------------------------------------------
    # 6. Inventory
    # ---------------------------------------------------------

    snapshot_ts = datetime.fromisoformat(
        f"{run_date}T23:00:00"
    )

    inventory_df = generate_inventory_snapshot(
        products_df=products_df,
        snapshot_ts=snapshot_ts,
    )
    save_inventory_snapshot(
        inventory_df,
        output_dir=batch_dir,
    )

    # ---------------------------------------------------------
    # 7. Payments
    # ---------------------------------------------------------

    payments_df = generate_payments(
        orders_df=orders_df,
        order_items_df=order_items_df,
    )
    save_payments(
        payments_df,
        output_dir=batch_dir,
    )

    # ---------------------------------------------------------
    # 8. Shipments
    # ---------------------------------------------------------

    shipments_df = generate_shipments(
        orders_df=orders_df,
    )
    save_shipments(
        shipments_df,
        output_dir=batch_dir,
    )

    # ---------------------------------------------------------
    # 9. Returns
    # ---------------------------------------------------------

    returns_df = generate_returns(
        shipments_df=shipments_df,
        order_items_df=order_items_df,
    )
    save_returns(
        returns_df,
        output_dir=batch_dir,
    )

    print()
    print(
        f"Finished data generation for run_date={run_date}"
    )

    return {
        "run_date": run_date,
        "status": "generated",
        "datasets_generated": 9,
        "row_counts": {
            "customers": len(customers_df),
            "products": len(products_df),
            "orders": len(orders_df),
            "order_items": len(order_items_df),
            "web_events": len(web_events_df),
            "inventory": len(inventory_df),
            "payments": len(payments_df),
            "shipments": len(shipments_df),
            "returns": len(returns_df),
        },
    }


def main():
    generate_batch()


if __name__ == "__main__":
    main()