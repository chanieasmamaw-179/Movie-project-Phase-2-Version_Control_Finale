from storage_interface import StorageInterface
import requests
from fuzzywuzzy import fuzz, process
from datetime import datetime
import statistics as stat
import matplotlib.pyplot as plt
import random
import pandas as pd

class MovieCollection:
    """Class to manage a collection of movies."""

    def __init__(self, storage: StorageInterface):
        self.storage = storage
        self.movies = self.storage.get_movies()  # Load movies from storage

    def fetch_movie_data(self, movie_title: str) -> dict:
        """Fetch movie data from an external API or from the local storage."""
        movie = self.movies.get(movie_title.lower())
        if not movie:
            movie = self.storage.fetch_movie_info(movie_title)  # Fetch from API if not found locally
        return movie

    def add_movie(self, title: str):
        """Add a new movie to the collection."""
        movie_data = self.fetch_movie_data(title)
        if movie_data:
            self.movies[title.lower()] = movie_data
            self.storage.save_movies(self.movies)  # Save the updated collection
            print(f"Movie '{title}' added successfully.")
        else:
            print(f"Movie '{title}' not found in the API.")

    def delete_movie(self, title: str):
        """Delete a movie from the collection."""
        if title.lower() in self.movies:
            del self.movies[title.lower()]
            self.storage.save_movies(self.movies)  # Save the updated collection
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found in the collection.")

    def update_movie(self, title: str):
        """Update an existing movie in the collection."""
        if title.lower() in self.movies:
            movie_data = self.fetch_movie_data(title)  # Fetch updated movie data
            if movie_data:
                self.movies[title.lower()] = movie_data
                self.storage.save_movies(self.movies)  # Save the updated collection
                print(f"Movie '{title}' updated successfully.")
            else:
                print(f"Movie '{title}' not found in the API.")
        else:
            print(f"Movie '{title}' not found in the collection.")

    def list_movies(self):
        """List all movies in the collection."""
        if not self.movies:
            print("No movies available.")
        else:
            for title, data in self.movies.items():
                print(f"{title.title()} - Rating: {data.get('rating', 'N/A')}")

    def show_stats(self):
        """Show movie statistics."""
        if not self.movies:
            print("No movies available to show statistics.")
            return
        ratings = [float(movie['rating']) for movie in self.movies.values() if movie.get('rating')]
        if ratings:
            print(f"Average Rating: {stat.mean(ratings):.2f}")
            print(f"Highest Rating: {max(ratings):.2f}")
            print(f"Lowest Rating: {min(ratings):.2f}")
        else:
            print("No ratings available.")

    def show_random_movie(self):
        """Show a random movie from the collection."""
        if self.movies:
            random_movie = random.choice(list(self.movies.values()))
            print(f"Random Movie: {random_movie['title']}")
        else:
            print("No movies available.")

    def search_movie(self, title: str):
        """Search for a movie by title using fuzzy matching."""
        titles = list(self.movies.keys())
        match, score = process.extractOne(title, titles)
        if score >= 80:
            movie = self.movies[match]
            print(f"Movie Found: {movie['title']} (Rating: {movie['rating']})")
        else:
            print(f"No match found for '{title}'.")

    def sort_movies_by_rating(self):
        """Sort movies by their rating and display them."""
        sorted_movies = sorted(self.movies.items(), key=lambda x: float(x[1].get('rating', 0)), reverse=True)
        for title, movie in sorted_movies:
            print(f"{movie['title']} - Rating: {movie.get('rating', 'N/A')}")
