# ---
# ## Q5 – Baseball-Flavored Coding: In-Game Win Probability Update

# **Problem**: Update win probability during a game based on plate appearance outcomes.

# **Inputs**:
# - Run expectancy table: (outs, base_state) → expected_runs_remaining
# - Before/after game states from a plate appearance




import csv
import math


def load_run_expectancy(path):
    re_dict = {}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (int(row["outs"]), row["base_state"])
            re_dict[key] = float(row["expected_runs"])
    return re_dict

def run_value(re, before, after, runs_scored):
    key_before = (before["outs"], before["base_state"])
    key_after = (after["outs"], after["base_state"])
    re_before = re.get(key_before, 0.0)
    re_after = re.get(key_after, 0.0)
    return (re_after + runs_scored) - re_before

def features_for_wp(state, cum_run_value):
    return [
        1.0,
        state["inning"],
        int(state["top"]),
        state["score_diff"],
        cum_run_value,
    ]

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def win_prob(beta, state, cum_run_value):
    x = features_for_wp(state, cum_run_value)
    z = sum(b * xi for b, xi in zip(beta, x))
    return sigmoid(z)

# SMOKE TEST
RE_EXAMPLE = {
    (1, "100"): 0.88,
    (1, "000"): 0.28,
}

before = {"inning": 7, "top": True, "score_diff": -1, "outs": 1, "base_state": "100"}
after  = {"inning": 7, "top": True, "score_diff": 0,  "outs": 1, "base_state": "000"}
runs_scored = 1

rv = run_value(RE_EXAMPLE, before, after, runs_scored)
print(f"Run Value: {rv:.2f}")  # Should be (0.28 + 1) - 0.88 = 0.40

beta = [0.2, 0.05, -0.05, 0.3, 0.1]  # Fake model weights
wp = win_prob(beta, after, cum_run_value=rv)
print(f"Win Probability: {wp:.2%}")

# Edge case: missing base_state/out combo
after_bad = after.copy()
after_bad["base_state"] = "999"  # Not in RE table
rv_bad = run_value(RE_EXAMPLE, before, after_bad, runs_scored)
print("Run Value (bad base_state):", rv_bad)

# Stress-ish: multiple inning WP updates
cum_rv = 0.0
for inning in range(7, 10):
    state = {"inning": inning, "top": False, "score_diff": inning - 7, "outs": 1, "base_state": "000"}
    cum_rv += 0.15
    print(f"Inning {inning}: WP = {win_prob(beta, state, cum_run_value=cum_rv):.2%}")
    print(f"Inning {inning}: WP = {win_prob(beta, state, cum_run_value=cum_rv):.2%}")
