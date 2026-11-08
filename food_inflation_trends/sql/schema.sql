CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS dw;
CREATE SCHEMA IF NOT EXISTS meta;

-- Staging -------------------------------------------------------------------

CREATE TABLE staging.price_observation (
    obs_date            date        NOT NULL,
    month_start         date        NOT NULL,
    market_id           integer     NOT NULL,
    market_name         text        NOT NULL,
    admin1              text,
    admin2              text,
    county_code         integer     NOT NULL,
    latitude            numeric(9, 5),
    longitude           numeric(9, 5),
    commodity_id        integer     NOT NULL,
    unit_code           text        NOT NULL,
    price_type          text        NOT NULL,
    price_flag          text,
    currency            text        NOT NULL,
    price               numeric(14, 4) NOT NULL,
    price_usd           numeric(14, 4),
    price_per_base      numeric(14, 4),
    base_unit           text        NOT NULL,
    unit_convertible    boolean     NOT NULL,
    run_id              text        NOT NULL,
    source_file_sha256  text        NOT NULL
);
CREATE INDEX ix_stg_price_month ON staging.price_observation (month_start);

CREATE TABLE staging.price_rejected (
    month_start         date        NOT NULL,
    reject_reason       text        NOT NULL,
    raw_json            jsonb       NOT NULL,
    run_id              text        NOT NULL,
    source_file_sha256  text        NOT NULL
);
CREATE INDEX ix_stg_rejected_month ON staging.price_rejected (month_start);

CREATE TABLE staging.cpi_overall (
    report_date         date        NOT NULL,
    overall_cpi         numeric(10, 2),
    mom_change          numeric(8, 2),
    yoy_inflation       numeric(8, 2),
    core_inflation      numeric(8, 2),
    non_core_inflation  numeric(8, 2),
    run_id              text        NOT NULL,
    source_file_sha256  text        NOT NULL
);

CREATE TABLE staging.cpi_division (
    report_date         date        NOT NULL,
    division_name       text        NOT NULL,
    weight              numeric(10, 4),
    division_mom        numeric(8, 2),
    division_yoy        numeric(8, 2),
    run_id              text        NOT NULL,
    source_file_sha256  text        NOT NULL
);

-- Dimensions ----------------------------------------------------------------

CREATE TABLE dw.dim_date (
    date_key      integer PRIMARY KEY,
    month_start   date    NOT NULL UNIQUE,
    year          integer NOT NULL,
    quarter       integer NOT NULL,
    month_number  integer NOT NULL,
    month_name    text    NOT NULL
);

INSERT INTO dw.dim_date (date_key, month_start, year, quarter, month_number, month_name)
SELECT to_char(g.d, 'YYYYMM')::integer,
       g.d::date,
       extract(year FROM g.d)::integer,
       extract(quarter FROM g.d)::integer,
       extract(month FROM g.d)::integer,
       trim(to_char(g.d, 'Month'))
FROM generate_series('2006-01-01'::date, '2035-12-01'::date, interval '1 month') AS g(d);

CREATE TABLE dw.dim_county (
    county_key   integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    county_code  integer NOT NULL UNIQUE,
    county_name  text    NOT NULL UNIQUE,
    province     text    NOT NULL
);

CREATE TABLE dw.dim_market (
    market_key   integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    market_id    integer NOT NULL UNIQUE,
    market_name  text    NOT NULL,
    county_key   integer NOT NULL REFERENCES dw.dim_county (county_key),
    admin1       text,
    admin2       text,
    latitude     numeric(9, 5),
    longitude    numeric(9, 5),
    updated_at   timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE dw.dim_commodity (
    commodity_key    integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    commodity_id     integer NOT NULL UNIQUE,
    commodity_name   text    NOT NULL,
    commodity_group  text    NOT NULL,
    category         text    NOT NULL,
    is_food          boolean NOT NULL,
    is_staple        boolean NOT NULL
);

CREATE TABLE dw.dim_unit (
    unit_key    integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    unit_code   text    NOT NULL UNIQUE,
    quantity    numeric(10, 3),
    base_unit   text    NOT NULL
);

CREATE TABLE dw.dim_source (
    source_key   integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_code  text NOT NULL UNIQUE,
    source_name  text NOT NULL
);

INSERT INTO dw.dim_source (source_code, source_name) VALUES
    ('wfp_food_prices_ken', 'WFP Kenya Food Prices (HDX)'),
    ('knbs_cpi_monthly', 'KNBS monthly CPI and inflation (compiled extract)');

-- Facts ---------------------------------------------------------------------

CREATE TABLE dw.fact_food_price (
    price_key           bigint  GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    date_key            integer NOT NULL REFERENCES dw.dim_date (date_key),
    obs_date            date    NOT NULL,
    county_key          integer NOT NULL REFERENCES dw.dim_county (county_key),
    market_key          integer NOT NULL REFERENCES dw.dim_market (market_key),
    commodity_key       integer NOT NULL REFERENCES dw.dim_commodity (commodity_key),
    unit_key            integer NOT NULL REFERENCES dw.dim_unit (unit_key),
    source_key          integer NOT NULL REFERENCES dw.dim_source (source_key),
    price_type          text    NOT NULL,
    price_flag          text,
    price_kes           numeric(14, 4) NOT NULL,
    price_usd           numeric(14, 4),
    price_per_base_kes  numeric(14, 4),
    base_unit           text    NOT NULL,
    unit_convertible    boolean NOT NULL,
    mom_change_pct      numeric(10, 2),
    yoy_change_pct      numeric(10, 2),
    is_outlier          boolean NOT NULL DEFAULT false,
    run_id              text    NOT NULL,
    source_file_sha256  text    NOT NULL,
    loaded_at           timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT uq_fact_food_price_nk
        UNIQUE (date_key, market_key, commodity_key, unit_key, price_type)
);
CREATE INDEX ix_fact_price_county ON dw.fact_food_price (county_key, commodity_key, date_key);

CREATE TABLE dw.fact_price_inflation (
    date_key                integer NOT NULL REFERENCES dw.dim_date (date_key),
    county_key              integer NOT NULL REFERENCES dw.dim_county (county_key),
    commodity_group         text    NOT NULL,
    price_type              text    NOT NULL,
    is_staple               boolean NOT NULL,
    n_markets               integer NOT NULL,
    n_series                integer NOT NULL,
    median_yoy_pct          numeric(10, 2),
    median_mom_pct          numeric(10, 2),
    avg_price_per_base_kes  numeric(14, 4),
    PRIMARY KEY (date_key, county_key, commodity_group, price_type)
);

CREATE TABLE dw.fact_cpi_overall (
    date_key            integer PRIMARY KEY REFERENCES dw.dim_date (date_key),
    overall_cpi         numeric(10, 2),
    mom_change_pct      numeric(8, 2),
    yoy_inflation_pct   numeric(8, 2),
    core_inflation_pct  numeric(8, 2),
    non_core_inflation_pct numeric(8, 2),
    run_id              text NOT NULL,
    source_file_sha256  text NOT NULL
);

CREATE TABLE dw.fact_cpi_division (
    date_key            integer NOT NULL REFERENCES dw.dim_date (date_key),
    division_name       text    NOT NULL,
    weight              numeric(10, 4),
    division_mom_pct    numeric(8, 2),
    division_yoy_pct    numeric(8, 2),
    run_id              text NOT NULL,
    source_file_sha256  text NOT NULL,
    PRIMARY KEY (date_key, division_name)
);

-- Metadata and lineage ------------------------------------------------------

CREATE TABLE meta.source_registry (
    source_code        text PRIMARY KEY,
    source_name        text NOT NULL,
    publisher          text NOT NULL,
    landing_url        text NOT NULL,
    license            text NOT NULL,
    update_frequency   text NOT NULL,
    granularity        text NOT NULL,
    validation_steps   text NOT NULL,
    known_limitations  text NOT NULL
);

INSERT INTO meta.source_registry VALUES
(
    'wfp_food_prices_ken',
    'WFP Kenya Food Prices (HDX)',
    'World Food Programme, via the Humanitarian Data Exchange',
    'https://data.humdata.org/dataset/wfp-food-prices-for-kenya',
    'Creative Commons Attribution for Intergovernmental Organisations',
    'Monthly (irregular market coverage per month)',
    'Market x commodity x unit x price type x month',
    'Required columns; date parse; positive KES price; county mapping; unit conversion; duplicate natural key; reject-rate threshold; month reconciliation',
    'Market panel is concentrated in arid and semi-arid counties; coverage changes year to year; not nationally representative'
),
(
    'knbs_cpi_monthly',
    'KNBS monthly CPI and inflation (compiled extract)',
    'Kenya National Bureau of Statistics (compiled extract supplied with the project)',
    'https://www.knbs.or.ke/',
    'To be confirmed against KNBS terms of use',
    'Monthly',
    'National, by COICOP division',
    'Required columns; date parse; month reconciliation',
    'National index only; no county breakdown; extract provenance to be confirmed'
);

CREATE TABLE meta.source_snapshot (
    sha256         text PRIMARY KEY,
    source_code    text NOT NULL REFERENCES meta.source_registry (source_code),
    file_name      text NOT NULL,
    size_bytes     bigint NOT NULL,
    snapshot_path  text NOT NULL,
    fetched_at     timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE meta.pipeline_runs (
    dag_id               text NOT NULL,
    data_interval_start  date NOT NULL,
    data_interval_end    date,
    dag_run_id           text NOT NULL,
    status               text NOT NULL,
    source_file_sha256   text,
    rows_read            integer,
    rows_loaded          integer,
    rows_rejected        integer,
    details              jsonb NOT NULL DEFAULT '{}'::jsonb,
    updated_at           timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (dag_id, data_interval_start)
);

CREATE TABLE meta.validation_result (
    dag_id               text NOT NULL,
    data_interval_start  date NOT NULL,
    check_name           text NOT NULL,
    stage                text NOT NULL,
    severity             text NOT NULL,
    passed               boolean NOT NULL,
    observed             text,
    threshold            text,
    checked_at           timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (dag_id, data_interval_start, check_name)
);

-- Reporting views -----------------------------------------------------------

CREATE VIEW dw.v_price_trend AS
SELECT d.month_start::timestamp AS month,
       co.county_name,
       co.province,
       c.commodity_group,
       f.price_type,
       min(f.base_unit) AS base_unit,
       round(avg(f.price_per_base_kes), 2) AS avg_price_per_base_kes,
       count(*) AS n_obs
FROM dw.fact_food_price f
JOIN dw.dim_date d ON d.date_key = f.date_key
JOIN dw.dim_county co ON co.county_key = f.county_key
JOIN dw.dim_commodity c ON c.commodity_key = f.commodity_key
WHERE f.price_per_base_kes IS NOT NULL AND c.is_food
GROUP BY d.month_start, co.county_name, co.province, c.commodity_group, f.price_type;

CREATE VIEW dw.v_inflation_county_month AS
SELECT d.month_start::timestamp AS month,
       co.county_name,
       co.province,
       i.commodity_group,
       i.price_type,
       i.n_markets,
       i.median_yoy_pct,
       i.median_mom_pct
FROM dw.fact_price_inflation i
JOIN dw.dim_date d ON d.date_key = i.date_key
JOIN dw.dim_county co ON co.county_key = i.county_key
UNION ALL
SELECT d.month_start::timestamp,
       co.county_name,
       co.province,
       'All staples',
       i.price_type,
       sum(i.n_markets)::integer,
       round((percentile_cont(0.5) WITHIN GROUP (ORDER BY i.median_yoy_pct))::numeric, 2),
       round((percentile_cont(0.5) WITHIN GROUP (ORDER BY i.median_mom_pct))::numeric, 2)
FROM dw.fact_price_inflation i
JOIN dw.dim_date d ON d.date_key = i.date_key
JOIN dw.dim_county co ON co.county_key = i.county_key
WHERE i.is_staple
GROUP BY d.month_start, co.county_name, co.province, i.price_type;

CREATE VIEW dw.v_cpi_monthly AS
SELECT d.month_start::timestamp AS month,
       o.overall_cpi,
       o.yoy_inflation_pct AS overall_yoy_pct,
       o.core_inflation_pct,
       o.non_core_inflation_pct,
       fd.division_yoy_pct AS food_yoy_pct,
       fd.division_mom_pct AS food_mom_pct
FROM dw.fact_cpi_overall o
JOIN dw.dim_date d ON d.date_key = o.date_key
LEFT JOIN dw.fact_cpi_division fd
       ON fd.date_key = o.date_key
      AND fd.division_name = 'Food and Non-Alcoholic Beverages';

CREATE VIEW dw.v_county_coverage AS
SELECT co.county_name,
       co.province,
       count(DISTINCT f.market_key) AS n_markets,
       count(*) AS n_observations,
       min(d.month_start) AS first_month,
       max(d.month_start) AS last_month
FROM dw.dim_county co
LEFT JOIN dw.fact_food_price f ON f.county_key = co.county_key
LEFT JOIN dw.dim_date d ON d.date_key = f.date_key
GROUP BY co.county_name, co.province;

-- Read-only role for Grafana --------------------------------------------------

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'grafana_reader') THEN
        CREATE ROLE grafana_reader LOGIN PASSWORD 'grafana_reader';
    END IF;
END
$$;

GRANT USAGE ON SCHEMA dw, meta TO grafana_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA dw, meta TO grafana_reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA dw, meta GRANT SELECT ON TABLES TO grafana_reader;
