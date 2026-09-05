with ranked_products as (

    select

        product_id,
        product_name,
        category,
        price,
        cost,
        active_flag,
        source_file,
        load_ts,

        row_number() over (
            partition by product_id
            order by load_ts desc, source_file desc
        ) as row_num

    from {{ source('raw', 'products') }}

)

select

    product_id,
    product_name,
    category,
    price,
    cost,
    active_flag,
    source_file,
    load_ts

from ranked_products

where row_num = 1