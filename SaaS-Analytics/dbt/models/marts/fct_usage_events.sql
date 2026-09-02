select
    event_id,
    customer_id,
    product_id,
    event_date,
    feature_used,
    usage_count,
    session_duration_minutes,
    platform
from {{ ref('stg_usage_events') }}