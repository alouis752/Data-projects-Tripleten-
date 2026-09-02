with customers as (

    select
        customer_id,
        signup_date,
        date_trunc('month', signup_date) as signup_month
    from {{ ref('dim_customers') }}

),

customer_revenue as (

    select
        customer_id,
        sum(total_amount_usd) as lifetime_revenue_usd,
        sum(arr_usd) as lifetime_arr_usd
    from {{ ref('fct_sales_orders') }}
    where lower(order_status) = 'completed'
    group by customer_id

),

cohorts as (

    select
        c.signup_month,

        count(distinct c.customer_id) as new_customers,

        avg(coalesce(r.lifetime_revenue_usd, 0)) as avg_ltv_usd,

        avg(coalesce(r.lifetime_arr_usd, 0)) as avg_lifetime_arr_usd

    from customers c

    left join customer_revenue r
        on c.customer_id = r.customer_id

    group by c.signup_month

),

marketing as (

    select
        date_trunc('month', month) as month,

        sum(spend_usd) as marketing_spend_usd,
        sum(leads_generated) as leads_generated,
        sum(impressions) as impressions

    from {{ ref('stg_marketing_spend') }}

    group by 1

),

final as (

    select
        c.signup_month as month,

        c.new_customers,

        coalesce(m.marketing_spend_usd, 0) as marketing_spend_usd,
        coalesce(m.leads_generated, 0) as leads_generated,
        coalesce(m.impressions, 0) as impressions,

        case
            when c.new_customers > 0
            then coalesce(m.marketing_spend_usd, 0) / c.new_customers
            else null
        end as cac_usd,

        c.avg_ltv_usd,
        c.avg_lifetime_arr_usd,

        case
            when coalesce(m.marketing_spend_usd, 0) > 0
                 and c.new_customers > 0
            then c.avg_ltv_usd /
                 (m.marketing_spend_usd / c.new_customers)
            else null
        end as ltv_to_cac_ratio

    from cohorts c

    left join marketing m
        on c.signup_month = m.month

)

select *
from final
order by month