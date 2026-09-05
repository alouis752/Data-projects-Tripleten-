select
    order_id,
    recognized_revenue,
    return_amount

from {{ ref('fct_orders') }}

where round(return_amount, 2) > round(recognized_revenue, 2)