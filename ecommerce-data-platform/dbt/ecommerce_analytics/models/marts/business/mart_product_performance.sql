select
    p.product_id,
    p.product_name,
    p.category,

    count(distinct oi.order_id) as order_count,
    sum(oi.quantity) as units_sold,

    sum(oi.gross_item_amount) as gross_revenue,
    sum(oi.discount_amount) as discount_amount,
    sum(oi.net_item_amount) as net_revenue,

    avg(oi.unit_price) as average_selling_price,

    sum(oi.net_item_amount - (p.cost * oi.quantity)) as gross_profit,

    case
        when sum(oi.net_item_amount) = 0 then 0
        else
            sum(oi.net_item_amount - (p.cost * oi.quantity))
            / sum(oi.net_item_amount)
    end as gross_margin_pct

from {{ ref('fct_order_items') }} oi

inner join {{ ref('dim_products') }} p
    on oi.product_id = p.product_id

group by
    p.product_id,
    p.product_name,
    p.category