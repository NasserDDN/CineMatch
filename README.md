# CineMatch: Personalized Movie Recommendation System

## Overview
CineMatch is a personalized movie recommendation system that leverages user preferences to suggest movies. The system uses the MovieLens dataset, renowned for its reliability and extensive genome tags and user ratings. By processing user likes and dislikes, CineMatch offers tailored movie suggestions, enhancing the user experience.

## Features
- **Personalized Recommendations**: Utilizes user preferences for tailored movie suggestions.
- **Rating-Based Sorting**: Displays movies sorted by average ratings for quality-focused recommendations.
- **Detailed Movie Information**: Shows movie posters, genres, summaries, and average ratings.
- **Interactive UI**: Users can like or dislike movies, influencing future recommendations.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/NasserDDN/CineMatch.git
   ```
2. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Before running the main application, compute the mean ratings for each movie:
1. Navigate to the `utils` directory.
2. Run the `compute_mean_ratings.py` script to generate `mean_ratings.csv`.
3. Launch the main application:
   ```bash
   python script.py
   ```

## How It Works
CineMatch operates on the MovieLens dataset. It first filters movies lacking genome tags, ensuring a quality dataset. User interactions (likes/dislikes) are tracked, and their movie genome data are used to find similar movies using a KNN algorithm. Movies are then sorted by average ratings and presented with detailed information.

## Dependencies
- Python 3
- Pandas
- NumPy
- Scikit-Learn
- Tkinter
- PIL
- Requests

## Credits
- MovieLens Dataset: [GroupLens](https://files.grouplens.org/datasets/movielens/ml-latest-README.html)
- Tkinter Theme: [Azure-ttk-theme](https://github.com/rdbende/Azure-ttk-theme/tree/main)

