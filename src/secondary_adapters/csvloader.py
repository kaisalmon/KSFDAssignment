import csv
from typing import List, Dict, Tuple, Iterator, Any
from logic.utils import iterate_results
from logic.movie import Movie, MovieQuery
from main_types import Config


def load_query(path: str, _: Config) -> MovieQuery:
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile) 
        row = next(reader)
        try:
            query = MovieQuery.from_dict(row)  
        except KeyError as e:
            raise ValueError("Could not parse query")
        except ValueError as e:
            raise ValueError("Could not parse query")
        return query

def load_dataset(path: str, conf: Config) -> List[Movie]:
    error_count = 0
    logger = conf.logger
    result: List[Movie] = []
    id = 1
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for (row, error) in iterate_results(reader):
            if error:
                error_count += 1
                logger.warning(error)
                continue
            try:
                row["record_id"] = id
                movie = Movie.from_dict(row)
                result.append(movie)
                id+=1
            except (ValueError, KeyError, TypeError) as e:
                error_count += 1
                logger.warning(e)
    conf.logger.debug(f"loaded {len(result)} records")
    if error_count > 0:
        conf.logger.warning(f"Encountered {error_count} error(s)")
    return result