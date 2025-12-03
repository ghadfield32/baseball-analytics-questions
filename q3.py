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
import pandas as pd

# Sample data to test with
data = [
    ("family_a", "v1", "2025-01-01 10:00:00", 10.2),
    ("family_a", "v1", "2025-01-02 11:00:00", 10.5),
    ("family_a", "v2", "2025-01-01 09:00:00", 11.0),
    ("family_b", "v1", "2025-01-01 08:00:00", 9.8),
    ("family_b", "v1", "2025-01-03 12:00:00", 10.0),
]

df = pd.DataFrame(data,
                  columns=["model_family", "model_version", "run_ts", "elpd"])

# -- Latest run per (model_family, model_version)

query1 = """
select 
  model_family,
  model_version,
  run_ts,
  elpd
from 
  (select *,
    row_number() over (partition by model_family, model_version order by run_ts desc) as rn
    from model_runs) t
where rn = 1;
"""

query2 = """
    with latest_per_versions as (
      select *,
        row_number() over (partition by model_family, model_version order by run_ts desc) as rn
      from model_runs
    )
    select
      model_family,
      model_version,
      run_ts,
      elpd
    from (
      select *,
        row_number() over (partition by model_family order by elpd desc) as r_best
      from latest_per_versions
      where rn = 1
    ) x
    where r_best = 1;

"""

if __name__ == "__main__":
  con = duckdb.connect(
  )  # optional, but clearer than using global duckdb.query

  # Register the pandas DataFrame as a DuckDB table
  con.register("model_runs", df)

  print("question 3================")
  latest_runs = con.sql(query1).df()
  best_versions = con.sql(query2).df()

  print("Latest run per (family, version):")
  print(latest_runs)

  print("\nBest version per family:")
  print(best_versions)
  print("question 3================ end")
