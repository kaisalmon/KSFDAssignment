from tabulate import tabulate
import logging
import sys

from main_types import Config
from secondary_adapters.csvloader import load_dataset, load_query
from secondary_adapters.vectordb import create_movie_vectordb, search_movies


def setup_logging() -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(message)s', '%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

def main(config: Config) -> None:
    config.logger.info("Starting FocalData assessment CLI application")
    dataset = load_dataset(config.dataset_path, config)
    db = create_movie_vectordb(dataset, config)
    query = load_query(config.query_path, config)
    min_release_year =-10000
    max_release_year = 10000
    query.max_release_year = max_release_year
    query.min_release_year = min_release_year
    results = search_movies(db, query)

    table = True
    if table:
        table_results = [
            {
                "record_id": result.record_id,
                "movie_id": result.movie_id,
                "country": result.country,
                "release_year": result.release_year,
                "title": result.title,
                "description": result.description[0:100]
            } for result in results
        ]
        print(tabulate(table_results))
    else:
        for result in results:
            print(result.record_id, result.movie_id, result.title, result.description)

if __name__ == "__main__":
    logger = setup_logging()
    config = Config(
        logger=logger,
        workspace_path="workspace",
        dataset_path="datasets\interview_dataset_movies.csv",
        query_path="queries\interview_query_movies.csv"
    )
    main(config)