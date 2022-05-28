import asyncio
import multiprocessing
import sys

from loguru import logger


async def sink(message):
    await asyncio.sleep(0.1)  # IO processing...
    print(message, end="")


async def work():
    logger.info("Start")
    logger.info("End")
    await logger.complete()


logger.add(sink)
asyncio.run(work())


def process():
    logger.info("Message sent from the child")
    logger.complete()


logger.add(sys.stderr, enqueue=True)
process = multiprocessing.Process(target=process)
process.start()
process.join()
