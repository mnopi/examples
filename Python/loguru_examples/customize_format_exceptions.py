from loguru import logger


def inverse(x):
    try:
        1 / x
    except ZeroDivisionError:
        logger.exception("Oups...")


if __name__ == "__main__":
    inverse(0)
