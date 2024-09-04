from abc import ABC, abstractmethod


class StorageInterface(ABC):
	
	@abstractmethod
	def get_movies(self):
		"""Load movies from storage."""
		pass
	
	@abstractmethod
	def save_movies(self, movies):
		"""Save movies to storage."""
		pass
