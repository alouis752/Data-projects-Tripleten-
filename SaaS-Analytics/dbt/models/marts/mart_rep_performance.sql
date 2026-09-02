with orders as (

    select *
    from {{ ref('fct_sales_orders') }}

),

employees as (

    select *
    from {{ ref('dim_employees') }}

),

sales_by_rep as (

    select
        sales_rep,

        count(distinct order_id) as total_orders,
        count(distinct customer_id) as customers_sold_to,

        sum(total_amount_usd) as total_bookings_usd,
        sum(mrr_usd) as total_mrr_usd,
        sum(arr_usd) as total_arr_usd,

        avg(total_amount_usd) as avg_order_value_usd,
        avg(discount_pct) as avg_discount_pct

    from orders

    where lower(order_status) = 'completed'

    group by sales_rep

),

final as (

    select
        e.employee_id,
        e.employee_name,
        e.team,
        e.title,
        e.manager_name,
        e.hire_date,
        e.quota_usd,

        coalesce(s.total_orders, 0) as total_orders,
        coalesce(s.customers_sold_to, 0) as customers_sold_to,
        coalesce(s.total_bookings_usd, 0) as total_bookings_usd,
        coalesce(s.total_mrr_usd, 0) as total_mrr_usd,
        coalesce(s.total_arr_usd, 0) as total_arr_usd,
        coalesce(s.avg_order_value_usd, 0) as avg_order_value_usd,
        coalesce(s.avg_discount_pct, 0) as avg_discount_pct,

        case
            when e.quota_usd > 0
            then coalesce(s.total_bookings_usd, 0) / e.quota_usd
            else null
        end as quota_attainment_pct

    from employees e

    left join sales_by_rep s
        on lower(trim(e.employee_name)) = lower(trim(s.sales_rep))

)

select *
from final