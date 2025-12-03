# ---
# ## Q3 – SQL: Deduplicate and Choose Latest Model Version

# **Problem**: Query a model runs table to find the latest run per model version, then find the best version per family.

# **Schema**:
# ```sql
# model_runs(
#   model_family   TEXT,
#   model_version  TEXT,
#   run_ts         TIMESTAMP,
#   elpd           DOUBLE PRECISION
# );
# ```




# TODO: Write SQL queries
# Query 1: Latest run per (family, version)
# Query 2: Best version by ELPD for each model_family
import duckdb




-- Latest run per (model_family, model_version)
SELECT
  model_family,
  model_version,
  run_ts,
  elpd
FROM (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY model_family, model_version
      ORDER BY run_ts DESC
    ) AS rn
  FROM model_runs
) t
WHERE rn = 1;

-- Best model_version per model_family by ELPD
WITH latest_per_version AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY model_family, model_version
      ORDER BY run_ts DESC
    ) AS rn
  FROM model_runs
)
SELECT
  model_family,
  model_version,
  run_ts,
  elpd
FROM (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY model_family
      ORDER BY elpd DESC
    ) AS r_best
  FROM latest_per_version
  WHERE rn = 1
) x
WHERE r_best = 1;

