from docarray import DocList, BaseDoc
from main_types import Config
from vectordb import InMemoryExactNNVectorDB
from docarray.typing import NdArray
from typing import List
from logic.movie import Movie, MovieQuery

class MovieDoc(BaseDoc):
    record_id: int
    movie_id: int
    title: str
    country: str
    release_year: int
    description: str
    embedding: NdArray[1536]

def create_movie_vectordb(movies: List[Movie], config: Config) -> InMemoryExactNNVectorDB[MovieDoc]:
    logger = config.logger
    logger.info("Creating db")
    db = InMemoryExactNNVectorDB[MovieDoc](workspace=config.workspace_path)

    doc_list = []
    error_count = 0
    for movie in movies:
        try: 
            movie_doc = MovieDoc(
                record_id=movie.record_id,
                movie_id=movie.movie_id,
                title=movie.title,
                country=movie.country,
                release_year=movie.release_year,
                description=movie.description,
                embedding=movie.vector_embedding
            )
            doc_list.append(movie_doc)
        except Exception as e:
            error_count+=1
            config.logger.error(e)
    
    logger.debug(f"loaded {len(doc_list)} docs")
    if error_count > 0:
            logger.warning(f"Encountered {error_count} error(s)")
    
    db.index(inputs=DocList[MovieDoc](doc_list))
    logger.debug(f"Indexed Successfully")
    return db

def search_movies(db: InMemoryExactNNVectorDB[MovieDoc], query:MovieQuery, limit: int = 10) -> List[MovieDoc]:
    query_embedding = query.vector_embedding
    querydoc = MovieDoc(
        record_id=-1,
        movie_id=-1,
        title="",
        country="",
        release_year=-1,
        description="",
        embedding=query_embedding
    )

    max_release_year = query.max_release_year
    min_release_year = query.min_release_year

    results = db.search(inputs=DocList[MovieDoc]([querydoc]))    

    filtered_results = []

    for match in results[0].matches:
        if min_release_year <= match.release_year <= max_release_year:
            filtered_results.append(match)
        if len(filtered_results) >= limit:
            return filtered_results

    return filtered_results