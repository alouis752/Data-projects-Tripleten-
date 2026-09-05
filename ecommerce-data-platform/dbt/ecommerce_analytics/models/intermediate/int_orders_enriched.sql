with orders as (

    select *
    from {{ ref('stg_orders') }}

),

order_summary as (

    select *
    from {{ ref('int_order_summary') }}

),

enriched as (

    select
        o.order_id,
        o.customer_id,
        o.order_ts,
        o.status,
        o.channel,

        s.line_item_count,
        s.total_quantity,
        s.gross_order_amount,
        s.discount_amount,
        s.net_order_amount

    from orders o

    left join order_summary s
        on o.order_id = s.order_id

)

select *
from enriched