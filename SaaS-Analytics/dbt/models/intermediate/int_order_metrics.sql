with orders as (

    select *
    from {{ ref('stg_sales_orders') }}

),

products as (

    select *
    from {{ ref('stg_products') }}

),

final as (

    select
        o.order_id,
        o.customer_id,
        o.product_id,
        o.order_date,
        o.quantity,
        o.unit_price_usd,
        o.discount_pct,
        o.total_amount_usd,
        o.order_status,
        o.billing_frequency,
        o.payment_method,
        o.sales_rep,

        p.product_name,
        p.category,
        p.plan_type,

        case
            when lower(o.billing_frequency) = 'monthly'
                then o.total_amount_usd
            when lower(o.billing_frequency) = 'annual'
                then o.total_amount_usd / 12
            else 0
        end as mrr_usd,

        case
            when lower(o.billing_frequency) = 'monthly'
                then o.total_amount_usd * 12
            when lower(o.billing_frequency) = 'annual'
                then o.total_amount_usd
            else 0
        end as arr_usd

    from orders o

    left join products p
        on o.product_id = p.product_id

)

select *
from final