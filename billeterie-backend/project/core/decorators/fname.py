from functools import wraps
from typing import Callable, Any

from project.core.helpers.custom_log import get_logger

logger = get_logger()


def fname(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        f_name = func.__name__
        logger.info(f'f_{f_name} was called')
        return func(*args, **kwargs)

    return wrapper
