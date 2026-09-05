with ranked_customers as (

    select

        customer_id,
        customer_name,
        email,
        created_at,
        region,
        segment,
        status,
        source_file,
        load_ts,

        row_number() over (
            partition by customer_id
            order by load_ts desc, source_file desc
        ) as row_num

    from {{ source('raw', 'customers') }}

)

select

    customer_id,
    customer_name,
    email,
    created_at,
    region,
    segment,
    status,
    source_file,
    load_ts

from ranked_customers

where row_num = 1