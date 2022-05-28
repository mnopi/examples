import sys

from loguru import logger
logger.info("2. That's it, beautiful and simple logging!")  # No resetea el color

# https://loguru.readthedocs.io/en/stable/overview.html#no-handler-no-formatter-no-filter-one-function-to-rule-them-all

logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")


logger.opt(exception=True).debug("Debug error:")
