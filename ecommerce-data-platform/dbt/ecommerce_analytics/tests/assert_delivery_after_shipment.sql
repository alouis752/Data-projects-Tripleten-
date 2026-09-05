select
    shipment_id,
    order_id,
    shipped_at,
    delivered_at

from {{ ref('stg_shipments') }}

where delivered_at is not null
  and delivered_at < shipped_at