"""
Generates a synthetic 'TechNova Solutions' product operations dataset,
modeled on the shape of real telematics/IoT product ops data
(bug tracking, release delivery, customer satisfaction).

Output: releases.csv, bugs.csv, feedback.csv
"""
import numpy as np
import pandas as pd
from datetime import timedelta

np.random.seed(42)

MODULES = ["Fleet Tracking", "Driver Mobile App", "Admin Web Dashboard",
           "IoT Sensor Hub", "Billing Portal"]
REGIONS = ["Nigeria", "UK", "UAE", "South Africa", "Kenya"]
SEVERITIES = ["Critical", "High", "Medium", "Low"]
SEV_WEIGHTS = [0.08, 0.22, 0.45, 0.25]

# ---------- 1. RELEASES ----------
start = pd.Timestamp("2025-01-06")  # first Monday of 2025
n_releases = 48  # ~ one release/week across modules, rotating
rows = []
for i in range(n_releases):
    release_id = f"REL-{1000+i}"
    module = MODULES[i % len(MODULES)]
    planned_date = start + timedelta(weeks=i // len(MODULES) * len(MODULES) + (i % len(MODULES)))
    # 90% on-time delivery target, so ~10% slip by 2-7 days
    on_time = np.random.rand() < 0.90
    if on_time:
        actual_date = planned_date
        status = "On-Time"
    else:
        slip = np.random.randint(2, 8)
        actual_date = planned_date + timedelta(days=int(slip))
        status = "Delayed"
    team_size = np.random.randint(4, 10)
    rows.append([release_id, module, f"{module} v{1 + i//len(MODULES)}.{i % len(MODULES)}",
                 planned_date.date(), actual_date.date(), status, team_size])

releases = pd.DataFrame(rows, columns=[
    "release_id", "product_module", "release_name",
    "planned_date", "actual_date", "status", "team_size"
])
releases.to_csv("releases.csv", index=False)

# ---------- 2. BUGS ----------
bug_rows = []
bug_counter = 1
for _, r in releases.iterrows():
    n_bugs = np.random.randint(10, 21)  # 10-20 bugs per release
    for _ in range(n_bugs):
        bug_id = f"BUG-{2000+bug_counter}"
        bug_counter += 1
        severity = np.random.choice(SEVERITIES, p=SEV_WEIGHTS)
        reported = pd.Timestamp(r["actual_date"]) + timedelta(days=int(np.random.randint(0, 10)))
        # resolution time varies by severity (critical fixed fastest)
        base_days = {"Critical": 1, "High": 3, "Medium": 6, "Low": 10}[severity]
        resolved_offset = max(0, int(np.random.normal(base_days, base_days * 0.4)))
        is_resolved = np.random.rand() < 0.93
        resolved = reported + timedelta(days=resolved_offset) if is_resolved else pd.NaT
        bug_rows.append([
            bug_id, r["release_id"], r["product_module"], severity,
            reported.date(),
            resolved.date() if is_resolved else "",
            "Resolved" if is_resolved else "Open",
            resolved_offset if is_resolved else ""
        ])

bugs = pd.DataFrame(bug_rows, columns=[
    "bug_id", "release_id", "module", "severity",
    "reported_date", "resolved_date", "status", "resolution_days"
])
bugs.to_csv("bugs.csv", index=False)

# ---------- 3. CUSTOMER FEEDBACK ----------
fb_rows = []
fb_counter = 1
for _, r in releases.iterrows():
    n_fb = np.random.randint(3, 9)
    # satisfaction trends upward over the year (simulating the 30% improvement)
    week_index = list(releases["release_id"]).index(r["release_id"])
    trend_boost = (week_index / n_releases) * 1.2  # up to +1.2 by year end
    for _ in range(n_fb):
        fb_id = f"FB-{3000+fb_counter}"
        fb_counter += 1
        score = np.clip(np.random.normal(3.2 + trend_boost, 0.7), 1, 5)
        fb_rows.append([
            fb_id, r["release_id"], r["product_module"],
            f"CUST-{np.random.randint(100, 400)}",
            round(score, 1),
            (pd.Timestamp(r["actual_date"]) + timedelta(days=int(np.random.randint(1, 14)))).date(),
            np.random.choice(REGIONS)
        ])

feedback = pd.DataFrame(fb_rows, columns=[
    "feedback_id", "release_id", "module", "customer_id",
    "satisfaction_score", "feedback_date", "region"
])
feedback.to_csv("feedback.csv", index=False)

print("releases:", releases.shape)
print("bugs:", bugs.shape)
print("feedback:", feedback.shape)
print("On-time %% :", round((releases['status']=='On-Time').mean()*100,1))
