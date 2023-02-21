SELECT
  Groupedby_City_Breakfast_Querry.city_breakfast as city,
  Total_Amount_breakfast/Orders_Count_breakfast as breakfast_basket,
  Total_Amount_Allmeals/Orders_Count_Allmeals as efood_basket,
  Orders_Count_breakfast/Users_Count_breakfast as breakfast_freq,
  Orders_Count_Allmeals/Users_Count_Allmeals as efood_freq
  
  FROM
  (
    SELECT 
      city as city_breakfast,
      Count(DISTINCT order_id) as Orders_Count_breakfast,
      Count(DISTINCT user_id) as Users_Count_breakfast,
      Sum(amount) as Total_Amount_breakfast
    FROM `efood-assesment.main_assessment.orders`
    WHERE cuisine = "Breakfast"
    GROUP BY city
    HAVING Orders_Count_breakfast > 1000
    ORDER BY Orders_Count_breakfast DESC
  ) 
  AS Groupedby_City_Breakfast_Querry
  JOIN
  (
    SELECT 
      city as city_Allmeals,
      Count(DISTINCT order_id) as Orders_Count_Allmeals,
      Count(DISTINCT user_id) as Users_Count_Allmeals,
      Sum(amount) as Total_Amount_Allmeals
    FROM `efood-assesment.main_assessment.orders`
    GROUP BY city
    HAVING Orders_Count_Allmeals > 1000
    ORDER BY Orders_Count_Allmeals DESC
  ) AS GroupedBy_City_Allmeals_Querry
  ON
    GroupedBy_City_Allmeals_Querry.city_Allmeals = Groupedby_City_Breakfast_Querry.city_breakfast