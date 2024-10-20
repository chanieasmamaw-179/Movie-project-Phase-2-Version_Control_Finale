class Movie_web_site_generator:
    """
    Attributes:
        movies (dict): A dictionary containing movie data where keys are movie titles
                       and values are dictionaries with details like 'Title', 'Year',
                       'Rating', 'Actors', and 'Poster'.
        output_file (str): The name of the output HTML file where the movie collection
                           will be saved.

    Methods:
        format_rating(rating): Formats the rating to ensure it is a string with at most one decimal place.
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

    def format_rating(self, rating):
        """
        Formats the rating to ensure it is a string with at most one decimal place.

        Args:
            rating (float or str): The rating to format.

        Returns:
            str: Formatted rating string or "Not Available" if input is invalid.
        """
        print(f"Received rating: {rating} (type: {type(rating)})")  # Debugging line
        if rating is None:  # Explicitly check for None
            return "Not Available"

        if isinstance(rating, (float, int)):
            return f"{rating:.1f}"  # Directly format if it's a number
        elif isinstance(rating, str) and rating.strip():  # Check if it's a non-empty string
            try:
                # Print the string before conversion for debugging
                print(f"Trying to convert rating string: '{rating}'")
                return f"{float(rating):.1f}"  # Attempt to convert and format
            except ValueError:
                print(f"ValueError: Could not convert '{rating}' to float.")  # Debugging line
                return "Not Available"  # Handle invalid conversion

        return "Not Available"  # Handle empty, None, or invalid cases

    def generate_html(self):
        """
        Generates HTML content for the movie collection and writes it to the output file.

        The generated HTML includes a list of movies with their titles, release years,
        ratings, actors, and posters. The layout is styled using an external CSS file.
        """
        html_content = """<!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>My Movie App</title>
            <link rel="stylesheet" href="style.css"/>
        </head>
        <body>
        <div class="list-movies-title">
            <h1>My Movie Collection</h1>
        </div>
        <div>
            <ul class="movie-grid">
        """

        # Generate movie list items
        for movie in self.movies.values():
            title = movie.get('Title', 'No title')
            year = movie.get('Year', 'Unknown')
            rating = movie.get('Rating')

            # Use format_rating to get the formatted rating
            formatted_rating = self.format_rating(rating)

            actors = movie.get('Actors', 'N/A')
            poster = movie.get('Poster')

            # Validate poster URL
            poster_html = (
                f'<img src="{poster}" alt="{title} poster" class="movie-poster"/>'
                if poster else
                '<div class="no-poster">No Image Available</div>'
            )

            html_content += f"""
            <li class="movie-item">
                <div class="movie-info">
                    {poster_html}
                    <h2 class="movie-title">{title}</h2>
                    <p class="movie-year"><strong>Year:</strong> {year}</p>
                    <p class="movie-rating"><strong>Rating:</strong> {formatted_rating}</p>
                    <p class="movie-actors"><strong>Actors:</strong> {actors}</p>
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
        try:
            with open(self.output_file, 'w', encoding='utf-8') as file:
                file.write(html_content)
                print(f"Webpage '{self.output_file}' has been generated and saved.")
        except IOError as e:
            print(f"An error occurred while writing to the file: {e}")

# Example usage:
# movies_data = {
#     'Inception': {'Title': 'Inception', 'Year': 2010, 'Rating': 8.8, 'Actors': 'Leonardo DiCaprio', 'Poster': 'inception.jpg'},
#     'Interstellar': {'Title': 'Interstellar', 'Year': 2014, 'Rating': '8.6', 'Actors': 'Matthew McConaughey', 'Poster': 'interstellar.jpg'},
# }
# generator = Movie_web_site_generator(movies_data, 'movies.html')
# generator.generate_html()
