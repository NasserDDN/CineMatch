import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO
import random
from tkinter import ttk

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

# Films liked by user
liked_movie_ids = []
disliked_movie_ids = []

# Store loved movies' genomes
liked_movies_genome = []

# Initialize the widget to display the names of popular films
appreciated_movies = []
unappreciated_movies = []

MAX_RESULTS = 10  # Maximum number of results to display
API_KEY = '582fe6553526e7a754f6347ba656ddf5'

# Global declaration for storing image references
image_references = []

def get_movie_poster(tmdbId):
    api_url = f"https://api.themoviedb.org/3/movie/{tmdbId}?api_key={API_KEY}&language=en-US"
    response = requests.get(api_url)
    data = response.json()

    # Basic URL for TMDb images
    base_url = "https://image.tmdb.org/t/p/original"
    
    if 'poster_path' in data and data['poster_path']:
        poster_url = base_url + data['poster_path']
        return poster_url
    else:
        return None  # or the URL of a placeholder image if the poster is not available


def search():
    query = entry.get().lower()
    resultat = df_films_filtered[df_films_filtered['title'].str.lower().str.contains(query)]
    root.after(0, update_ui, resultat.head(MAX_RESULTS))  # Display only the first results


def load_image_from_url(url, max_size=(200, 200)):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image.thumbnail(max_size, Image.Resampling.LANCZOS) 
    return ImageTk.PhotoImage(image)

def delete_genome_in_DF(movieIDs):
        global df_gen_scores_with_cols
        # Delete dataframe rows containing ids in movieIDs list
        df_gen_scores_with_cols = df_gen_scores_with_cols[~df_gen_scores_with_cols['movieId'].isin(movieIDs)]
        

def on_like(movieId):

    if movieId not in liked_movie_ids:

        liked_movie_ids.append(movieId)
        nom_film = df_films_filtered[df_films_filtered['movieId'] == movieId]['title'].iloc[0]

        if movieId in disliked_movie_ids:
            # Remove movieId if it is in the disliked list
            disliked_movie_ids.remove(movieId)

            # Remove movie name
            unappreciated_movies.remove(nom_film)

            update_unapreciated_movies_list()

        if nom_film not in appreciated_movies:
            
            appreciated_movies.append(nom_film)
            update_appreciated_movies_list()

def on_dislike(movieId):

    if movieId not in disliked_movie_ids:

        disliked_movie_ids.append(movieId)
        nom_film = df_films_filtered[df_films_filtered['movieId'] == movieId]['title'].iloc[0]

        if movieId in liked_movie_ids:
            # Remove movieId if it is in the liked list
            liked_movie_ids.remove(movieId)

            # Remove movie name
            appreciated_movies.remove(nom_film)
            update_appreciated_movies_list()

        if nom_film not in unappreciated_movies:
            unappreciated_movies.append(nom_film)
            update_unapreciated_movies_list()

def update_ui(films):
    global image_references
    image_references.clear()  # Delete previous references

    for widget in inner_frame.winfo_children():
        widget.destroy()

    for _, film in films.iterrows():
        movieId = film['movieId']
        film_frame = ttk.Frame(inner_frame)
        film_frame.pack(fill='x', expand=True, padx=5, pady=5)

        tmdbId = df_links[df_links['movieId'] == film['movieId']]['tmdbId'].iloc[0]
        poster_url = get_movie_poster(tmdbId)
        if poster_url:
            poster_image = load_image_from_url(poster_url)

            # Store image reference to prevent it being collected by the garbage collector
            image_references.append(poster_image)

            image_label = ttk.Label(film_frame, image=poster_image)
            image_label.pack(side="left", padx=10)

        ttk.Label(film_frame, text=f"{film['title']} - {film['genres']}").pack(side="left", padx=10)


        # Add Like and Dislike buttons
        like_button = ttk.Button(film_frame, text="Like", command=lambda mid=movieId: on_like(mid))
        like_button.pack(side="left", padx=5)

        dislike_button = ttk.Button(film_frame, text="Dislike", command=lambda mid=movieId: on_dislike(mid))
        dislike_button.pack(side="left", padx=5)

        film_frame.pack(fill='x', expand=True, padx=5, pady=5)

    # Update interface to obtain updated dimensions
    root.update_idletasks()
    inner_frame.update_idletasks()

    # Calculate the x position to center the inner_frame
    canvas_width = canvas.winfo_width()
    inner_frame_width = inner_frame.winfo_reqwidth()
    new_x_position = (canvas_width - inner_frame_width) / 2 if canvas_width > inner_frame_width else 0

    # Update inner_frame position
    canvas.coords(inner_frame_window, new_x_position, 0)

    # Update canvas scroll region
    canvas.configure(scrollregion=canvas.bbox("all"))

def center_frames():
    # Update interface to obtain updated dimensions
    root.update_idletasks()
    inner_frame.update_idletasks()

    # Calculate the x position to center the inner_frame
    canvas_width = canvas.winfo_width()
    inner_frame_width = inner_frame.winfo_reqwidth()
    new_x_position = (canvas_width - inner_frame_width) / 2 if canvas_width > inner_frame_width else 0

    # Update inner_frame position
    canvas.coords(inner_frame_window, new_x_position, 0)

    # Update canvas scroll region
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_window_resize(event):
    center_frames()

def truncate_text(text, max_length=30):
    """Truncate text if it exceeds the maximum length allowed."""
    if len(text) > max_length:
        return text[:max_length-3] + "..."
    return text

def update_appreciated_movies_list():
    appreciated_movies_list.delete(0, tk.END)
    for film in appreciated_movies:
        appreciated_movies_list.insert(tk.END, truncate_text(film))

def update_unapreciated_movies_list():
    unappreciated_movies_list.delete(0, tk.END)
    for film in unappreciated_movies:
        unappreciated_movies_list.insert(tk.END, truncate_text(film))

def increase_nb_neighbors():
    global nb_neighbors_to_find
    nb_neighbors_to_find += 1
    nb_neighbors_label.config(text=str(nb_neighbors_to_find))

def decrease_nb_neighbors():
    global nb_neighbors_to_find
    if nb_neighbors_to_find > 1:
        nb_neighbors_to_find -= 1
        nb_neighbors_label.config(text=str(nb_neighbors_to_find))

def display_recommendations(recommended_movies):
    # Delete existing search results
    for widget in inner_frame.winfo_children():
        widget.destroy()

    # Add a title for the recommendations section
    recommendations_title = ttk.Label(inner_frame, text="Recommendations", font=("Helvetica", 16))
    recommendations_title.pack(side="top", pady=10)

    for movie in recommended_movies:
        film_frame = ttk.Frame(inner_frame)
        film_frame.pack(fill='x', expand=True, padx=5, pady=5)

        # Show film poster (if available)
        poster_url = get_movie_poster(movie['tmdbId'])
        if poster_url:
            poster_image = load_image_from_url(poster_url)
            image_label = ttk.Label(film_frame, image=poster_image)
            image_label.image = poster_image  # Keep a reference
            image_label.pack(side="left", padx=10)

        # Show film title and reason for recommendation
        film_title_label = ttk.Label(film_frame, text=f"{movie['title']} because you loved {movie['reason']}")
        film_title_label.pack(side="left", padx=10)

def recommend():
    global df_gen_scores_without_cols, df_gen_scores_with_cols, liked_movie_ids, disliked_movie_ids, liked_movies_genome

    # If some movies have been liked
    if len(liked_movie_ids) > 0:

        # Get liked movies' genomes
        liked_movies_genome.extend([
            df_gen_scores_with_cols[df_gen_scores_with_cols['movieId'] == movieId]['relevance'].tolist() 
            for movieId in liked_movie_ids 
            if df_gen_scores_with_cols[df_gen_scores_with_cols['movieId'] == movieId]['relevance'].tolist() not in liked_movies_genome
        ])

        # Remove watched movies in genome Dataframe
        delete_genome_in_DF(liked_movie_ids)
        delete_genome_in_DF(disliked_movie_ids)

        # Select only the third column containg relevances
        df_gen_scores_without_cols = df_gen_scores_with_cols.iloc[:,2].to_numpy()

        # Create and fill X which is entry of KNN
        # X which is a 2D array containing lists of all genome relevance tags per film
        X = []
        for idx in range(0,len(df_gen_scores_without_cols), nb_gen_tags_per_film):
            X.append(df_gen_scores_without_cols[idx:idx+nb_gen_tags_per_film].tolist())

        recommended_movies = []  # List to store information on recommended films
        
        for x in range(nb_neighbors_to_find):
            
            # Randomly select a film in liked ones
            rand_film = random.randint(0, len(liked_movie_ids)-1)
            movie_title = appreciated_movies[rand_film]
            movie_genome = liked_movies_genome[rand_film]

            # Prediction
            neigh = NearestNeighbors(n_neighbors=1)
            neigh.fit(X)
            ids_pred_movies = neigh.kneighbors([movie_genome], return_distance=False)

            # Get movie's id in database
            id_db = df_gen_scores_with_cols.iloc[ids_pred_movies[0,0]*nb_gen_tags_per_film, 0]

            # Get movies' titles
            pred_movie = df_films_filtered.loc[df_films_filtered['movieId'] == id_db]
            print(f"Recommended movie {x} : {pred_movie.iloc[0,1]}, because you liked {movie_title}")

            id_tmdb = df_links[df_links['movieId'] == id_db]['tmdbId'].iloc[0]
            recommended_movies.append({'title': pred_movie.iloc[0,1], 'tmdbId': id_tmdb, 'reason' : movie_title })

            # Remove genome from dataframe for not recommending the same film in the futur
            delete_genome_in_DF([id_db])
            del X[ids_pred_movies[0,0]]
        
        # Show recommendations
        display_recommendations(recommended_movies)

# Window creation
root = tk.Tk()

# Set the initial theme
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "light")

# Parent frame for the entire interface
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Frame for search area
search_frame = ttk.Frame(main_frame)
search_frame.pack(side="top", fill="y")

entry = ttk.Entry(search_frame)
entry.pack(side="left", padx=5, pady=5)

search_button = ttk.Button(search_frame, text="Search", command=search)
search_button.pack(side="left", padx=5, pady=5)

# Frame for the Recommendations button
recommandations_frame = ttk.Frame(main_frame)
recommandations_frame.pack(side="top", fill="x")

recommander_button = ttk.Button(recommandations_frame, text="Recommend movies", command=recommend)
recommander_button.pack(side="top", pady=5)

# Outer frame for centering
outer_nb_neighbors_frame = ttk.Frame(main_frame)
outer_nb_neighbors_frame.pack(side="top", fill="x")

# Empty frame for left space
left_space_frame = ttk.Frame(outer_nb_neighbors_frame, width=100)
left_space_frame.pack(side="left", expand=True)

# Frame for the number of films to recommend and +/- buttons
nb_neighbors_frame = ttk.Frame(outer_nb_neighbors_frame)
nb_neighbors_frame.pack(side="left")

recommandations_text_label = ttk.Label(nb_neighbors_frame, text="Number of films to recommend :")
recommandations_text_label.pack(side="left")

nb_neighbors_label = ttk.Label(nb_neighbors_frame, text=str(nb_neighbors_to_find))
nb_neighbors_label.pack(side="left")

plus_button = ttk.Button(nb_neighbors_frame, text="+", command=increase_nb_neighbors)
plus_button.pack(side="left", padx=2)

minus_button = ttk.Button(nb_neighbors_frame, text="-", command=decrease_nb_neighbors)
minus_button.pack(side="left", padx=2)

# Empty frame for space on right
right_space_frame = ttk.Frame(outer_nb_neighbors_frame, width=100)
right_space_frame.pack(side="left", expand=True)


# Frame for grouping liked and disliked films, placed at top right
appreciated_movies_group_frame = ttk.Frame(main_frame)
appreciated_movies_group_frame.pack(side="right", fill="y")

# Canvas for movies, placed after the frames of liked/unliked movies
canvas = tk.Canvas(main_frame)
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

inner_frame = ttk.Frame(canvas)
inner_frame_window = canvas.create_window((0, 0), window=inner_frame, anchor='nw')

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="left", fill="y")

# Frame for popular films
appreciated_movies_frame = ttk.Frame(appreciated_movies_group_frame)
appreciated_movies_frame.pack(fill="x")

appreciated_movies_label = ttk.Label(appreciated_movies_frame, text="Appreciated movies")
appreciated_movies_label.pack()

appreciated_movies_list = tk.Listbox(appreciated_movies_frame)
appreciated_movies_list.pack(fill="y")

# Frame for unappreciated films
unappreciated_movies_frame = ttk.Frame(appreciated_movies_group_frame)
unappreciated_movies_frame.pack(fill="x")

unappreciated_movies_label = ttk.Label(unappreciated_movies_frame, text="Unappreciated movies")
unappreciated_movies_label.pack()

unappreciated_movies_list = tk.Listbox(unappreciated_movies_frame, takefocus=0)
unappreciated_movies_list.pack(fill="y")

# Listbox width settings for liked and disliked films
width_listbox = 50
appreciated_movies_list.configure(width=width_listbox)
unappreciated_movies_list.configure(width=width_listbox)

root.bind("<Configure>", on_window_resize)
root.mainloop()
