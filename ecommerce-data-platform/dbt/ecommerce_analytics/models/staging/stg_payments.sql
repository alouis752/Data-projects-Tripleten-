select
    payment_id,
    order_id,
    amount,
    payment_method,
    payment_status,
    payment_ts,
    source_file,
    load_ts
from {{ source('raw', 'payments') }}