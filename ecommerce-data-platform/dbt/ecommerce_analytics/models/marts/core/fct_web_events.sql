{{
    config(
        materialized='incremental',
        unique_key='event_id',
        incremental_strategy='merge'
    )
}}

select
    event_id,
    session_id,
    event_type,
    product_id,
    traffic_source,
    event_ts,
    cast(event_ts as date) as event_date

from {{ ref('stg_web_events') }}

{% if is_incremental() %}

where event_ts >= (
    select coalesce(
        dateadd(day, -1, max(event_ts)),
        '1900-01-01'::timestamp
    )
    from {{ this }}
)

{% endif %}