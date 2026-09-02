select
    customer_id,
    company_name,
    industry,
    region,
    country,
    plan_tier,
    employee_count,
    signup_date,
    account_status,
    account_owner
from {{ source('raw', 'customers') }}