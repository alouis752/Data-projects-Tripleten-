with customers as (

    select *
    from {{ ref('dim_customers') }}

),

tickets as (

    select
        customer_id,
        count(*) as total_support_tickets,
        avg(resolution_hours) as avg_resolution_hours,
        avg(satisfaction_score) as avg_satisfaction_score,
        sum(
            case
                when lower(severity) = 'critical' then 1
                else 0
            end
        ) as critical_tickets

    from {{ ref('fct_support_tickets') }}

    group by customer_id

),

payments as (

    select
        customer_id,

        count(*) as total_payments,

        sum(
            case
                when lower(payment_status) = 'paid' then 1
                else 0
            end
        ) as successful_payments,

        sum(
            case
                when days_late > 0 then 1
                else 0
            end
        ) as late_payments,

        avg(coalesce(days_late, 0)) as avg_days_late

    from {{ ref('fct_payments') }}

    group by customer_id

),

subscription_changes as (

    select
        customer_id,

        max(change_date) as last_subscription_change_date,

        sum(
            case
                when lower(change_type) = 'upgrade' then 1
                else 0
            end
        ) as upgrades,

        sum(
            case
                when lower(change_type) = 'downgrade' then 1
                else 0
            end
        ) as downgrades,

        sum(
            case
                when lower(change_type) = 'cancellation' then 1
                else 0
            end
        ) as cancellations

    from {{ ref('fct_subscription_changes') }}

    group by customer_id

),

final as (

    select
        c.customer_id,
        c.company_name,
        c.industry,
        c.region,
        c.plan_tier,
        c.account_status,
        c.account_owner,

        c.total_usage_events,
        c.total_usage_count,
        c.avg_session_duration_minutes,
        c.last_usage_date,
        c.products_used,
        c.features_used,

        coalesce(t.total_support_tickets, 0) as total_support_tickets,
        t.avg_resolution_hours,
        t.avg_satisfaction_score,
        coalesce(t.critical_tickets, 0) as critical_tickets,

        coalesce(p.total_payments, 0) as total_payments,
        coalesce(p.successful_payments, 0) as successful_payments,
        coalesce(p.late_payments, 0) as late_payments,
        coalesce(p.avg_days_late, 0) as avg_days_late,

        s.last_subscription_change_date,
        coalesce(s.upgrades, 0) as upgrades,
        coalesce(s.downgrades, 0) as downgrades,
        coalesce(s.cancellations, 0) as cancellations,

        case
            when lower(c.account_status) <> 'active'
                then 'High Risk'

            when coalesce(s.cancellations, 0) > 0
                then 'High Risk'

            when coalesce(p.late_payments, 0) >= 2
                or coalesce(t.critical_tickets, 0) >= 2
                or coalesce(s.downgrades, 0) >= 1
                then 'Medium Risk'

            else 'Healthy'
        end as customer_health_status

    from customers c

    left join tickets t
        on c.customer_id = t.customer_id

    left join payments p
        on c.customer_id = p.customer_id

    left join subscription_changes s
        on c.customer_id = s.customer_id

)

select *
from final