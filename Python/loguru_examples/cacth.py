from loguru import logger


@logger.catch
def f(x):
    return 100 / x


def g():
    f(10)


f(0)
g()
