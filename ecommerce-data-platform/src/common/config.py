from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"


def get_batch_raw_dir(run_date: str) -> Path:

    return RAW_DATA_DIR / f"run_date={run_date}"


RANDOM_SEED = 42

DEFAULT_CUSTOMER_COUNT = 500
DEFAULT_PRODUCT_COUNT = 100
DEFAULT_ORDER_COUNT = 1000
DEFAULT_WEB_EVENT_COUNT = 10000

DEFAULT_INVENTORY_MIN_QUANTITY = 0
DEFAULT_INVENTORY_MAX_QUANTITY = 250