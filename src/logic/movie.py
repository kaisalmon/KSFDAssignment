
from dataclasses import dataclass
import json
from typing import Any, Dict, List


@dataclass
class Movie:
    record_id: int
    movie_id: int
    title: str
    country: str
    release_year: int
    description: str
    vector_embedding: List[float]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Movie':
        return cls(
            record_id=int(data['record_id']),
            movie_id=int(data['movie_id']),
            title=data['title'],
            country=data['country'],
            release_year=int(data['release_year']),
            description=data['description'],
            vector_embedding=json.loads(data['vector_embedding'])
        )


@dataclass
class MovieQuery:
    min_release_year: int
    max_release_year: int
    query: str
    vector_embedding: List[float]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Movie':
        return cls(
            min_release_year=int(data['min_release_year']),
            max_release_year=int(data['max_release_year']),
            query=data['query'],
            vector_embedding=json.loads(data['vector_embedding'])
        )
