from sklearn.metrics.pairwise import cosine_distances
from dataclasses import dataclass
from main_types import Config
import numpy as np
from docarray.typing import NdArray
from typing import List, Tuple
from logic.movie import Movie, MovieQuery

def search_movies(movies: List[Movie], query: MovieQuery, limit: int = 10) -> List[Tuple[Movie, float]]:
    max_release_year = query.max_release_year
    min_release_year = query.min_release_year
    query_embedding = np.array(query.vector_embedding)

    filtered_movies = [
        movie
        for movie in movies
        if min_release_year <= movie.release_year <= max_release_year
    ]

    filtered_embeddings = np.array([movie.vector_embedding for movie in filtered_movies])
    if len(filtered_embeddings) == 0:
        return []
    
    cosine_scores = cosine_distances(query_embedding.reshape(1, -1), filtered_embeddings)

    sorted_movies = sorted(zip(filtered_movies, cosine_scores[0]), key=lambda x: x[1], reverse=False)

    top_movies = [(movie, distance) for movie, distance in sorted_movies[:limit]]

    return top_movies