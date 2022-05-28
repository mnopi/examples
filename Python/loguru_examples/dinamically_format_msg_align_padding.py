# The default formatter is unable to vertically align log messages because the length of {name}, {function} and {
# line} are not fixed.
#
# One workaround consists of using padding with some maximum value that should suffice most of the time,
# like this for example:
import sys

from loguru import logger

fmt = "{time} | {level: <8} | {name: ^15} | {function: ^15} | {line: >3} | {message}"
logger.add(sys.stderr, format=fmt)
logger.info('Align Padding - Manual')


# Others solutions are possible by using a formatting function or class. For example, it is possible to dynamically
# adjust the padding length based on previously encountered values:
class Formatter:

    def __init__(self):
        self.padding = 0
        self.fmt = "{time} | {level: <8} | {name}:{function}:{line}{extra[padding]} | {message}\n{exception}"

    def format(self, record):
        length = len("{name}:{function}:{line}".format(**record))
        self.padding = max(self.padding, length)
        record["extra"]["padding"] = " " * (self.padding - length)
        return self.fmt


formatter = Formatter()

logger.remove()
logger.add(sys.stderr, format=formatter.format)
logger.info('Align Padding - Automatic')
