from dataclasses import dataclass
from typing import List

from logic.movie import Movie
from main_types import Config
from secondary_adapters.csvloader import load_dataset, load_query
from secondary_adapters.vectordb import search_movies


@dataclass
class SearchParams:
    dataset_path: str
    query_path: str
    max_release_year: int
    min_release_year: int
    limit: int

def perform_search(params:SearchParams, config: Config) -> List[Movie]:
    movies = load_dataset(params.dataset_path, config)
    query = load_query(params.query_path, config)
    if params.min_release_year:
        query.min_release_year = params.min_release_year
    if params.max_release_year:
        query.max_release_year = params.max_release_year
    
    results = search_movies(movies, query, limit=params.limit)
    return results