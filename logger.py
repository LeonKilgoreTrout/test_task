from loguru import logger
import sys
from time import time


config = {
    "handlers": [
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
