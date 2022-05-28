from loguru import logger

logger.level("foobar", no=33, icon="🤖", color="<blue>")

logger.log("foobar", "A message")

from functools import partialmethod

logger.__class__.foobar = partialmethod(logger.__class__.log, "foobar")

logger.foobar("A message")
