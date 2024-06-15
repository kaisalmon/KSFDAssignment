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
    results = search_movies(db, query)
    for result in results:
        print(result.title)

if __name__ == "__main__":
    logger = setup_logging()
    config = Config(
        logger=logger,
        workspace_path="workspace",
        dataset_path="datasets\interview_dataset_movies.csv",
        query_path="queries\interview_query_movies.csv"
    )
    main(config)