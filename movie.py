import random
import logging
from fuzzywuzzy import process
from typing import Optional, Dict
from storage_interface import StorageInterface
import statistics as stat

# Configure logging
logging.basicConfig(level=logging.INFO)


class MovieCollection:
    """Class to manage a collection of movies."""

    def __init__(self, storage: StorageInterface):
        """Initialize the movie collection with a storage interface."""
        self.storage = storage
        self.movies = self.storage.get_movies()  # Load movies from storage
        logging.info(f"Initial movies loaded: {self.movies}")  # Log the loaded movies

    def fetch_movie_data(self, movie_title: str) -> Optional[Dict]:
        """Fetch movie data from an external API or local storage."""
        movie = self.movies.get(movie_title.lower())
        if not movie:
            movie = self.storage.fetch_movie_info(movie_title)
            if not movie:
                logging.warning(f"Movie '{movie_title}' not found in the API.")
                return None
        return movie

    def add_movie(self, title: str) -> str:
        """Add a new movie to the collection."""
        movie_data = self.fetch_movie_data(title)
        if movie_data:
            self.movies[title.lower()] = movie_data
            self.storage.save_movies(self.movies)  # Save the updated collection
            message = f"Movie '{title}' added successfully."
            logging.info(message)
            return message
        else:
            message = f"Movie '{title}' not found."
            logging.warning(message)
            return message

    def delete_movie(self, title: str) -> str:
        """Delete a movie from the collection."""
        title_lower = title.lower()
        if title_lower in self.movies:
            del self.movies[title_lower]
            self.storage.save_movies(self.movies)
            message = f"Movie '{title}' deleted successfully."
            logging.info(message)
            return message
        else:
            match, score = process.extractOne(title_lower, self.movies.keys())
            if score >= 80:
                message = f"Movie '{title}' not found. Did you mean '{match}'?"
                logging.info(message)
                return message
            else:
                message = f"Movie '{title}' not found in the collection."
                logging.warning(message)
                return message

    def update_movie(self, title: str) -> str:
        """Update an existing movie in the collection."""
        title_lower = title.lower()
        if title_lower in self.movies:
            movie_data = self.fetch_movie_data(title)
            if movie_data:
                self.movies[title_lower] = movie_data
                self.storage.save_movies(self.movies)
                message = f"Movie '{title}' updated successfully."
                logging.info(message)
                return message
            else:
                message = f"Movie '{title}' not found in the API."
                logging.warning(message)
                return message
        else:
            match, score = process.extractOne(title_lower, self.movies.keys())
            if score >= 80:
                message = f"Movie '{title}' not found. Did you mean '{match}'?"
                logging.info(message)
                return message
            else:
                message = f"Movie '{title}' not found in the collection."
                logging.warning(message)
                return message

    def list_movies(self) -> str:
        """List all movies in the collection."""
        if not self.movies:
            message = "No movies available."
            logging.info(message)
            return message
        else:
            movie_list = []
            for title, data in self.movies.items():
                rating = data.get('rating') or data.get('imdbRating') or data.get('score') or 'N/A'
                movie_title = title.title() if title else 'Unknown Title'
                movie_list.append(f"{movie_title} - Rating: {rating}")

            movie_list_str = "\n".join(movie_list)
            logging.info(movie_list_str)
            return movie_list_str

    def show_stats(self) -> str:
        """Show movie statistics such as average, highest, and lowest rating."""
        if not self.movies:
            message = "No movies available to show statistics."
            logging.info(message)
            return message

        ratings = []
        for movie in self.movies.values():
            rating = movie.get('rating') or movie.get('imdbRating') or movie.get('score')
            if rating:
                try:
                    ratings.append(float(rating))
                except ValueError:
                    logging.warning(f"Invalid rating found for movie: {movie.get('title', 'Unknown')}")

        if ratings:
            avg_rating = stat.mean(ratings)
            highest_rating = max(ratings)
            lowest_rating = min(ratings)
            message = (
                f"Average Rating: {avg_rating:.2f}\n"
                f"Highest Rating: {highest_rating:.2f}\n"
                f"Lowest Rating: {lowest_rating:.2f}"
            )
            logging.info(message)
            return message
        else:
            message = "No valid ratings available."
            logging.info(message)
            return message

    def show_random_movie(self) -> str:
        """Show a random movie from the collection."""
        if self.movies:
            # Create a list of movies that have valid titles and ratings
            valid_movies = [movie for movie in self.movies.values() if 'Title' in movie and 'imdbRating' in movie]

            if valid_movies:
                random_movie = random.choice(valid_movies)
                # Safely get the title and rating
                movie_title = random_movie.get('Title', 'Unknown Title')
                movie_rating = random_movie.get('imdbRating', 'N/A')
                message = f"Random Movie: {movie_title} (Rating: {movie_rating})"
                return message
            else:
                return "No valid movies available to display."
        else:
            return "No movies available."

    def search_movie(self, title: str) -> str:
        """Search for a movie by title using fuzzy matching."""
        titles = list(self.movies.keys())
        match, score = process.extractOne(title.lower(), titles)
        if score >= 80:  # Adjust the threshold if needed
            movie = self.movies[match]
            movie_title = movie.get('Title', 'Unknown Title')
            movie_rating = movie.get('imdbRating', 'N/A')
            message = f"Movie Found: {movie_title} (Rating: {movie_rating})"
            logging.info(message)
            return message
        else:
            message = f"No match found for '{title}'."
            logging.warning(message)
            return message

    def sort_movies_by_rating(self) -> str:
        """Sort movies by their rating and display them."""
        sorted_movies = sorted(self.movies.items(), key=lambda x: float(x[1].get('imdbRating', 0)), reverse=True)
        sorted_list = [f"{movie['Title']} - Rating: {movie.get('imdbRating', 'N/A')}" for title, movie in sorted_movies]
        sorted_list_str = "\n".join(sorted_list)
        logging.info(sorted_list_str)
        return sorted_list_str
