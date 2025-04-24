import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import sqlite3  # For SQL queries using SQLite

# Step 1: Load the Dataset
data = pd.read_csv(r"C:\Users\ch.Tharani\Desktop\Project 1\netflix1.csv.csv")

# Step 2: Initial Inspection
print("Columns in the dataset:", data.columns)
print(data.head())
print(data.info())
print(data.describe())

# Step 3: Data Cleaning
# Drop duplicates
data.drop_duplicates(inplace=True)

# Fill missing values (no 'cast' column in dataset)
data['director'] = data['director'].fillna('Not Given')
data['country'] = data['country'].fillna('Not Given')

# Convert date_added to datetime
data['date_added'] = pd.to_datetime(data['date_added'])

# Feature Engineering: Extract Year, Month, Day
data['year'] = data['date_added'].dt.year
data['month'] = data['date_added'].dt.month
data['day'] = data['date_added'].dt.day

# Step 4: Create genres column
data['genres'] = data['listed_in'].apply(lambda x: x.split(', '))

# Step 5: Prepare for SQL - Drop 'genres' column before saving to SQL
data_sql = data.drop(columns=['genres'])

# Step 6: SQLite Setup
conn = sqlite3.connect(':memory:')
data_sql.to_sql('netflix', conn, index=False, if_exists='replace')

# Example SQL query: Count of Movies vs TV Shows
query1 = "SELECT type, COUNT(*) as count FROM netflix GROUP BY type"
sql_result1 = pd.read_sql(query1, conn)
print(sql_result1)

# Example SQL query: Top 10 countries
query2 = "SELECT country, COUNT(*) as count FROM netflix GROUP BY country ORDER BY count DESC LIMIT 10"
sql_result2 = pd.read_sql(query2, conn)
print(sql_result2)

# Step 7: EDA & Visualizations
sns.set(style='whitegrid')

# Content Type Distribution
plt.figure(figsize=(6, 4))
sns.countplot(x='type', data=data, palette='Set2')
plt.title('Distribution of Content by Type')
plt.show()

# Top 10 Genres for Movies
movie_genres = data[data['type'] == 'Movie']['listed_in'].str.split(', ').explode()
top_movie_genres = movie_genres.value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_movie_genres.values, y=top_movie_genres.index, palette='Set3')
plt.title('Top 10 Movie Genres')
plt.show()

# Top 10 Genres for TV Shows
tv_genres = data[data['type'] == 'TV Show']['listed_in'].str.split(', ').explode()
top_tv_genres = tv_genres.value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_tv_genres.values, y=top_tv_genres.index, palette='Set1')
plt.title('Top 10 TV Show Genres')
plt.show()

# Content Added Over Time (Yearly)
yearly_content = data['year'].value_counts().sort_index()
plt.figure(figsize=(12, 6))
sns.lineplot(x=yearly_content.index, y=yearly_content.values)
plt.title('Content Added Over Years')
plt.xlabel('Year')
plt.ylabel('Number of Additions')
plt.grid(True)
plt.show()

# Content Added Monthly
monthly_movies = data[data['type'] == 'Movie']['month'].value_counts().sort_index()
monthly_shows = data[data['type'] == 'TV Show']['month'].value_counts().sort_index()
plt.figure(figsize=(10, 5))
plt.plot(monthly_movies.index, monthly_movies.values, label='Movies')
plt.plot(monthly_shows.index, monthly_shows.values, label='TV Shows')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.title('Monthly Releases of Movies and TV Shows')
plt.xlabel('Month')
plt.ylabel('Number of Releases')
plt.legend()
plt.grid(True)
plt.show()

# Top 10 Countries
top_countries = data['country'].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_countries.values, y=top_countries.index, palette='muted')
plt.title('Top 10 Countries with Most Content')
plt.show()

# Ratings Distribution
ratings = data['rating'].value_counts()
plt.figure(figsize=(12, 6))
sns.barplot(x=ratings.index, y=ratings.values, palette='coolwarm')
plt.xticks(rotation=45)
plt.title('Ratings Distribution')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.show()

# Top 10 Directors
top_directors = data['director'].value_counts().drop('Not Given').head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_directors.values, y=top_directors.index, palette='Blues_d')
plt.title('Top 10 Directors with Most Titles')
plt.xlabel('Number of Titles')
plt.ylabel('Director')
plt.show()

# Word Cloud of Movie Titles
movie_titles = data[data['type'] == 'Movie']['title']
wordcloud = WordCloud(width=800, height=400, background_color='black').generate(' '.join(movie_titles))
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Movie Titles')
plt.show()

# Step 8: Export cleaned data for Tableau or reference
data.to_excel(r'C:\Users\ch.Tharani\Desktop\Project 1\netflix_data_final.xlsx', index=False)

# Step 9: Close SQLite connection
conn.close()

print("✅ Project completed: Data cleaned, SQL analysis done, visualizations created, and data exported.")


