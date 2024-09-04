import json

class Movie_web_site_generator:
    def __init__(self, movies, output_file):
        self.movies = movies
        self.output_file = output_file

    def generate_movie_html(self):
        """Generates HTML for a list of movies."""
        if not self.movies:
            return "<p>No movies available.</p>"

        movie_items = ""
        for movie in self.movies.values():  # Iterate over movie values, not keys
            title = movie.get('title', 'No title')
            year = movie.get('year', 'Unknown')
            rating = movie.get('rating', 'N/A')
            actors = movie.get('actors', 'N/A')
            poster = movie.get('poster', 'N/A')

            movie_items += f"""
            <li class="movie-item">
                <div class="movie-info">
                    <h2 class="movie-title">{title}</h2>
                    <p class="movie-year"><strong>Year:</strong> {year}</p>
                    <p class="movie-rating"><strong>Rating:</strong> {rating}</p>
                    <p class="movie-actors"><strong>Actors:</strong> {actors}</p>
                    <p class="movie-poster"><strong>Poster:</strong><br><img src="{poster}" alt="{title} poster" style="width:150px;height:auto;"/></p>
                </div>
            </li>
            """
        return movie_items

    def generate_html(self):
        """Generates the full HTML content and writes it to a file."""
        movie_html = self.generate_movie_html()

        html_template = """
        <!DOCTYPE html>
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
            <ul class="movie-list">
                __REPLACE_MOVIE_INFO__
            </ul>
        </div>
        </body>
        </html>
        """

        html_content = html_template.replace("__REPLACE_MOVIE_INFO__", movie_html)

        with open(self.output_file, "w", encoding="utf-8") as file:
            file.write(html_content)
