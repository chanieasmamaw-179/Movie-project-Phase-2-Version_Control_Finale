import json
import requests
from typing import Dict
from storage_interface import StorageInterface

class MovieStorage(StorageInterface):
    """Class for managing movie storage, including API interactions."""

    def __init__(self, api_key: str):
        """Initialize the storage with an API key."""
        self.api_key = api_key
        self.movies_file = "movies.json"

    def get_movies(self) -> Dict:
        """Load movies from a JSON file."""
        try:
            with open(self.movies_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print("Error: The movies file is not a valid JSON.")
            return {}

    def save_movies(self, movies: Dict) -> None:
        """Save the current movies to a JSON file."""
        with open(self.movies_file, "w", encoding="utf-8") as file:
            json.dump(movies, file, ensure_ascii=False, indent=4)

    def fetch_movie_info(self, title: str) -> Dict:
        """Fetch movie information from an external API using the provided title."""
        url = f"http://www.omdbapi.com/?t={title}&apikey={self.api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching data for '{title}': {response.status_code}")
            return {}
