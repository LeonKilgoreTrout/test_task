from loguru import logger
import sys
from typing import Any, Dict
from time import time


config = {
    "handlers": [
        # {
        #     "sink": "../logs/logs.log",
        #     "format": "{message}",
        #     "rotation": "5 MB"
        # },
        {
            "sink": sys.stdout,
            "format": "{message}"
        }
    ]
}

logger.remove()
logger.configure(**config)


def log(message: str, **kwargs) -> None:
    data = {
        "message": message,
        "info": str(kwargs),
        "timestamp": time()
    }
    logger.info(data)
