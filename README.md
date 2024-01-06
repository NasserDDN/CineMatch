# CineMatch

## Description
CineMatch is a Python-based application that recommends movies to users based on their preferences. It utilizes a dataset of movies, including genome scores, movie titles, and genres, to generate personalized recommendations. The system features a user-friendly graphical interface built with Tkinter and the Azure ttk theme.

## Features
- **Search Functionality:** Allows users to search for movies from the dataset by titles.
- **Like and Dislike Options:** Users can like or dislike movies, influencing future recommendations.
- **Recommendation Engine:** Uses a K-Nearest Neighbors algorithm to recommend movies based on user preferences.
- **Dynamic UI Updates:** The interface updates in real-time to display search results and recommendations.

## Installation
1. Ensure Python is installed on your system.
2. Install required libraries: `pandas`, `numpy`, `sklearn`, `PIL`, and `requests`.
3. Clone the repository or download the script.

    ```bash
    git clone https://github.com/NasserDDN/CineMatch.git
    ```

4. Download the movie dataset [here](https://grouplens.org/datasets/movielens/latest/) and place it in the specified directory.

## Usage
1. Run the script:

    ```bash
    python script.py
    ```

2. The application window will open. Use the search bar to find movies or interact with the like/dislike buttons to set preferences.
3. Adjust the number of movies the application will recommend to you
4. Click on "Recommend movies" to get personalized movie suggestions.

## Dependencies
- **Pandas:** For data manipulation and analysis.
- **NumPy:** For numerical operations.
- **Scikit-learn:** For implementing the K-Nearest Neighbors algorithm.
- **Pillow (PIL):** For image processing.
- **Requests:** For fetching movie posters from an external API.
- **Tkinter:** For GUI creation.
- **Azure ttk theme:** For styling the GUI. Visit the [Azure ttk theme GitHub repository](https://github.com/rdbende/Azure-ttk-theme/tree/main) for more information.

## Note
This application is a demonstration project. The movie recommendation logic is basic and serves as an example of integrating machine learning algorithms with a GUI in Python.
