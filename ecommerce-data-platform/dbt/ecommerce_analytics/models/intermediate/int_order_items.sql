with order_items as (

    select *
    from {{ ref('stg_order_items') }}

),

calculated as (

    select
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price,
        discount,

        quantity * unit_price as gross_item_amount,

        quantity * unit_price * discount as discount_amount,

        quantity * unit_price * (1 - discount) as net_item_amount

    from order_items

)

select *
from calculated