import json
from Movie_web_site_generator import Movie_web_site_generator
from movie import MovieCollection
from movie_storage import MovieStorage

def load_data(file_path):
    """Loads a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON.")
        return {}

def main():
    """Main function to handle command-line interactions for the movie collection."""

    # Set storage type to 'json' as default
    storage_type = 'json'
    storage = MovieStorage()  # JSONStorage and CSVStorage no longer need to be passed here

    # Load movies initially
    movies = storage.get_movies()  # Load existing movies from storage
    movie_collection = MovieCollection(storage)

    while True:
        print("\nMenu")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie")
        print("5. Show statistics")
        print("6. Show random movie")
        print("7. Search movie by title")
        print("8. Show movies sorted by rating")
        print("9. Generate and save movie webpage")

        choice = input("Enter your choice: ")

        try:
            if choice == "0":
                print("Exiting the program. Bye!")
                break
            elif choice == "1":
                movie_collection.list_movies()
            elif choice == "2":
                title = input("Enter movie title: ").strip()
                movie_collection.add_movie(title)
            elif choice == "3":
                title = input("Enter the title of the movie to delete: ").strip()
                movie_collection.delete_movie(title)
            elif choice == "4":
                title = input("Enter the title of the movie to update: ").strip()
                movie_collection.update_movie(title)
            elif choice == "5":
                movie_collection.show_stats()
            elif choice == "6":
                movie_collection.show_random_movie()
            elif choice == "7":
                title = input("Enter the title of the movie to search for: ").strip()
                movie_collection.search_movie(title)
            elif choice == "8":
                movie_collection.sort_movies_by_rating()
            elif choice == "9":
                # Ensure we have movies loaded in the MovieCollection
                movies = movie_collection.movies  # Use movies already loaded in the collection
                if not movies:
                    print("No movies available to generate a webpage.")
                else:
                    generator = Movie_web_site_generator(movies, 'movie_web.html')
                    generator.generate_html()
                    print("Webpage 'movie_web.html' has been generated and saved.")
            else:
                print("Invalid choice. Please try again.")
        except ValueError as e:
            print(f"Value error: {e}. Please check your input and try again.")
        except KeyError as e:
            print(f"Key error: {e}. It seems like a movie was not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
