
from dataclasses import dataclass
import logging


@dataclass
class Config:
    logger: logging.Logger
    