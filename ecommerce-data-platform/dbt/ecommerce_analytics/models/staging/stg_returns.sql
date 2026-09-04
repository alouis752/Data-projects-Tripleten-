select
    return_id,
    order_id,
    returned_at,
    return_amount,
    return_reason,
    source_file,
    load_ts
from {{ source('raw', 'returns') }}