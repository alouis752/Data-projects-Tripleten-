select
    order_id,
    customer_id,
    order_ts,
    status,
    channel,
    source_file,
    load_ts
from {{ source('raw', 'orders') }}