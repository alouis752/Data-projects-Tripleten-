select
    spend_id,
    month,
    channel,
    spend_usd,
    leads_generated,
    impressions
from {{ source('raw', 'marketing_spend') }}