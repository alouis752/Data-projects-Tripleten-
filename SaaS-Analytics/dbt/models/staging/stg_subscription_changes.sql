select
    change_id,
    customer_id,
    change_date,
    change_type,
    old_plan_tier,
    new_plan_tier,
    reason
from {{ source('raw', 'subscription_changes') }}