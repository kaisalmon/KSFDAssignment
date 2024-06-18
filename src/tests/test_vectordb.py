import unittest
from logic.movie import Movie, MovieQuery
from secondary_adapters.vectordb import search_movies

class TestSearch2DMovies(unittest.TestCase):
    def setUp(self):
        self.movies = [
            Movie(record_id=1, movie_id=1, title="North", country="A", release_year=1, description="Blah", vector_embedding=[0, 1]),
            Movie(record_id=2, movie_id=2, title="East", country="B", release_year=2, description="Blah", vector_embedding=[1, 0]),
            Movie(record_id=3, movie_id=3, title="South", country="B", release_year=2, description="Blah", vector_embedding=[0, -1]),
            Movie(record_id=4, movie_id=4, title="West", country="C", release_year=4, description="Blah", vector_embedding=[-1, 0]),
        ]

    def test_search_movies(self):
        query = MovieQuery(min_release_year=0, max_release_year=5, query="North West West", vector_embedding=[-0.6, 0.3])
        results = search_movies(self.movies, query, limit=2)
        north_result = next(((movie, distance)  for (movie, distance) in results if movie.title == "North"), None)
        west_result = next(((movie, distance)  for (movie, distance) in results if movie.title == "West"), None)
        assert west_result, "One of the results should be West"
        assert north_result, "One of the results should be North"

    def test_search_movies_filter_high(self):
        query = MovieQuery(min_release_year=4, max_release_year=5, query="North West West", vector_embedding=[-0.6, 0.3])
        results = search_movies(self.movies, query, limit=4)
        assert len(results)==1, "Only one result should be returned"
        (movie, _) = results[0]
        assert movie.title == "West"
        
    def test_search_movies_filter_low(self):
        query = MovieQuery(min_release_year=1, max_release_year=1, query="North West West", vector_embedding=[-0.6, 0.3])
        results = search_movies(self.movies, query, limit=4)
        assert len(results)==1, "Only one result should be returned"
        (movie, _) = results[0]
        assert movie.title == "North"

    def test_search_movies_no_results(self):
        query = MovieQuery(min_release_year=100, max_release_year=100, query="No results", vector_embedding=[0,0])
        results = search_movies(self.movies, query, limit=4)
        assert len(results)==0, "No results returned"

if __name__ == '__main__':
    unittest.main()