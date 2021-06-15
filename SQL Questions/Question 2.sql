WITH promotion_visitors AS(
    SELECT SUM(sv.`number of visitors`) AS promo_vis_sum
    FROM site_visitors sv
    JOIN `promotion dates` pd
    ON sv.site = pd.site
    AND sv.date >= pd.start_date
    AND sv.date <= pd.end_date
    )
SELECT STR((SELECT promo_vis_sum FROM promotion_visitors) / SUM(`number of visitors`) * 100) || '%' AS promotion_day_traffic_pct
FROM site_visitors