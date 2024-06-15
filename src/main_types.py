
from dataclasses import dataclass
import logging


@dataclass
class Config:
    logger: logging.Logger
    workspace_path: str
    dataset_path: str
    query_path: str