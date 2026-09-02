select
    ticket_id,
    customer_id,
    created_date,
    resolved_date,
    category,
    severity,
    resolution_hours,
    satisfaction_score
from {{ ref('stg_support_tickets') }}