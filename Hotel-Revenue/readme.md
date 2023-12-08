# Hotel Revenue




The project task was to analyze hotel data and determine if more parking was needed based on revenue and parking.


My first task in this project was to gather the data. I was provided with multiple sheets. 3 sheets included dates for the years 2018, 2019, and 2020. The data also included a sheet for meal cost and market segment.

My first action with this data was to gather the dates. Using Microsoft SQL Server, I imported all data as separate tables. Once the data was in SQL, I utilized the following code: 

  with hotels as (
  SELECT * FROM dbo.['2018$']
  union
  SELECT * FROM dbo.['2019$']
  union
  SELECT * FROM dbo.['2020$'])

  Due to the data having the same values but different years, Union was the best way to join this data. I then joined this data with the 2 remaining tables:

    SELECT * FROM hotels
    left join dbo.market_segment$ 
    ON hotels.market_segment = market_segment$.market_segment
    left join dbo.meal_cost$
    ON hotels.meal = meal_cost$.meal

I used this query in Power BI to get all the data into my visualization tool. Once this was done I started working on the dashboard. 

The first section of the dashboard I worked on was revenue. I utilized cards and line graphs to get visualizations for revenue, as well as daily average rate, total nights, and average discount

![image](https://github.com/alouis752/Data-projects-Tripleten-/assets/75276869/980388f8-bd25-473d-8343-4dbdad243c1f)

I then added a line graph for overall revenue, colored by hotel property:

![image](https://github.com/alouis752/Data-projects-Tripleten-/assets/75276869/0ef312e3-cd30-465f-8aab-e9e7d35a2eb2)



I then focused on the question of parking with the same visualization method as well as a table:

![image](https://github.com/alouis752/Data-projects-Tripleten-/assets/75276869/c8fd2a8b-082f-4c8f-9422-95ef47aa9bef)


My last task was to add filters to determine the date (year and quarter), as well as the property.

![image](https://github.com/alouis752/Data-projects-Tripleten-/assets/75276869/2647bb0f-1301-4f93-aee2-a1eb203984fc)


The following is the final dashboard created

![image](https://github.com/alouis752/Data-projects-Tripleten-/assets/75276869/89af7e0e-2bc9-441e-beb7-9fc5949d4599)




I found that the resort hotel had much more demand for parking, but that the needs were being met in both properties at the current time. I also determined that the 3rd quarter was the most popular for both hotels, but that the Resort hotel was more popular. 



