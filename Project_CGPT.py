import time

def read_file(pathname: str, year: int = 0):
    """
    Reads data from a CSV file and returns a list of movies. Filters movies
    based on the year if specified.

    Parameters:
        pathname (str): Path to the file.
        year (int): Year after which movies will be included (default is 0,
                    meaning all movies).

    Returns:
        list: A list of movies, where each movie is represented as a list of
              attributes (strings).
    """
    movies = []

    with open(pathname, mode='r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines[1:]:
        row = line.strip().split(';')
        if int(row[6]) >= year:
            movies.append(row)

    return movies


def get_actor_ratings(data):
    """
    Creates a dictionary of actor names and their highest movie rating.

    Parameters:
        data (list): A list of movies, where each movie is represented as a list
                     of attributes (strings).

    Returns:
        dict: A dictionary where keys are actor names and values are their highest movie ratings.
    """
    actor_ratings = {}

    for movie in data:
        actors = movie[5].split(',')
        rating = float(movie[8])

        for actor in actors:
            actor = actor.strip()
            if actor not in actor_ratings:
                actor_ratings[actor] = rating
            else:
                actor_ratings[actor] = max(actor_ratings[actor], rating)

    return actor_ratings


def actor_rating(actors, data, actor_ratings):
    """
    Calculates the average rating for the actors in the movie.

    Parameters:
        actors (str): A string of actors' names separated by commas.
        data (list): A list of movies, where each movie is represented as a list
                     of attributes (strings).
        actor_ratings (dict): A dictionary with actor names and their highest movie ratings.

    Returns:
        float: The average actor rating for the movie.
    """
    actor_ratings_list = []

    for actor in actors.split(','):
        actor = actor.strip()
        if actor in actor_ratings:
            actor_ratings_list.append(actor_ratings[actor])

    if actor_ratings_list:
        return sum(actor_ratings_list) / len(actor_ratings_list)
    return 0


def top_n(data: list, genre: str = '', n: int = 0):
    """
    Returns a list of top n movies based on their rating and the average actor
    rating. Sorts movies first by the average rating, then by title in
    lexicographical order.

    Parameters:
        data (list): A list of movies, where each movie is represented as a list
                     of attributes (strings).
        genre (str): Genre to filter movies by (can include multiple genres
                     separated by commas).
        n (int): Number of movies to return (0 means returning all movies).

    Returns:
        list: A list of top movies as tuples (Title, Average_rating).
    """
    actor_ratings = get_actor_ratings(data)
    filtered_movies = []

    for movie in data:
        movie_genres = movie[2].split(',')
        if genre and not any(g.strip() in genre.split(',') for g in movie_genres):
            continue

        movie_rating = float(movie[8])
        actors_avg_rating = actor_rating(movie[5], data, actor_ratings)
        avg_rating = (movie_rating + actors_avg_rating) / 2

        filtered_movies.append((movie[1], avg_rating))
    filtered_movies.sort(key=compare_movies_sort_key)

    return filtered_movies[:n] if n > 0 else filtered_movies


def compare_movies_sort_key(movie):
    """
    This function is used as a key for sorting movies.
    It returns a tuple (negative average rating, title), so that sorting works
    first by average rating in descending order, and if ratings are the same,
    it sorts lexicographically by title.

    Parameters:
        movie (tuple): A tuple (Title, Average_rating)

    Returns:
        tuple: Sorting key (negative rating, title)
    """
    return (-movie[1], movie[0])


def write_file(top: list, file_name: str):
    """
    Writes the top movies to a file, where each movie is listed as "Title,
    rating".

    Parameters:
        top (list): A list of top movies as tuples (Title, rating).
        file_name (str): The name of the file to write the results to.
    """
    with open(file_name, mode='w', encoding='utf-8') as file:
        for title, rating in top:
            file.write(f"{title}, {rating}\n")

start_time = time.time()
data = read_file('films.csv', 2014)
top_movies = top_n(data, genre='Action', n=5)
write_file(top_movies, 'films_top.txt')
end_time = time.time()

execution_time = end_time - start_time
print(f'execution_time = {execution_time:.4f}')