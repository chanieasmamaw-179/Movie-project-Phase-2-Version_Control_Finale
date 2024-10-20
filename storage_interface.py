from abc import ABC, abstractmethod
from typing import Dict

class StorageInterface(ABC):
    """Abstract base class for storage interface."""

    @abstractmethod
    def get_movies(self) -> Dict:
        """Retrieve movies from storage."""
        pass

    @abstractmethod
    def save_movies(self, movies: Dict) -> None:
        """Save movies to storage."""
        pass

    @abstractmethod
    def fetch_movie_info(self, title: str) -> Dict:
        """Fetch movie information from an external source."""
        pass
