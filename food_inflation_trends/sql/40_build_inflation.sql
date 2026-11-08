DELETE FROM dw.fact_price_inflation
WHERE date_key IN (
    to_char(%(month)s::date, 'YYYYMM')::integer,
    to_char(%(month)s::date + interval '1 month', 'YYYYMM')::integer,
    to_char(%(month)s::date + interval '12 months', 'YYYYMM')::integer
);

INSERT INTO dw.fact_price_inflation (
    date_key, county_key, commodity_group, price_type, is_staple,
    n_markets, n_series, median_yoy_pct, median_mom_pct, avg_price_per_base_kes
)
SELECT f.date_key,
       f.county_key,
       c.commodity_group,
       f.price_type,
       bool_or(c.is_staple),
       count(DISTINCT f.market_key),
       count(*),
       round((percentile_cont(0.5) WITHIN GROUP (ORDER BY f.yoy_change_pct))::numeric, 2),
       round((percentile_cont(0.5) WITHIN GROUP (ORDER BY f.mom_change_pct))::numeric, 2),
       round(avg(f.price_per_base_kes), 4)
FROM dw.fact_food_price f
JOIN dw.dim_commodity c ON c.commodity_key = f.commodity_key
WHERE c.is_food
  AND f.date_key IN (
    to_char(%(month)s::date, 'YYYYMM')::integer,
    to_char(%(month)s::date + interval '1 month', 'YYYYMM')::integer,
    to_char(%(month)s::date + interval '12 months', 'YYYYMM')::integer
  )
GROUP BY f.date_key, f.county_key, c.commodity_group, f.price_type;
