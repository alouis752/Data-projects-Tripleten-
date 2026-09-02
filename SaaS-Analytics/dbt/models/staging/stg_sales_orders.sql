select
    order_id,
    customer_id,
    product_id,
    order_date,
    quantity,
    unit_price_usd,
    discount_pct,
    total_amount_usd,
    order_status,
    billing_frequency,
    payment_method,
    sales_rep
from {{ source('raw', 'sales_orders') }}