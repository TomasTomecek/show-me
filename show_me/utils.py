import logging
import os
from pathlib import Path


def set_logging(
        logger_name="show_me",
        level=logging.DEBUG,
        handler_class=logging.StreamHandler,
        handler_kwargs=None,
        format='%(asctime)s.%(msecs).03d %(filename)-17s %(levelname)-6s %(message)s',
        date_format='%H:%M:%S'):
    """
    Set personal logger for this library.

    :param logger_name: str, name of the logger
    :param level: int, see logging.{DEBUG,INFO,ERROR,...}: level of logger and handler
    :param handler_class: logging.Handler instance, default is StreamHandler (/dev/stderr)
    :param handler_kwargs: dict, keyword arguments to handler's constructor
    :param format: str, formatting style
    :param date_format: str, date style in the logs
    :return: logger instance
    """
    logger = logging.getLogger(logger_name)
    # do we want to propagate to root logger?
    # logger.propagate = False
    logger.setLevel(level)

    # don't readd handler
    if not [x for x in logger.handlers if isinstance(x, handler_class)]:
        handler_kwargs = handler_kwargs or {}
        handler = handler_class(**handler_kwargs)
        handler.setLevel(level)
        formatter = logging.Formatter(format, date_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def get_cache_dir() -> Path:
    p = os.getenv("XDG_CACHE_HOME", None)
    if p is None:
        return Path.home().joinpath(".cache")
    return Path(p).resolve()


def get_cache_file_path() -> Path:
    return get_cache_dir().joinpath("show-me.json")
