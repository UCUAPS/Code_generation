"""
This code solves film ranking task.
"""
import time
def temp(item):
    """
    Temporary function to substitute lambda func.
    """
    return (-item[1], item[0])

def read_file(pathname: str, year: int=0) -> list[list[str]]:
    """
    This function reads a file from the path(pathname)
    and returns a list of films created in a particular year(year)
    --------------------------------------------------------------
    param: pathname(str) - path to a file with content,
           year(int) - a year when film was created
    return: list[list[str]]
    
    >>> read_file('films.csv', 2014)[:2] ==\
 [['1', 'Guardians of the Galaxy', 'Action,Adventure,Sci-Fi',\
 'A group of intergalactic criminals are forced to work together to stop\
 a fanatical warrior from taking control of the universe.', 'James Gunn',\
 'Chris Pratt, Vin Diesel, Bradley Cooper, Zoe Saldana', '2014', '121', '8.1',\
 '757074', '333.13', '76.0'],\
 ['3', 'Split', 'Horror,Thriller', 'Three girls are kidnapped by a man with a\
 diagnosed 23 distinct personalities. They must try to escape before the apparent\
 emergence of a frightful new 24th.', 'M. Night Shyamalan', 'James McAvoy, Anya Taylor-Joy,\
 Haley Lu Richardson, Jessica Sula', '2016', '117', '7.3', '157606', '138.12', '62.0']]
    True
    >>> read_file('films.csv', 2016)[:1] ==\
 [['3', 'Split', 'Horror,Thriller', 'Three girls are kidnapped by\
 a man with a diagnosed 23 distinct personalities. They must try\
 to escape before the apparent emergence of a frightful new 24th.',\
 'M. Night Shyamalan', 'James McAvoy, Anya Taylor-Joy, Haley Lu Richardson,\
 Jessica Sula', '2016', '117', '7.3', '157606', '138.12', '62.0']]
    True
    """
    films_in_year = []
    with open(pathname, mode='r', encoding='utf-8') as file:
        next(file)
        for line in file:
            line = line.strip().split(';')
            if int(line[6]) >= year:
                films_in_year.append(line)
    return films_in_year

def actors_rating(movies:list) -> dict[str, int]:
    """
    This function gets maximum ranking for an actor.
    """
    rating = {}
    for movie in movies:
        for actor in movie[5].split(','):
            if actor in rating:
                rating[actor] = max(float(movie[8]), rating[actor])
            else:
                rating.setdefault(actor, float(movie[8]))
    return rating

def movie_rating(data_f: list, act_rating:dict) -> dict:
    """
    This function finds film rating from it's actors' ranking.
    """
    movie_rank = {movie[1]:[] for movie in data_f}
    for movie in data_f:
        actors = movie[5].strip().split(',')
        for actor in actors:
            movie_rank[movie[1]].append(act_rating[actor])
    return movie_rank


def top_n(data_f: list, genre: str='', n:int=0) -> list[tuple[str]]:
    """
    This function takes list of films, desired genre and number of films.
    It ranks them according to the acotors' ratings in data_f.
    ---------------------------------------------------------------------
    param: data_f(list) - list of movies
           genre(str) - desired genre
           n(int) - ranks from 1 up to 1 + n
    return: list[tuple[str]] list of movies,
    represented in tuples ('Name of movie', actors score)

    >>> top_n(read_file('films.csv', 2014), genre='Action', n=5)
    [('Dangal', 8.8), ('Bahubali: The Beginning', 8.3),\
 ('Guardians of the Galaxy', 8.1),\
 ('Star Wars: Episode VII - The Force Awakens', 8.1),\
 ('Mad Max: Fury Road', 8.1)]
    >>> top_n(read_file('films.csv', 2015), genre='', n=6)
    [('Dangal', 8.8), ('Kimi no na wa', 8.6),\
 ('Koe no katachi', 8.4), ('La La Land', 8.3),\
 ('Bahubali: The Beginning', 8.3), ('Paint It Black', 8.3)]
    """
    rating_of_act = actors_rating(data_f) # 'Will Smith' : [8.1]
    movie_score = movie_rating(data_f, rating_of_act) # 'Interstellar': [5.6, 8.1, 9.2]
    final = []
    for movie in data_f:
        if genre in movie[2].strip().split(','):
            final.append((movie[1], sum(movie_score[movie[1]]) / len(movie_score[movie[1]])))
    return sorted(final, key=temp)[:n] if n>0 else sorted(final, key=temp)

def write_file(top: list, file_name: str):
    """
    This function writes film-top to a
    separate file.
    ----------------------------------
    param: top(list) - film-top in list[tuple] form
           file_name(str) - name of file to write in.
    return: None

    >>> data_f = read_file('films.csv', 2014)
    >>> top = top_n(data_f, 'Action', 5)
    >>> write_file(top, 'films_top.txt')
    >>> with open('films_top.txt', mode='r', encoding='utf-8') as file:
    ...     content = file.readlines()
    >>> content == ['Dangal, 8.8\\n',\
'Bahubali: The Beginning, 8.3\\n',\
'Guardians of the Galaxy, 8.1\\n',\
'Star Wars: Episode VII - The Force Awakens, 8.1\\n',\
'Mad Max: Fury Road, 8.1\\n']
    True
    """
    with open(file_name, mode='w', encoding='utf-8') as file:
        for film in top:
            file.write(f'{film[0]}, {film[1]}\n')

start_time = time.time()

data = read_file('films.csv', 2014)
act_rt = actors_rating(data)
mv_rt = movie_rating(data, act_rt)
top_own = top_n(data, 'Action', 3)
write_file(top_own,'films_top.txt')
end_time = time.time()

execution_time = end_time - start_time
print(f'executino_time = {execution_time:.4f}')