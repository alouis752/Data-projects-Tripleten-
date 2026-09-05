select
    product_id,
    product_name,
    category,
    price,
    cost,
    active_flag
from {{ ref('stg_products') }}