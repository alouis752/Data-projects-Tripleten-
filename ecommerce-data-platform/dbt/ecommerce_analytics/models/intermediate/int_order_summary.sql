with order_items as (

    select *
    from {{ ref('int_order_items') }}

),

order_summary as (

    select
        order_id,

        count(*) as line_item_count,
        sum(quantity) as total_quantity,
        sum(gross_item_amount) as gross_order_amount,
        sum(discount_amount) as discount_amount,
        sum(net_item_amount) as net_order_amount

    from order_items

    group by order_id

)

select *
from order_summary