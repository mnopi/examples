import sys

import stackprinter
from loguru import logger


def format(record):
    format_ = "{time} {message}\n"

    if record["exception"] is not None:
        record["extra"]["stack"] = stackprinter.format(record["exception"])
        format_ += "{extra[stack]}\n"

    return format_


logger.add(sys.stderr, format=format)
