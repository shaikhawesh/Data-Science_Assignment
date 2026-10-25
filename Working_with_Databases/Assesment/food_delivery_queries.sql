-- SECTION A SQL REFERENCES

-- S4: all restaurants, including zero-order restaurants
SELECT r.name, COALESCE(SUM(o.order_value),0) AS total_revenue
FROM restaurants r
LEFT JOIN orders o ON r.restaurant_id=o.restaurant_id
GROUP BY r.restaurant_id,r.name;

-- S5: rank agents within city and retrieve previous count
WITH agent_summary AS (
  SELECT city, agent_id, SUM(completed_deliveries) AS completed_deliveries
  FROM deliveries
  WHERE delivery_date >= date('now','start of month')
  GROUP BY city,agent_id
)
SELECT city,agent_id,completed_deliveries,
       RANK() OVER(PARTITION BY city ORDER BY completed_deliveries DESC) AS delivery_rank,
       LAG(completed_deliveries) OVER(PARTITION BY city ORDER BY completed_deliveries DESC) AS previous_agent_count
FROM agent_summary;

-- S6: CTE
WITH top_categories AS (
  SELECT category FROM restaurants
  GROUP BY category ORDER BY COUNT(*) DESC LIMIT 5
)
SELECT o.*
FROM orders o
JOIN restaurants r ON r.restaurant_id=o.restaurant_id
JOIN top_categories t ON t.category=r.category;