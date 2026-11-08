INSERT INTO dw.dim_market (market_id, market_name, county_key, admin1, admin2, latitude, longitude, updated_at)
SELECT DISTINCT ON (s.market_id)
       s.market_id, s.market_name, c.county_key, s.admin1, s.admin2, s.latitude, s.longitude, now()
FROM staging.price_observation s
JOIN dw.dim_county c ON c.county_code = s.county_code
WHERE s.month_start = %(month)s::date
ORDER BY s.market_id, s.obs_date DESC
ON CONFLICT (market_id) DO UPDATE SET
    market_name = EXCLUDED.market_name,
    county_key  = EXCLUDED.county_key,
    admin1      = EXCLUDED.admin1,
    admin2      = EXCLUDED.admin2,
    latitude    = EXCLUDED.latitude,
    longitude   = EXCLUDED.longitude,
    updated_at  = now();
