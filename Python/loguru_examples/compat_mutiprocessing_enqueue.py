# Linux implementation
import multiprocessing
from loguru import logger


def my_process():
    logger.info("Executing function in child process")
    logger.complete()


if __name__ == "__main__":
    logger.add("file.log", enqueue=True)

    process = multiprocessing.Process(target=my_process)
    process.start()
    process.join()

    logger.info("Done")
