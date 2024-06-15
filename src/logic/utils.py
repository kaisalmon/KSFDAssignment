from typing import List, Dict, Tuple, Iterator, Any

def iterate_results(gen: Iterator[Dict[str, Any]]) -> Iterator[Tuple[Dict[str, Any], Exception]]:
    while True:
        try:
            yield (next(gen), None)
        except StopIteration:
            break
        except Exception as e:
            yield (None, e)