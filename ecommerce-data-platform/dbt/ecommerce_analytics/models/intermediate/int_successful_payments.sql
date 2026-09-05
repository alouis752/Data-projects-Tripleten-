{{ config(materialized='ephemeral') }}

select
    order_id,
    count(*) as payment_attempt_count,

    sum(
        case
            when payment_status = 'successful'
                then amount
            else 0
        end
    ) as successful_payment_amount,

    max(
        case
            when payment_status = 'successful'
                then 1
            else 0
        end
    ) as has_successful_payment

from {{ ref('stg_payments') }}

group by order_id