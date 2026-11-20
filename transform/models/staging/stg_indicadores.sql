select
    serie,
    to_date(data, 'DD/MM/YYYY') as mes,
    cast(valor as numeric(10, 4)) as valor,
    extraido_em
from {{ source('raw', 'indicadores') }}
