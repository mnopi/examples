import contextlib
import sys
from loguru import logger


class StreamToLogger:

    def __init__(self, level="INFO"):
        self._level = level

    def write(self, buffer):
        for line in buffer.rstrip().splitlines():
            logger.opt(depth=1).log(self._level, line.rstrip())

    def flush(self):
        pass


logger.remove()
logger.add(sys.__stdout__)

stream = StreamToLogger()
with contextlib.redirect_stdout(stream):
    print("Standard output is sent to added handlers.")


# You may also capture warnings emitted by your application by replacing warnings.showwarning():
import warnings
from loguru import logger

showwarning_ = warnings.showwarning


def showwarning(message, *args, **kwargs):
    logger.warning(message)
    showwarning_(message, *args, **kwargs)


warnings.showwarning = showwarning


