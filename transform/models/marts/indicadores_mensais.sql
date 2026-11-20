with pivot as (
    select
        mes,
        max(case when serie = 'ipca' then valor end) as ipca,
        max(case when serie = 'selic' then valor end) as selic
    from {{ ref('stg_indicadores') }}
    group by mes
)

select
    mes,
    ipca,
    selic,
    -- IPCA acumulado em 12 meses → multiplica (1 + taxa) dos últimos 12 meses
    round(
        (exp(sum(ln(1 + ipca / 100)) over (order by mes rows between 11 preceding and current row)) - 1) * 100,
        2
    ) as ipca_12m,
    round(selic - ipca, 2) as juro_real_mes
from pivot
where ipca is not null and selic is not null
order by mes
