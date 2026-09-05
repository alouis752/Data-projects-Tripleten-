with date_spine as (

    select
        dateadd(
            day,
            seq4(),
            '2026-01-01'::date
        ) as date_day

    from table(generator(rowcount => 1095))

),

final as (

    select
        date_day,

        year(date_day) as year,
        quarter(date_day) as quarter,
        month(date_day) as month_number,
        monthname(date_day) as month_name,

        day(date_day) as day_of_month,
        dayofweekiso(date_day) as day_of_week_number,
        dayname(date_day) as day_of_week_name,

        weekiso(date_day) as week_number,

        case
            when dayofweekiso(date_day) in (6, 7) then true
            else false
        end as is_weekend

    from date_spine

)

select *
from final