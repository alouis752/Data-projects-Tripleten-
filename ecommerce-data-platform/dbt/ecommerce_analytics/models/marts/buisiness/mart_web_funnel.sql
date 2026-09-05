select
    event_date,
    traffic_source,

    count(distinct session_id) as total_sessions,

    count(distinct case
        when event_type = 'view' then session_id
    end) as view_sessions,

    count(distinct case
        when event_type = 'search' then session_id
    end) as search_sessions,

    count(distinct case
        when event_type = 'add_to_cart' then session_id
    end) as add_to_cart_sessions,

    count(distinct case
        when event_type = 'checkout' then session_id
    end) as checkout_sessions,

    count(distinct case
        when event_type = 'purchase' then session_id
    end) as purchase_sessions,

    case
        when count(distinct session_id) = 0 then 0
        else
            count(distinct case
                when event_type = 'purchase' then session_id
            end)::decimal(18,4)
            / count(distinct session_id)
    end as session_conversion_rate

from {{ ref('fct_web_events') }}

group by
    event_date,
    traffic_source