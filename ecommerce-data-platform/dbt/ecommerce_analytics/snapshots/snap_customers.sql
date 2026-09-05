{% snapshot snap_customers %}

{{
    config(
        target_schema='MARTS',
        unique_key='customer_id',
        strategy='check',
        check_cols=[
            'customer_name',
            'email',
            'region',
            'segment',
            'status'
        ]
    )
}}

select
    customer_id,
    customer_name,
    email,
    created_at,
    region,
    segment,
    status

from {{ ref('stg_customers') }}

{% endsnapshot %}