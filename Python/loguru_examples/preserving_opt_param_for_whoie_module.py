from loguru import logger

logger = logger.opt(colors=True)

logger.info("It <green>works</>!")


# However, it should be noted that it’s not possible to chain opt() calls, using this method again will reset the
# colors option to its default value (which is False). For this reason, it is also necessary to patch the opt()
# method so that all subsequent calls continue to use the desired value:

from functools import partial

logger = logger.opt(colors=True)
logger.opt = partial(logger.opt, colors=True)

logger.opt(raw=True).info("It <green>still</> works!\n")
