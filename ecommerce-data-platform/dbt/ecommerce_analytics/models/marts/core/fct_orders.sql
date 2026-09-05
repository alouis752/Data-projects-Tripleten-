with orders as (
    select *
    from {{ ref('int_orders_enriched') }}
),

lifecycle as (
    select *
    from {{ ref('int_order_lifecycle') }}
),

final as (
    select
        o.order_id,
        o.customer_id,
        o.order_ts,
        cast(o.order_ts as date) as order_date,
        o.status as order_status,
        o.channel,

        -- Order value
        o.line_item_count,
        o.total_quantity,
        o.gross_order_amount,
        o.discount_amount,
        o.net_order_amount,

        -- Payment lifecycle
        l.payment_attempt_count,
        l.successful_payment_amount,
        l.has_successful_payment,

        -- Fulfillment lifecycle
        l.shipped_at,
        l.delivered_at,
        l.shipment_count,

        -- Returns
        l.return_count,
        l.return_amount,
        l.has_return,

        -- Revenue is only recognized for successfully paid orders
        case
            when l.has_successful_payment = 1
                then o.net_order_amount
            else 0
        end as recognized_revenue,

        -- Revenue remaining after returns
        case
            when l.has_successful_payment = 1
                then greatest(
                    o.net_order_amount - coalesce(l.return_amount, 0),
                    0
                )
            else 0
        end as net_revenue_after_returns

    from orders o

    left join lifecycle l
        on o.order_id = l.order_id
)

select *
from final