select
    customer_id,
    customer_name,
    email,
    created_at,
    region,
    segment,
    status,
    source_file,
    load_ts
from {{ source('raw', 'customers') }}