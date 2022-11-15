from project.core.helpers.custom_log import get_logger

logger = get_logger()


def is_empty(obj):
    try:
        if obj is None:
            return True
        if len(obj) == 0:
            return True
    except TypeError as e1:
        logger.error(e1)
        return False
    except Exception as e2:
        logger.error(e2)
        return False
    return False
