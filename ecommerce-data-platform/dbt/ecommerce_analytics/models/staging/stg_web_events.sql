select
    event_id,
    session_id,
    event_type,
    product_id,
    traffic_source,
    event_ts,
    source_file,
    load_ts
from {{ source('raw', 'web_events') }}