"""Define and setup Logger-Instances.

todo: add colors (see: https://github.com/healkeiser/fxlog/blob/main/fxlog/fxlogger.py#L57)

"""

import logging
import os

LOG_FORMAT = "%(name)s %(levelname)s [%(funcName)s] %(message)s"
"""str: Format to be used for log messages."""


logger = logging.getLogger("🌀")
"""The logger to log logging related log messages."""

formatter = logging.Formatter(LOG_FORMAT)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

if os.getenv("DEBUG"):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
