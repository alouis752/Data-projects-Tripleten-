select
    payment_id,
    order_id,
    customer_id,
    invoice_date,
    payment_date,
    amount_usd,
    payment_status,
    days_late
from {{ ref('stg_payments') }}