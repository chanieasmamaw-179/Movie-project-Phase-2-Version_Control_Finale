from storage_interface import StorageInterface
import requests
from fuzzywuzzy import fuzz, process
from datetime import datetime
import statistics as stat
import matplotlib.pyplot as plt
import random

class MovieCollection:
    """Class to manage a collection of movies."""

    def __init__(self, storage: StorageInterface):
        self.storage = storage
        self.movies = self.storage.get_movies()  # Load movies from storage

    def fetch_movie_data(self, title):
        """Fetch movie data from OMDb API."""
        API_KEY = '5567aa49'  # Use environment variables or secure methods
        try:
            response = requests.get(f'http://www.omdbapi.com/?t={title}&apikey={API_KEY}')
            response.raise_for_status()
            movie_data = response.json()
            if movie_data.get('Response') == 'True':
                return {
                    'title': movie_data.get('Title'),
                    'year': movie_data.get('Year'),
                    'rating': movie_data.get('imdbRating'),
                    'actors': movie_data.get('Actors', 'N/A'),  # Default if not present
                    'poster': movie_data.get('Poster', 'N/A')  # Default if not present
                }
            else:
                print(f"Error fetching data for '{title}': {movie_data.get('Error')}")
                return None
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def add_movie(self, title):
        """Add a movie by fetching data from the OMDb API based on the title."""
        movie_info = self.fetch_movie_data(title)
        if movie_info:
            self.movies[movie_info['title'].lower()] = movie_info
            self.storage.save_movies(self.movies)  # Save after adding
            print(f"Data for '{movie_info['title']}' has been added.")

    def delete_movie(self, movie_title):
        """Delete a movie by title with fuzzy matching."""
        movie_title_lower = movie_title.lower()
        movie_titles = list(self.movies.keys())
        best_match, score = process.extractOne(movie_title_lower, movie_titles, scorer=fuzz.partial_ratio)

        if score >= 50:  # Threshold for a good match
            del self.movies[best_match]
            print(f"Deleted movie: {best_match.title()} (Score: {score})")
            self.storage.save_movies(self.movies)  # Save after deleting
        else:
            print(f"Movie '{movie_title}' not found.")

    def update_movie(self, title):
        """Update a movie's data by fetching from the OMDb API."""
        title_lower = title.lower()
        movie_titles = list(self.movies.keys())
        best_match, score = process.extractOne(title_lower, movie_titles, scorer=fuzz.partial_ratio)

        if score >= 50:  # Threshold for a good match
            movie_info = self.fetch_movie_data(best_match)
            if movie_info:
                self.movies[best_match] = movie_info
                print(f"Updated movie data for '{movie_info['title']}'.")
                self.storage.save_movies(self.movies)  # Save after updating
        else:
            print(f"Movie '{title}' not found.")

    def list_movies(self):
        if not self.movies:
            print("No movies in the list.")
        else:
            for movie in self.movies.values():
                print(f"{movie['title']} ({movie['year']}): {movie['rating']} rating")
                print(f"  Actors: {movie.get('actors', 'N/A')}")
                print(f"  Poster: {movie.get('poster', 'N/A')}")

    def show_stats(self):
        if self.movies:
            try:
                ratings = [float(movie.get('rating', 0)) for movie in self.movies.values()]
            except ValueError as e:
                print(f"Error converting ratings to float: {e}")
                return

            if ratings:
                average_rating = stat.mean(ratings)
                median_rating = stat.median(ratings)
                best_movie = max(self.movies.values(), key=lambda x: float(x.get('rating', 0)))
                worst_movie = min(self.movies.values(), key=lambda x: float(x.get('rating', 0)))

                print(f"Average rating: {average_rating:.2f}")
                print(f"Median rating: {median_rating:.2f}")
                print(f"Best rating: {best_movie['rating']} ({best_movie['title']} ({best_movie['year']}))")
                print(f"Worst rating: {worst_movie['rating']} ({worst_movie['title']} ({worst_movie['year']}))")

                titles = [movie['title'] for movie in self.movies.values()]
                ratings = [float(movie.get('rating', 0)) for movie in self.movies.values()]
                plt.figure(figsize=(10, 8))
                plt.barh(titles, ratings, color='black')
                plt.xlabel('Ratings')
                plt.ylabel('Movies')
                plt.title('Ratings of Movies')
                plt.show()
            else:
                print("No ratings available for statistics.")
        else:
            print("No movies available for statistics.")

    def show_random_movie(self):
        if self.movies:
            random_movie = random.choice(list(self.movies.values()))
            print(f"Random movie: {random_movie['title']} ({random_movie['year']}): {random_movie['rating']} rating")
            print(f"  Actors: {random_movie.get('actors', 'N/A')}")
            print(f"  Poster: {random_movie.get('poster', 'N/A')}")
        else:
            print("No movies available.")

    def sort_movies_by_rating(self):
        if not self.movies:
            print("No movies to sort.")
            return

        try:
            sorted_movies = sorted(self.movies.values(), key=lambda movie: float(movie.get('rating', 0)), reverse=True)
        except ValueError as e:
            print(f"Error converting ratings to float: {e}")
            return

        for movie in sorted_movies:
            print(f"Sorted movie: {movie['title']} ({movie['year']}): {movie['rating']} rating")

    def search_movie(self, title):
        title_lower = title.lower()
        movie_titles = list(self.movies.keys())
        best_match, score = process.extractOne(title_lower, movie_titles, scorer=fuzz.partial_ratio)

        if score >= 50:  # Threshold for a good match
            movie = self.movies[best_match]
            print(f"Found {movie['title']} ({movie['year']}): {movie['rating']} rating (Score: {score})")
            print(f"  Actors: {movie.get('actors', 'N/A')}")
            print(f"  Poster: {movie.get('poster', 'N/A')}")
        else:
            print(f"Movie '{title}' not found.")
