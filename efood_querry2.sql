SELECT
  A.city as city,
  SUM(A.user_orders_count / B.city_orders_count) as Percentage_orders
FROM 
(
  SELECT 
  city,
  ROW_NUMBER() OVER(PARTITION BY city) AS rn,
  user_id,
  COUNT(order_id) as user_orders_count
  FROM `efood-assesment.main_assessment.orders`
  GROUP BY city, user_id
  ORDER BY city ASC, user_orders_count DESC
) AS A
LEFT JOIN
(
  SELECT 
    city,
    COUNT(order_id) as city_orders_count
  FROM `efood-assesment.main_assessment.orders`
  GROUP BY city
) AS B 
ON
  A.city = B.city
WHERE A.rn<11
GROUP BY A.city
ORDER BY A.city