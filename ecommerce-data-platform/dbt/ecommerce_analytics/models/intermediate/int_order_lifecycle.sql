with payments as (

    select *
    from {{ ref('int_successful_payments') }}

),

shipments as (

    select *
    from {{ ref('stg_shipments') }}

),

returns as (

    select *
    from {{ ref('stg_returns') }}

),

shipment_summary as (

    select
        order_id,
        min(shipped_at) as shipped_at,
        max(delivered_at) as delivered_at,
        count(*) as shipment_count

    from shipments

    group by order_id
),

return_summary as (

    select
        order_id,
        count(*) as return_count,
        sum(return_amount) as return_amount

    from returns

    group by order_id
)

select
    o.order_id,

    coalesce(p.payment_attempt_count, 0) as payment_attempt_count,
    coalesce(p.successful_payment_amount, 0) as successful_payment_amount,
    coalesce(p.has_successful_payment, 0) as has_successful_payment,

    s.shipped_at,
    s.delivered_at,
    coalesce(s.shipment_count, 0) as shipment_count,

    coalesce(r.return_count, 0) as return_count,
    coalesce(r.return_amount, 0) as return_amount,

    case
        when coalesce(r.return_count, 0) > 0 then 1
        else 0
    end as has_return

from {{ ref('stg_orders') }} o

left join payments p
    on o.order_id = p.order_id

left join shipment_summary s
    on o.order_id = s.order_id

left join return_summary r
    on o.order_id = r.order_id