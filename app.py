import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Steam Games Ingestion") \
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "4g") \
    .enableHiveSupport() \
    .getOrCreate()

def load_data(query):
    spark.sql("USE default")  
    return spark.sql(query).toPandas()

with open("./style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Steam Game Analysis Dashboard")

st.header("Total Games Count")
total_games_query = "SELECT COUNT(Name) AS total_games FROM steam_games"
total_games_df = load_data(total_games_query)
total_games_count = total_games_df['total_games'][0]
st.metric(label="Total Games", value=total_games_count)

st.header("Top Games by Metrics")
metric = st.selectbox("Choose Metric", ["Estimated Owners", "Reviews", "Average Playtime"])
if metric == "Estimated Owners":
    query = "SELECT Name, `Estimated owners` FROM steam_games ORDER BY `Estimated owners` DESC LIMIT 10"
elif metric == "Reviews":
    query = "SELECT Name, Reviews FROM steam_games ORDER BY Reviews DESC LIMIT 10"
else:
    query = "SELECT Name, Average_playtime_forever FROM steam_games ORDER BY `Average playtime forever` DESC LIMIT 10"
top_games_df = load_data(query)
st.write(top_games_df)

st.header("Game Distribution by Platform (Excluding Windows)")

platform_distribution_query = """
SELECT 
    SUM(CASE WHEN Mac = 'True' THEN 1 ELSE 0 END) AS Mac,
    SUM(CASE WHEN Linux = 'True' THEN 1 ELSE 0 END) AS Linux
FROM steam_games;
"""

platform_distribution_df = load_data(platform_distribution_query)
st.write(platform_distribution_df)
fig, ax = plt.subplots()
platform_distribution_df.plot(kind='bar', stacked=True, ax=ax)
ax.set_title("Game Distribution by Platform (Mac and Linux)")
ax.set_xlabel("Platforms")
ax.set_ylabel("Number of Games")
st.pyplot(fig)

st.header("Price vs User Score")
price_vs_score_query = """
SELECT Price, `Metacritic score`, `Metacritic url`, `User score`, `Positive`, `Negative` FROM steam_games
WHERE Price IS NOT NULL AND `Metacritic score` IS NOT NULL AND `Metacritic url` IS NOT NULL AND `User score` IS NOT NULL 
"""
price_vs_score_df = load_data(price_vs_score_query)
st.write(price_vs_score_df)

fig, ax = plt.subplots()
ax.scatter(price_vs_score_df['Price'], price_vs_score_df['Metacritic score'])
ax.set_xlabel("Price")
ax.set_ylabel("Metacritic score")
ax.set_title("Price vs Metacritic score")
st.pyplot(fig)  

st.header("User Engagement Insights")
engagement_query = """
SELECT AVG(`Average playtime forever`) AS avg_playtime, AVG(`Median playtime forever`) AS median_playtime
FROM steam_games
"""
engagement_df = load_data(engagement_query)
st.write(engagement_df)
fig, ax = plt.subplots()
sns.barplot(data=engagement_df, palette="viridis", ax=ax)
ax.set_title("User Engagement")
st.pyplot(fig) 

st.header("Release Date Impact")
release_date_query = """
SELECT `Release_date`, AVG(`User score`) AS avg_user_score
FROM steam_games
GROUP BY `Release_date`
"""
release_date_df = load_data(release_date_query)
release_date_df['Release_date'] = release_date_df['Release_date'].str.replace('"', '').str.strip()
release_date_df['Release_date'] = pd.to_datetime(release_date_df['Release_date'], format='%b %d, %Y', errors='coerce')
release_date_df.dropna(subset=['Release_date'], inplace=True)
release_date_df.set_index('Release_date', inplace=True)
if not release_date_df.empty:
    fig, ax = plt.subplots()
    release_date_df.plot(kind='line', ax=ax)
    ax.set_title("Average User Score Over Time by Release Date")
    ax.set_xlabel("Release Date")
    ax.set_ylabel("Average User Score")
    st.pyplot(fig)
else:
    st.write("No valid release date data to plot.")

st.write("Dashboard created by kitkat")
