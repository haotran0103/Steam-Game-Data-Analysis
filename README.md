# **Steam Game Data Analysis and Dashboard**

## 1. **Project Overview**

This project involves analyzing a dataset of Steam games using Hadoop and Hive for data processing, with PySpark for handling large-scale data analysis. The objective is to uncover valuable insights into game performance, user engagement, pricing trends, and platform distribution. We also built an interactive dashboard using Streamlit to present these insights in a user-friendly format.

The analysis focuses on:
- Identifying top-performing games based on various metrics.
- Understanding game pricing trends and their relationship with user scores.
- Exploring the impact of release dates on game success.
- Visualizing platform distribution (Windows, Mac, Linux) and user engagement patterns.

## 2. **Technologies Used**
- **Hadoop**: For distributed data storage and management.
- **Hive**: For SQL-like querying on large datasets.
- **PySpark**: For handling big data analysis and enabling efficient data ingestion.
- **Streamlit**: For building an interactive, real-time data dashboard.
- **Python**: For data manipulation and visualization.
- **Pandas, Matplotlib, Seaborn**: Python libraries used for advanced data analysis and visualizations.

## 3. **Data Insights**

1. **Total Number of Games**:
   - **Insight**: The dataset contains a total of 97,404 games on Steam. This highlights the vast diversity and richness of the platform.

2. **Top Games by Metrics**:
   - **Insight**: Based on estimated owners, the top-performing games include:
     - **New World**
     - **Black Myth: Wukong**
     - **Counter-Strike: Global Offensive**
     - **PUBG: BATTLEGROUNDS**
   These games have an estimated player base of 50 to 100 million, demonstrating their immense popularity and wide-reaching appeal.

3. **Game Distribution by Platform (Excluding Windows)**:
   - **Insight**: Excluding Windows, the number of games available on Mac (17,726 games) and Linux (13,332 games) are relatively balanced. This reflects a relatively equal distribution of games across these two platforms.

4. **Price vs Metacritic Score**:
   - **Insight**: A scatter plot analysis shows no clear correlation between a game's price and its Metacritic score. Some high-priced games still achieve high scores, while many lower-priced games also receive strong ratings, indicating that price is not a definitive factor in game quality from the user’s perspective.

5. **User Engagement Metrics**:
   - **Insight**: The small difference between the average playtime (91.77 hours) and the median playtime (81.85 hours) suggests that users tend to engage with games for extended periods. A significant portion of players invest substantial time into their favorite games.

6. **Impact of Release Date**:
   - **Insight**: A trend analysis of user scores over time reveals a noticeable spike in 2017, where several games released during this period received higher average user scores compared to other years. This may be attributed to the release of particularly successful and well-received games in that timeframe.

## 4. **HiveSQL Queries**
### 1. **Top-Performing Games**
```sql
SELECT Name, Estimated_owners, Peak_CCU 
FROM steam_games 
ORDER BY Estimated_owners DESC 
LIMIT 10;
```

### 2. **Game Pricing Trends**
```sql
SELECT Price, Discount, COUNT(AppID) AS game_count 
FROM steam_games 
GROUP BY Price, Discount 
ORDER BY game_count DESC;
```

### 3. **Release Date Impact**
```sql
SELECT YEAR(Release_date) AS release_year, COUNT(AppID) AS game_count, AVG(User_score) AS avg_user_score 
FROM steam_games 
GROUP BY YEAR(Release_date) 
ORDER BY release_year DESC;
```

### 4. **Platform Distribution**
```sql
SELECT COUNT(CASE WHEN Windows = 'true' THEN 1 END) AS windows_games,
       COUNT(CASE WHEN Mac = 'true' THEN 1 END) AS mac_games,
       COUNT(CASE WHEN Linux = 'true' THEN 1 END) AS linux_games
FROM steam_games;
```

### 5. **User Engagement**
```sql
SELECT Name, AVG(Average_playtime_forever) AS avg_playtime, AVG(Median_playtime_forever) AS median_playtime
FROM steam_games
GROUP BY Name
ORDER BY avg_playtime DESC
LIMIT 10;
```

### 6. **Reviews and Scores**
```sql
SELECT Name, Reviews, Metacritic_score, User_score 
FROM steam_games 
ORDER BY User_score DESC 
LIMIT 10;
```

### 7. **Game Performance by Genre**
- **Top Genres by Estimated Owners**
```sql
SELECT Genre, AVG(Estimated_owners) AS avg_owners, COUNT(AppID) AS game_count
FROM steam_games 
GROUP BY Genre
ORDER BY avg_owners DESC
LIMIT 10;
```

- **Genre Comparison Based on User Score**
```sql
SELECT Genre, AVG(User_score) AS avg_user_score, COUNT(AppID) AS game_count 
FROM steam_games 
GROUP BY Genre
ORDER BY avg_user_score DESC
LIMIT 10;
```

- **Genre-Based Engagement**
```sql
SELECT Genre, AVG(Average_playtime_forever) AS avg_playtime, AVG(Median_playtime_forever) AS median_playtime
FROM steam_games 
GROUP BY Genre
ORDER BY avg_playtime DESC
LIMIT 10;
```

### 8. **User Scores vs Developer Reputation**
- **Top Developers by Number of Games Released**
```sql
SELECT Developers, COUNT(AppID) AS game_count 
FROM steam_games 
GROUP BY Developers
ORDER BY game_count DESC
LIMIT 10;
```

- **Developers with the Highest Average User Score**
```sql
SELECT Developers, AVG(User_score) AS avg_user_score, COUNT(AppID) AS game_count 
FROM steam_games 
GROUP BY Developers
ORDER BY avg_user_score DESC
LIMIT 10;
```

## 5. **Installation and Usage**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/steam-game-analysis.git
   cd steam-game-analysis
   ```

2. **Set Up Hadoop and Hive**:  
   Ensure that Hadoop and Hive are installed and configured. Follow [this guide](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html) for setting up a single-node cluster. After setup, start both services:
   ```bash
   start-dfs.sh
   start-yarn.sh
   hive
   ```

3. **Ingest Data into Hive**:
   Use the provided SQL queries to create the necessary Hive tables and load the Steam game data.

4. **Set Up PySpark**:
   Ensure that PySpark is installed in your environment. You can install it via pip:
   ```bash
   pip install pyspark
   ```

5. **Run the Dashboard**:
   Install Streamlit and other dependencies:
   ```bash
   pip install streamlit pandas matplotlib seaborn
   ```
   Run the Streamlit dashboard:
   ```bash
   streamlit run app.py
   ```
   The dashboard will be accessible at `http://localhost:8501/`.
