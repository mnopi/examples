import datetime
import functools
import pickle
import sys

from icecream import ic


def serialized():
    # Want your logs to be serialized for easier parsing or to pass them around? Using the serialize argument,
    # each log message will be converted to a JSON string before being sent to the configured sink.
    from loguru import logger as logger

    def add_task(record):
        ic(record)

    logger.add(add_task, serialize=True)
    print()


def binding():
    # Using bind() you can contextualize your logger messages by modifying the extra record attribute.
    from loguru import logger as logger
    i = logger.add("file.log", format="{extra[ip]} {extra[user]} {message}")
    context_logger = logger.bind(ip="192.168.0.1", user="someone")
    context_logger.info("Contextualize your logger easily")
    context_logger.bind(user="someone_else").info("Inline binding of extra attribute")
    context_logger.info("Use kwargs to add context during formatting: {user}", user="anybody")
    logger.remove(i)
    print()


def context():
    # It is possible to modify a context-local state temporarily with contextualize():
    from loguru import logger as logger
    i = logger.add(sys.stderr, format="{message} | {extra}")

    logger.level("FINISH", no=41, color="<blue>", icon="🐍")

    def task():
        logger.trace('Processing Task')

    def contextualize(task_number):
        with logger.contextualize(task_id=task_number):
            # crea un nuevo context.
            logger.info("Start Task")
            task()
            logger.success("End Task")

    def run_tasks():
        logger.info("Start Tasks")
        for t in range(0, 4):
            contextualize(t)
        logger.log('FINISH', "End Tasks")

    run_tasks()
    logger.remove(i)
    print()


def bind_filter():
    # You can also have more fine-grained control over your logs by combining bind() and filter:
    from loguru import logger as logger

    i = logger.add("special.log", filter=lambda record: "special" in record["extra"])
    logger.debug("This message is not logged to the file")
    logger.bind(special=True).info("This message, though, is logged to the file!")
    logger.remove(i)
    print()


def extra_ip():
    from loguru import logger as logger
    i = logger.add(sys.stderr, format="<lg>{extra[ip]}</>: {message}")
    logger.info('Start', ip='2.2.2.2')
    logger.info('Finish', ip='2.2.2.2')
    logger.remove(0)
    logger.info('Start', ip='8.8.8.8')
    logger.info('Finish', ip='8.8.8.8')
    logger.remove(i)
    print()


def patch_utc():
    # Finally, the patch() method allows dynamic values to be attached to the record dict of each new message:
    from loguru import logger as logger
    i = logger.add(sys.stderr, format="<lr>{extra[utc]}</> {message}")
    logger = logger.patch(lambda record: record["extra"].update(utc=datetime.datetime.utcnow()))
    logger.info('Dynamic UTC 1')
    logger.info('Dynamic UTC 2')
    logger.remove(i)
    print()


def patch_decorator():
    from loguru import logger as logger

    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger.patch(lambda record: record.update(function=func.__name__)).info("Wrapped!")
            return func(*args, **kwargs)
        return wrapped

    @wrapper
    def patch_test():
        logger.info('patch test')

    patch_test()
    print()


def patch_level_message():
    from loguru import logger as logger

    def recv_record_from_network(pipe):
        info = pipe if isinstance(pipe, dict) else pickle.loads(pipe.read())
        level, message = info["level"], info["message"]
        logger.patch(lambda record: record.update(record)).log(level, message)
        logger.success('patched')
    recv_record_from_network(dict(level='SUCCESS', message='network'))
    print()


if __name__ == '__main__':
    binding()
    context()
    bind_filter()
    extra_ip()
    patch_utc()
    patch_decorator()
    patch_level_message()
