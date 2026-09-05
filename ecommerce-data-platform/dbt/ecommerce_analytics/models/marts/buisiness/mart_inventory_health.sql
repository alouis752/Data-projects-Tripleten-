with inventory as (

    select *
    from {{ ref('fct_inventory') }}

),

recent_sales as (

    select
        product_id,
        sum(quantity) as units_sold_30d
    from {{ ref('fct_order_items') }}

    where order_date between
        dateadd(day, -29, '2026-08-31'::date)
        and '2026-08-31'::date

    group by product_id

),

final as (

    select
        i.snapshot_date,
        i.product_id,
        p.product_name,
        p.category,

        i.quantity_on_hand,
        i.reorder_point,
        i.is_below_reorder_point,

        coalesce(s.units_sold_30d, 0) as units_sold_30d,

        coalesce(s.units_sold_30d, 0) / 30.0
            as avg_daily_units_sold_30d,

        case
            when coalesce(s.units_sold_30d, 0) = 0 then null
            else
                i.quantity_on_hand
                / (s.units_sold_30d / 30.0)
        end as days_of_supply

    from inventory i

    left join recent_sales s
        on i.product_id = s.product_id

    left join {{ ref('dim_products') }} p
        on i.product_id = p.product_id

)

select *
from final