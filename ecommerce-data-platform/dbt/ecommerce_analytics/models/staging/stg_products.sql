select
    product_id,
    product_name,
    category,
    price,
    cost,
    active_flag,
    source_file,
    load_ts
from {{ source('raw', 'products') }}