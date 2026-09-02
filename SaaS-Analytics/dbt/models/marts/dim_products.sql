select
    product_id,
    product_name,
    category,
    plan_type,
    monthly_price_usd,
    annual_price_usd,
    launch_date
from {{ ref('stg_products') }}