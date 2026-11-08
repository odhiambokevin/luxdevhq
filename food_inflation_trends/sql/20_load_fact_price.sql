DELETE FROM dw.fact_food_price
WHERE date_key = to_char(%(month)s::date, 'YYYYMM')::integer;

INSERT INTO dw.fact_food_price (
    date_key, obs_date, county_key, market_key, commodity_key, unit_key, source_key,
    price_type, price_flag, price_kes, price_usd, price_per_base_kes, base_unit,
    unit_convertible, run_id, source_file_sha256
)
SELECT to_char(s.month_start, 'YYYYMM')::integer,
       s.obs_date,
       m.county_key,
       m.market_key,
       cm.commodity_key,
       u.unit_key,
       src.source_key,
       s.price_type,
       s.price_flag,
       s.price,
       s.price_usd,
       s.price_per_base,
       s.base_unit,
       s.unit_convertible,
       s.run_id,
       s.source_file_sha256
FROM staging.price_observation s
JOIN dw.dim_market m ON m.market_id = s.market_id
JOIN dw.dim_commodity cm ON cm.commodity_id = s.commodity_id
JOIN dw.dim_unit u ON u.unit_code = s.unit_code
JOIN dw.dim_source src ON src.source_code = 'wfp_food_prices_ken'
WHERE s.month_start = %(month)s::date;
