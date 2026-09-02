-- Using intermediate to provide MRR and ARR calculations 

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
    sales_rep,
    product_name,
    category,
    plan_type,
    mrr_usd,
    arr_usd
from {{ ref('int_order_metrics') }}