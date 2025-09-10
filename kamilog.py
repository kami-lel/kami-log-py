"""kamilog.py"""

# TODO module docstring

import logging
from logging import Formatter, StreamHandler

__all__ = ("getLogger",)
__version__ = "1.0.0"
__author__ = "kamiLeL"


_INITIALIZED_LOGGERS = []


def _levelno2padded_levelname(levelno):
    """
    :param levelno:
    :type levelno: int
    :return: padded level name, always 5 letter width
    :rtype: str
    """
    if levelno <= 10:
        return "DEBUG"
    elif levelno <= 20:
        return "INFO "
    elif levelno <= 30:
        return "WARN "
    elif levelno <= 40:
        return "ERROR"
    else:
        return "CRIT "


class _KamiLogFormatter(Formatter):

    def format(self, record):
        # TODO implement code
        return super().format(record)


def getLogger(name):
    # TODO docstring
    global _INITIALIZED_LOGGERS

    logger = logging.getLogger(name)

    # no repeated configure/initialize for any loggers
    if name in _INITIALIZED_LOGGERS:
        return logger

    # init loggers  ============================================================
    # console stream handler  --------------------------------------------------
    console_handler = StreamHandler()
    console_formatter = _KamiLogFormatter()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # todo add file handler

    _INITIALIZED_LOGGERS.append(name)

    return logger
