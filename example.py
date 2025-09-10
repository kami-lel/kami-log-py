#!/usr/bin/env python3
# todo docstring

import logging

a = logging.getLogger("hi")
a.setLevel(logging.DEBUG)

if __name__ == "__main__":
    a.debug("debug")
    a.info("info")
    a.critical("crit")
    pass
