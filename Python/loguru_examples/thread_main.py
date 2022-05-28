# main.py
from multiprocessing import Pool
from loguru import logger
import thread_worker_a
import thread_worker_b


if __name__ == "__main__":
    logger.remove()
    logger.add("file.log", enqueue=True)
    print(1)
    worker = thread_worker_a.Worker()
    with Pool(4, initializer=worker.set_logger, initargs=(logger, )) as pool:
        resuts = pool.map(worker.work, [1, 10, 100])
    print(2)

    with Pool(4, initializer=thread_worker_b.set_logger, initargs=(logger, )) as pool:
        results = pool.map(thread_worker_b.work, [1, 10, 100])
    print(3)

    logger.info("Done")
