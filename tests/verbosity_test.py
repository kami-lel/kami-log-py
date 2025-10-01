"""
tests function related to verbosity & logging level

ie
add_verbose_arguments, calc_verbosity, set_logging_level_by_verbosity
"""

from argparse import ArgumentParser
import sys
import os
from logging import getLogger

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
from kamilog.kamilog import (
    add_verbose_arguments,
    calc_verbosity,
    set_logging_level_by_verbosity,
)

LOGGER_NAME = "VERBOSITY_TEST"

# sys.argv parser  #############################################################

sys_argv_parser = ArgumentParser()
add_verbose_arguments(sys_argv_parser)


if __name__ == "__main__":
    args = sys_argv_parser.parse_args()

    # test calc_verbosity
    verbosity = calc_verbosity(args)
    print("verbosity:\t{}".format(verbosity))

    # test set_logging_level_by_verbosity
    set_logging_level_by_verbosity(args, LOGGER_NAME)

    logger = getLogger(LOGGER_NAME)
    print("logging level:\t{}".format(logger.level))
