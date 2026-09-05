select
    order_date,

    count(distinct order_id) as order_count,
    count(distinct customer_id) as customer_count,

    sum(gross_order_amount) as gross_order_value,
    sum(net_order_amount) as net_order_value,

    sum(recognized_revenue) as recognized_revenue,
    sum(return_amount) as return_amount,
    sum(net_revenue_after_returns) as net_revenue_after_returns,

    avg(
        case
            when has_successful_payment = 1
                then net_order_amount
        end
    ) as average_paid_order_value

from {{ ref('fct_orders') }}

group by order_date