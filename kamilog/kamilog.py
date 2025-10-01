"""kamilog: Customized Logging Output Module

This script provides a simple interface to obtain Python loggers with a
customized logging output format. The format includes timestamps and padded
log level names for cleaner, more uniform log display.





Installation as Script:
Copy the single script `./kamilog/kamilog.py` into your project folder.

Example directory structure::

    your_project/
    ├── kamilog.py
    └── main.py

In `main.py`, import the module as follows::

    import kamilog





Installation as Module:
Copy the entire `kamilog` folder into your project's source folder.

Example directory structure::

    your_project/
    ├── project_abc/
    │   ├── kamilog/
    │   │   ├── __init__.py
    │   │   └── kamilog.py
    │   ├── module_a/
    │   │   └── some_code.py
    │   └── module_b/
    │       └── other_code.py
    └── setup.py

Then you can import `kamilog` anywhere within the project like this::

    from project_abc import kamilog





Usage:
Use ``kamilog.getLogger()` (in places of `logging.getLogger()`)
to get a configured logger instance::

    import logging
    import kamilog

    my_logger = kamilog.getLogger("myLogger")
    my_logger.setLevel(logging.DEBUG)

    my_logger.debug("Debugging details here")
    my_logger.info("Informational message")
    my_logger.warning("Warning message")
    my_logger.error("Error occurred!")
    my_logger.critical("Critical issue!")

    try:
        1 / 0
    except ZeroDivisionError as err:
        my_logger.exception(err)

Output::

    [2024-06-15 14:30:00,000] DEBUG: Debugging details here
    [2024-06-15 14:30:00,000] INFO : Informational message
    [2024-06-15 14:30:00,000] WARN : Warning message
    [2024-06-15 14:30:00,001] ERROR: Error occurred!
    [2024-06-15 14:30:00,001] CRIT : Critical issue!
    [2024-06-15 14:30:00,001] ERROR: division by zero
    Traceback (most recent call last):
      File "/home/kami/repos/kami-log-py/example.py", line 18, in <module>
        1 / 0
        ~~^~~
    ZeroDivisionError: division by zero



verbosity and logging level:

Set up parser with options of `-v/--verbose` and `-q/--quiet`::

    from argparse import ArgumentParser

    parser = ArgumentParser()
    add_verbose_arguments(parser)

After parsing, set logging level of logger by verbosity of this parser::

    args = parser.parse_args()
    set_logging_level_by_verbosity(args)

Alternatively, calc the verbosity as a number::

    print(calc_verbosity(args))  # 1
"""

import logging
from logging import Formatter, StreamHandler

__version__ = "1.2.0"
__author__ = "kamiLeL"
__all__ = ("getLogger",)


# customized logger  ###########################################################

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

    _INITIALIZED_LOGGERS.append(name)

    return logger


# verbosity & logging level  ###################################################


def add_verbose_arguments(parser):
    """
    add -v/--verbose and -q/--quiet options to ``parser``


    :param parser:
    :type parser: argparse.ArgumentParser
    """
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="make verbose; each -v/--verbose increase verbosity value by 1",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="count",
        default=0,
        help="make quiet; each -q/--quiet decrease verbosity value by 1",
    )


def calc_verbosity(namespace):
    """
    calculate a **verbosity** value from --verbose &/ --quiet options
    contained in ``namespace``

    verbosity default to 0,
    each -v/--verbose flag will +1 to verbosity,
    each -q/--quiet flag will -1 to verbosity,
    no upper/lower bounds


    :param namespace: parsed from parser with --verbose & --quiet options
    :type namespace: argparse.Namespace
    :return: verbosity number
    :rtype: int
    """
    verbosity = 0

    if hasattr(namespace, "verbose"):
        verbosity += namespace.verbose
    if hasattr(namespace, "quiet"):
        verbosity -= namespace.quiet

    return verbosity


def set_logging_level_by_verbosity(namespace, logger_name=None):
    """
    set **logging level** of a logger based on *verbosity* calculated
    from --verbose &/ --quiet options contained in ``namespace``

    - ``-vv`` (or more): DEBUG
    - ``-v``: INFO
    - no option: WARNING
    - ``-q`` (or more): all message suppressed, even CRITICAL


    :param namespace: parsed from parser with --verbose &/ --quiet
    :type namespace: argparse.Namespace
    :param logger_name: set specific logger with this name
            defaults to None, set root logger
    :type logger_name: str, optional
    """
    verbosity = calc_verbosity(namespace)

    if verbosity >= 2:
        level = logging.DEBUG
    elif verbosity == 1:
        level = logging.INFO
    elif verbosity == 0:
        level = logging.WARNING
    else:
        level = logging.CRITICAL + 1

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
