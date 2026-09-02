select
    employee_id,
    employee_name,
    team,
    title,
    hire_date,
    quota_usd,
    manager_name
from {{ source('raw', 'employees') }}