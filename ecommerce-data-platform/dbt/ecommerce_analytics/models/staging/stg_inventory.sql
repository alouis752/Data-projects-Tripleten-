select
    product_id,
    snapshot_ts,
    quantity_on_hand,
    reorder_point,
    source_file,
    load_ts
from {{ source('raw', 'inventory') }}