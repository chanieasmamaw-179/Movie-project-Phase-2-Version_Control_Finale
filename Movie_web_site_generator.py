class Movie_web_site_generator:
    """
    Attributes:
        movies (dict): A dictionary containing movie data where keys are movie titles
                       and values are dictionaries with details like 'Title', 'Year',
                       'Rating', 'Actors', and 'Poster'.
        output_file (str): The name of the output HTML file where the movie collection
                           will be saved.

    Methods:
        generate_html(): Generates HTML content for the movie collection and writes it
                         to the specified output file.
    """

    def __init__(self, movies, output_file):
        """
        Initializes the Movie_web_site_generator with a movie collection and output file name.

        Args:
            movies (dict): A dictionary of movies to be displayed.
            output_file (str): The name of the HTML file to generate.
        """
        self.movies = movies
        self.output_file = output_file

    def generate_html(self):
        """
        Generates HTML content for the movie collection and writes it to the output file.

        The generated HTML includes a list of movies with their titles, release years,
        ratings, actors, and posters. The layout is styled using an external CSS file.
        """
        html_content = """<!DOCTYPE html>
        <html>
        <head>
            <title>My Movie App</title>
            <link rel="stylesheet" href="style.css"/>
        </head>
        <body>
        <div class="list-movies-title">
            <h1>My Movie Collection</h1>
        </div>
        <div>
            <ul class="movie-grid">
        """  # Changed from "movie-list" to "movie-grid" to match CSS

        # Generate movie list items
        for movie in self.movies.values():
            html_content += f"""
            <li class="movie-item">
                <div class="movie-info">
                    <img src="{movie.get('Poster', 'N/A')}" alt="{movie.get('Title', 'No title')} poster" class="movie-poster"/>
                    <h2 class="movie-title">{movie.get('Title', 'No title')}</h2>
                    <p class="movie-year"><strong>Year:</strong> {movie.get('Year', 'Unknown')}</p>
                    <p class="movie-rating"><strong>Rating:</strong> {movie.get('Rating', 'N/A')}</p>
                    <p class="movie-actors"><strong>Actors:</strong> {movie.get('Actors', 'N/A')}</p>
                </div>
            </li>
            """

        # Closing tags for HTML
        html_content += """
            </ul>
        </div>
        </body>
        </html>
        """

        # Write the HTML content to the output file
        with open(self.output_file, 'w', encoding='utf-8') as file:
            file.write(html_content)
            print(f"Webpage '{self.output_file}' has been generated and saved.")
