import argparse

from tabulate import tabulate
from logic.logging import setup_logging
from logic.search import SearchParams, perform_search
from main_types import Config

def process_cli(config: Config):
    args = parse_args()
    if args.verbose:
        config.logger = setup_logging(True)
    config.logger.debug("Starting FocalData assessment CLI application")
    results = perform_search(SearchParams(
        dataset_path = args.dataset_path,
        query_path=args.query_path,
        max_release_year=args.max_release_year,
        min_release_year=args.min_release_year,
        limit=args.limit
    ), config)
    print_results(args, results)

def print_results(args, results):
    if args.tabulate:
        tabulated_results = results_to_table(results)
        print(tabulated_results)
    else:
        for (result, _) in results:
            print(result)

def parse_args():
    parser = argparse.ArgumentParser(
                        prog='Movie VectorDB Searcher',
                        description='Returns the most relevant movies in a dataset to a query',
                        epilog='By Kai Salmon, for Focaldata')
    parser.add_argument('-v', '--verbose',
                        action='store_true')
    parser.add_argument('-q', '--query_path',
                        action='store', help="Path for the query csv. Defaults to ./queries/interview_query_movies.csv", default='./queries/interview_query_movies.csv')
    parser.add_argument('-d', '--dataset_path',
                        action='store', help="Path for the dataset csv. Defaults to ./datasets/interview_dataset_movies.csv", default='./datasets/interview_dataset_movies.csv')
    parser.add_argument('-m', '--min_release_year',
                        action='store', help="Minimum release year, defaults to the value from the query.csv", type=int)
    parser.add_argument('-M', '--max_release_year',
                        action='store', help="Maximum release year, defaults to the value from the query.csv", type=int)
    parser.add_argument('-l', '--limit',
                        action='store', help="Number of responses, defaults to 10", default=10, type=int)
    parser.add_argument('-t', '--tabulate',
                        action='store_true', help="Print results as table")
    args = parser.parse_args()
    return args

def results_to_table(results):
    table_results = [
            {
                "distance": distance,
                "record_id": result.record_id,
                "movie_id": result.movie_id,
                "country": result.country,
                "release_year": result.release_year,
                "title": result.title,
                "description": result.description[0:100]
            } for (result, distance) in results
        ]
    tabulated_results = tabulate(table_results)
    return tabulated_results