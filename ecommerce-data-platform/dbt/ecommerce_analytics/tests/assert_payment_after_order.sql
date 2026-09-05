select
    p.payment_id,
    p.order_id,
    o.order_ts,
    p.payment_ts

from {{ ref('stg_payments') }} p

inner join {{ ref('stg_orders') }} o
    on p.order_id = o.order_id

where p.payment_ts < o.order_ts