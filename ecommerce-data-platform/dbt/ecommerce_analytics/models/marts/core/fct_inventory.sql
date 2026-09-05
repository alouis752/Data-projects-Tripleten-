with inventory as (

    select *
    from {{ ref('stg_inventory') }}

),

final as (

    select
        product_id,
        cast(snapshot_ts as date) as snapshot_date,
        snapshot_ts,
        quantity_on_hand,
        reorder_point,

        case
            when quantity_on_hand <= reorder_point then true
            else false
        end as is_below_reorder_point,

        quantity_on_hand - reorder_point as units_above_reorder_point

    from inventory

)

select *
from final