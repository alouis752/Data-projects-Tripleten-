select
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    discount,
    source_file,
    load_ts
from {{ source('raw', 'order_items') }}