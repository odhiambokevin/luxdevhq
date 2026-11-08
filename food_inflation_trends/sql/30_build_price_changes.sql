WITH scope AS (
    SELECT f.price_key, f.market_key, f.commodity_key, f.unit_key, f.price_type,
           d.month_start, f.price_kes
    FROM dw.fact_food_price f
    JOIN dw.dim_date d ON d.date_key = f.date_key
    WHERE d.month_start IN (
        %(month)s::date,
        (%(month)s::date + interval '1 month')::date,
        (%(month)s::date + interval '12 months')::date
    )
),
calc AS (
    SELECT s.price_key,
           round(((s.price_kes / nullif(prev.price_kes, 0)) - 1) * 100, 2) AS mom,
           round(((s.price_kes / nullif(yago.price_kes, 0)) - 1) * 100, 2) AS yoy
    FROM scope s
    LEFT JOIN dw.fact_food_price prev
           ON prev.market_key = s.market_key
          AND prev.commodity_key = s.commodity_key
          AND prev.unit_key = s.unit_key
          AND prev.price_type = s.price_type
          AND prev.date_key = to_char(s.month_start - interval '1 month', 'YYYYMM')::integer
    LEFT JOIN dw.fact_food_price yago
           ON yago.market_key = s.market_key
          AND yago.commodity_key = s.commodity_key
          AND yago.unit_key = s.unit_key
          AND yago.price_type = s.price_type
          AND yago.date_key = to_char(s.month_start - interval '12 months', 'YYYYMM')::integer
)
UPDATE dw.fact_food_price f
SET mom_change_pct = c.mom,
    yoy_change_pct = c.yoy,
    is_outlier = coalesce(abs(c.mom) > 50, false)
FROM calc c
WHERE f.price_key = c.price_key;
