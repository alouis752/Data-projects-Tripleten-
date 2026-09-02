select
    employee_id,
    employee_name,
    team,
    title,
    hire_date,
    quota_usd,
    manager_name
from {{ ref('stg_employees') }}