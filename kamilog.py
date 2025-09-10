"""kamilog.py"""

# TODO module docstring

# todo allow use relative time
# todo time allow omit date

import logging
from logging import Formatter, StreamHandler

__all__ = ("getLogger",)
__version__ = "1.0.0"
__author__ = "kamiLeL"


MESSAGE_FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"


_PADDED_LEVELNAMES = ("DEBUG", "INFO ", "WARN ", "ERROR", "CRIT ")


def _levelno2padded_levelname(levelno):
    """
    :param levelno:
    :type levelno: int
    :return: padded level name, always 5 letter width
    :rtype: str
    """
    return _PADDED_LEVELNAMES[levelno // 10 - 1]


class _LogFormatter(Formatter):

    def __init__(
        self,
        fmt=MESSAGE_FORMAT,
        datefmt=None,
        style="%",
        validate=True,
        *,
        defaults=None
    ):
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)

    def format(self, record):
        record.levelname = _levelno2padded_levelname(record.levelno)
        return super().format(record)


_INITIALIZED_LOGGERS = []


def getLogger(name=None):
    """
    :param name: logger name
    :type name: str
    :return: a logger with the `name`, create if non-existence;
            root logger if `name` is `None`
    :rtype: logging.Logger
    """
    global _INITIALIZED_LOGGERS

    logger = logging.getLogger(name)

    # no repeated configure/initialize for any loggers
    if name in _INITIALIZED_LOGGERS:
        return logger

    # init loggers  ============================================================
    # console stream handler  --------------------------------------------------
    console_handler = StreamHandler()
    console_formatter = _LogFormatter()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # todo add file handler

    _INITIALIZED_LOGGERS.append(name)

    return logger
