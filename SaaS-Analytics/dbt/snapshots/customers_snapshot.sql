{% snapshot customers_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='check',
        check_cols=['plan_tier', 'account_status']
    )
}}

select
    customer_id,
    company_name,
    plan_tier,
    account_status
from {{ ref('stg_customers') }}

{% endsnapshot %}