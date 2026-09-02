with usage as (

    select *
    from {{ ref('stg_usage_events') }}

),

final as (

    select
        customer_id,

        count(*) as total_usage_events,

        sum(usage_count) as total_usage_count,

        avg(session_duration_minutes) as avg_session_duration_minutes,

        max(event_date) as last_usage_date,

        count(distinct product_id) as products_used,

        count(distinct feature_used) as features_used

    from usage

    group by customer_id

)

select *
from final