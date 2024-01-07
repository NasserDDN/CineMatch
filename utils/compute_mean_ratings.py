import pandas as pd

# PARAMETERS
nb_gen_tags_per_film = 1128
nb_neighbors_to_find = 1

# READ CSV
# Get data sample
df_gen_scores_with_cols = pd.read_csv(r"ml-latest/genome-scores.csv", delimiter=',', header=0)
df_links = pd.read_csv(r"ml-latest/links.csv", delimiter=',', header=0)

# Dataframe of movie.csv
df_films = pd.read_csv(r"ml-latest/movies.csv", delimiter=',',  quotechar='"', header=0)

# Deleting films that do not have a genome tag
unique_movie_ids = df_gen_scores_with_cols['movieId'].unique()
df_films_filtered = df_films[df_films['movieId'].isin(unique_movie_ids)]

# Read the ratings data
df_ratings = pd.read_csv(r"ml-latest/ratings.csv", delimiter=',', header=0)

# Merge movies data with ratings
df_movies_with_ratings = pd.merge(df_films_filtered, df_ratings, on='movieId')

# Calculate the average rating for each movie
average_ratings = df_movies_with_ratings.groupby('movieId')['rating'].mean()
average_ratings.to_csv(r"ml-latest/mean_ratings.csv", index=True)