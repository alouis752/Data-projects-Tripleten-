select
    shipment_id,
    order_id,
    shipped_at,
    delivered_at,
    carrier,
    source_file,
    load_ts
from {{ source('raw', 'shipments') }}