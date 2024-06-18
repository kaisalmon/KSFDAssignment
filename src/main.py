from logic.logging import setup_logging
from main_types import Config
from primary_adapters.cli import process_cli

if __name__ == "__main__":
    logger = setup_logging(False)
    config = Config(
        logger=logger,
    )
    process_cli(config)