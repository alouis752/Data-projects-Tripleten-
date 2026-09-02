with orders as (

    select *
    from {{ ref('fct_sales_orders') }}

),

final as (

    select
        date_trunc('month', order_date) as month,

        sum(mrr_usd) as mrr_usd,

        sum(arr_usd) as arr_usd,

        count(distinct customer_id) as customers,

        count(distinct order_id) as orders

    from orders

    where lower(order_status) = 'completed'

    group by 1

)

select *
from final