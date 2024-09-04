import json
import requests
from storage_interface import StorageInterface

class JSONStorage(StorageInterface):
    DATA_FILE = 'data.json'
    API_KEY = ""  # Consider setting this via the constructor for flexibility

    def get_movies(self):
        """Load movies from the JSON file."""
        try:
            with open(self.DATA_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error loading movies: {e}")
            return {}  # Return an empty dictionary if there's a JSON decoding error
        except FileNotFoundError:
            print("Movies file not found.")
            return {}  # Return an empty dictionary if the file is not found

    def fetch_movie_info(self, movie_title):
        """Fetch movie information from an external API."""
        url = f"https://www.omdbapi.com/?apikey={self.API_KEY}&t={movie_title}"  # Corrected URL and usage of API key
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  # Return the JSON response
        else:
            print(f"Error fetching movie: {response.status_code}")
            return None  # Return None to handle errors appropriately

    def save_movies(self, movies):
        """Save movies to the JSON file."""
        with open(self.DATA_FILE, 'w') as file:
            json.dump(movies, file, indent=4)  # Save the movies data with indentation for readability

class MovieStorage:
    def __init__(self, storage_type: str):
        if storage_type == 'json':
            self.storage = JSONStorage()
        # elif storage_type == 'csv':
        #     self.storage = CSVStorage()  # Example of how you could expand this later
        else:
            raise ValueError(f"Unsupported storage type: {storage_type}")

    def get_movies(self):
        return self.storage.get_movies()

    def save_movies(self, movies):
        self.storage.save_movies(movies)
