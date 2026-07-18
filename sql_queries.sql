-- ============================================================
-- Nova Product Ops SQL Analysis
-- Database: technova_product_ops.db
-- Please open this file inside DB Browser for SQLite -> "Execute SQL" tab
-- Kindly run ONE query at a time: click into the query, then click the play/run button (or press Ctrl+Enter / Cmd+Return)
-- ============================================================


-- 1. ON-TIME DELIVERY RATE (overall)
-- Tells the % of on-time delivery.
SELECT
    COUNT(*) AS total_releases,
    SUM(CASE WHEN status = 'On-Time' THEN 1 ELSE 0 END) AS on_time_releases,
    ROUND(100.0 * SUM(CASE WHEN status = 'On-Time' THEN 1 ELSE 0 END) / COUNT(*), 1) AS on_time_pct
FROM releases;


-- 2. ON-TIME DELIVERY RATE BY MODULE
-- Tells which product module is the most/least reliable at hitting deadlines 
-- It is useful for a "where should we focus" slide.
SELECT
    product_module,
    COUNT(*) AS releases,
    ROUND(100.0 * SUM(CASE WHEN status = 'On-Time' THEN 1 ELSE 0 END) / COUNT(*), 1) AS on_time_pct
FROM releases
GROUP BY product_module
ORDER BY on_time_pct DESC;


-- 3. BUGS PER RELEASE, BY SEVERITY
-- Shows the average bug load per release, split by how serious the bugs are.
-- This helps with identifying bugs per release.
SELECT
    b.severity,
    COUNT(*) AS total_bugs,
    ROUND(1.0 * COUNT(*) / (SELECT COUNT(*) FROM releases), 1) AS avg_bugs_per_release
FROM bugs b
GROUP BY b.severity
ORDER BY
    CASE b.severity
        WHEN 'Critical' THEN 1 WHEN 'High' THEN 2
        WHEN 'Medium' THEN 3 ELSE 4 END;


-- 4. AVERAGE BUG RESOLUTION TIME, BY SEVERITY
-- Shows how many days it typically takes to fix a bug of a given severity 
-- This helps QA/ops efficiency metric.
SELECT
    severity,
    ROUND(AVG(resolution_days), 1) AS avg_days_to_resolve,
    COUNT(*) AS resolved_bug_count
FROM bugs
WHERE status = 'Resolved'
GROUP BY severity
ORDER BY avg_days_to_resolve;


-- 5. MONTHLY BUG TREND
-- Shows if bug volume going up or down over time
-- This feeds the "bugs over time" line chart in the dashboard.
SELECT
    strftime('%Y-%m', reported_date) AS month,
    COUNT(*) AS bugs_reported
FROM bugs
GROUP BY month
ORDER BY month;


-- 6. CUSTOMER SATISFACTION TREND OVER TIME
-- This shows whether there is improvement in customer satisfaction or not, with a real trend line.
SELECT
    strftime('%Y-%m', feedback_date) AS month,
    ROUND(AVG(satisfaction_score), 2) AS avg_satisfaction,
    COUNT(*) AS responses
FROM feedback
GROUP BY month
ORDER BY month;


-- 7. SATISFACTION BY REGION
-- Shows which markets are the happiest/unhappiest
-- This is useful for a "where do we need attention" view and feedback to mgt.
SELECT
    region,
    ROUND(AVG(satisfaction_score), 2) AS avg_satisfaction,
    COUNT(*) AS responses
FROM feedback
GROUP BY region
ORDER BY avg_satisfaction DESC;


-- 8. FULL JOINED VIEW (this single table can be used in Power BI)
-- This query can be turned into a Power BI data source if one flat table is needed instead of three linked ones.
SELECT
    r.release_id,
    r.product_module,
    r.release_name,
    r.planned_date,
    r.actual_date,
    r.status AS delivery_status,
    r.team_size,
    (SELECT COUNT(*) FROM bugs b WHERE b.release_id = r.release_id) AS bug_count,
    (SELECT ROUND(AVG(f.satisfaction_score), 2) FROM feedback f WHERE f.release_id = r.release_id) AS avg_satisfaction
FROM releases r
ORDER BY r.planned_date;
