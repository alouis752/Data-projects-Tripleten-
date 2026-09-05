with order_items as (

    select *
    from {{ ref('int_order_items') }}

),

orders as (

    select
        order_id,
        customer_id,
        order_ts,
        status,
        channel
    from {{ ref('stg_orders') }}

),

final as (

    select
        oi.order_item_id,
        oi.order_id,
        o.customer_id,
        oi.product_id,

        o.order_ts,
        cast(o.order_ts as date) as order_date,
        o.status as order_status,
        o.channel,

        oi.quantity,
        oi.unit_price,
        oi.discount,

        oi.gross_item_amount,
        oi.discount_amount,
        oi.net_item_amount

    from order_items oi

    inner join orders o
        on oi.order_id = o.order_id

)

select *
from final