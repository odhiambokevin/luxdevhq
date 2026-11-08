DELETE FROM dw.fact_cpi_overall WHERE date_key = to_char(%(month)s::date, 'YYYYMM')::integer;
DELETE FROM dw.fact_cpi_division WHERE date_key = to_char(%(month)s::date, 'YYYYMM')::integer;

INSERT INTO dw.fact_cpi_overall (
    date_key, overall_cpi, mom_change_pct, yoy_inflation_pct, core_inflation_pct,
    non_core_inflation_pct, run_id, source_file_sha256
)
SELECT to_char(report_date, 'YYYYMM')::integer, overall_cpi, mom_change, yoy_inflation,
       core_inflation, non_core_inflation, run_id, source_file_sha256
FROM staging.cpi_overall
WHERE report_date = %(month)s::date;

INSERT INTO dw.fact_cpi_division (
    date_key, division_name, weight, division_mom_pct, division_yoy_pct, run_id, source_file_sha256
)
SELECT to_char(report_date, 'YYYYMM')::integer, division_name, weight, division_mom, division_yoy,
       run_id, source_file_sha256
FROM staging.cpi_division
WHERE report_date = %(month)s::date;
