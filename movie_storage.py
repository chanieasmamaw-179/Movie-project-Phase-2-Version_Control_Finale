import json
import requests
import csv
from storage_interface import StorageInterface
from typing import Dict, Optional

class JSONStorage(StorageInterface):
    """Class to handle JSON file storage for movies."""

    def __init__(self, api_key: str = ""):
        self.DATA_FILE = 'data.json'  # JSON file for movie storage
        self.API_KEY = api_key  # Set API key via the constructor

    def get_movies(self) -> Dict[str, dict]:
        """Load movies from the JSON file."""
        try:
            with open(self.DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error loading movies: {e}")
            return {}
        except FileNotFoundError:
            print("Movies file not found. Returning an empty movie collection.")
            return {}

    def fetch_movie_info(self, movie_title: str) -> Optional[dict]:
        """Fetch movie information from an external API."""
        url = f"https://www.omdbapi.com/?apikey={self.API_KEY}&t={movie_title}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  # Return the JSON response
        else:
            print(f"Error fetching movie: {response.status_code}")
            return None  # Return None to handle errors appropriately

    def save_movies(self, movies: Dict[str, dict]):
        """Save movies to the JSON file."""
        with open(self.DATA_FILE, 'w', encoding="utf-8") as file:
            json.dump(movies, file, indent=4)  # Save the movies data with indentation for readability


class CSVStorage(StorageInterface):
    """Class to handle CSV file storage for movies."""

    def __init__(self):
        self.DATA_FILE = 'movies.csv'  # CSV file for movie storage

    def get_movies(self) -> Dict[str, dict]:
        """Load movies from the CSV file."""
        movies = {}
        try:
            with open(self.DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title_lower = row['title'].lower()
                    movies[title_lower] = row  # Store the movie data indexed by title (lowercased)
        except FileNotFoundError:
            print("CSV file not found. Returning an empty movie collection.")
        return movies

    def save_movies(self, movies: Dict[str, dict]):
        """Save movies to the CSV file."""
        with open(self.DATA_FILE, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['title', 'rating', 'year', 'actors', 'poster']  # Added fields for actors and poster
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # Write the header row
            for movie in movies.values():
                # Ensure all required fields are present in the movie dictionary
                writer.writerow({field: movie.get(field, '') for field in fieldnames})


class MovieStorage:
    """Class to handle storage of movies in both JSON and CSV formats."""

    def __init__(self, api_key: str = ""):
        self.json_storage = JSONStorage(api_key)  # Create an instance of JSONStorage
        self.csv_storage = CSVStorage()  # Create an instance of CSVStorage

    def get_movies(self) -> Dict[str, dict]:
        """Retrieve movies from the storage (use JSON as the primary source)."""
        return self.json_storage.get_movies()

    def fetch_movie_info(self, movie_title: str) -> Optional[dict]:
        """Fetch movie information via the JSON storage (API-based)."""
        return self.json_storage.fetch_movie_info(movie_title)  # Delegate the call to JSONStorage

    def save_movies(self, movies: Dict[str, dict]):
        """Save movies to both JSON and CSV formats."""
        # Save movies to JSON
        self.json_storage.save_movies(movies)
        # Save movies to CSV
        self.csv_storage.save_movies(movies)
