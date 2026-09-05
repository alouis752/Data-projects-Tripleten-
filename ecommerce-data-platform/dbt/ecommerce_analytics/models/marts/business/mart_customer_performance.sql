with customers as (

    select *
    from {{ ref('dim_customers') }}

),

orders as (

    select *
    from {{ ref('fct_orders') }}

),

customer_metrics as (

    select
        customer_id,

        count(distinct order_id) as total_orders,

        count(distinct case
            when has_successful_payment = 1 then order_id
        end) as paid_orders,

        min(order_date) as first_order_date,
        max(order_date) as last_order_date,

        sum(net_order_amount) as lifetime_order_value,

        sum(recognized_revenue) as lifetime_recognized_revenue,

        sum(return_amount) as lifetime_return_amount,

        sum(net_revenue_after_returns)
            as lifetime_net_revenue,

        case
            when count(distinct case
                when has_successful_payment = 1 then order_id
            end) = 0 then null

            else
                sum(recognized_revenue)
                / count(distinct case
                    when has_successful_payment = 1 then order_id
                end)
        end as average_paid_order_value

    from orders

    group by customer_id

),

final as (

    select
        c.customer_id,
        c.customer_name,
        c.region,
        c.segment,
        c.status,

        coalesce(m.total_orders, 0) as total_orders,
        coalesce(m.paid_orders, 0) as paid_orders,

        m.first_order_date,
        m.last_order_date,

        coalesce(m.lifetime_order_value, 0)
            as lifetime_order_value,

        coalesce(m.lifetime_recognized_revenue, 0)
            as lifetime_recognized_revenue,

        coalesce(m.lifetime_return_amount, 0)
            as lifetime_return_amount,

        coalesce(m.lifetime_net_revenue, 0)
            as lifetime_net_revenue,

        m.average_paid_order_value

    from customers c

    left join customer_metrics m
        on c.customer_id = m.customer_id

)

select *
from final