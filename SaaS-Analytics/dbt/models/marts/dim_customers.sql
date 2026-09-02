with customers as (

    select *
    from {{ ref('stg_customers') }}

),

usage_summary as (

    select *
    from {{ ref('int_customer_usage_summary') }}

),

final as (

    select
        c.customer_id,
        c.company_name,
        c.industry,
        c.region,
        c.country,
        c.plan_tier,
        c.employee_count,
        c.signup_date,
        c.account_status,
        c.account_owner,

        coalesce(u.total_usage_events, 0) as total_usage_events,
        coalesce(u.total_usage_count, 0) as total_usage_count,
        u.avg_session_duration_minutes,
        u.last_usage_date,
        coalesce(u.products_used, 0) as products_used,
        coalesce(u.features_used, 0) as features_used

    from customers c

    left join usage_summary u
        on c.customer_id = u.customer_id

)

select *
from final