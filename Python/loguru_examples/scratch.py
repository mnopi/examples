import datetime
import functools
import math
import pickle
import random
import sys
from os import environ

from icecream import ic
from loguru import logger
environ['LOGURU_INFO_COLOR'] = "<light-green><normal>"  # <Fore><Style>

logger.debug("1. That's it, beautiful and simple logging!")
logger.info("2. That's it, beautiful and simple logging!")  # No resetea el color
print('Ahora saldrán dos mensajes de INFO en CONSOLE')
logger.add(sys.stderr, format="{level} {message}", level="INFO", colorize='<le><i>')
print('hola')
logger.debug("3. That's it, beautiful and simple logging!")
from loguru._logger import Level
new_level = Level(name='SPAM', no=5, color='<le><i>', icon=None)
print('# Ahora saldrán en fichero los de formato inicial no el sink añadido antes')
file_sink_id = logger.add("file_{time}.log")
logger.debug("4. That's it, beautiful and simple logging!")
# environ['LOGURU_INFO_COLOR'] = "<light-green><normal>"  # <Fore><Style>
logger.info("5. That's it, beautiful and simple logging!")
logger.remove(file_sink_id)
file_sink_id = logger.add("file_3.log", rotation="1 day", retention='1 week')  # Once the file is too old, it's rotated
logger.info("<red>6</>. That's it, beautiful and simple logging!", extra=dict(extra1=1, extra2=2),
            function='_function', line=1, name='_name', module='_module', process='_process', thread='_thread',
            file='_file', exception=Exception('_Exception'))
logger.remove(file_sink_id)

logger.add(sys.stdout, format="{time} - {level} - {message}", filter="sub.module")


def debug_only(record):
    return record["level"].name == "DEBUG"


logger.add("debug.log", filter=debug_only)  # Other levels are filtered out


def my_sink(message):
    def update_db(message, time, level):
        ic(message, time, level)
    record = message.record
    update_db(message, time=record["time"], level=record["level"])


logger.add(my_sink)

level_per_module = {
    "": "DEBUG",
    "third.lib": "WARNING",
    "anotherlib": False
}
logger.add(lambda m: print(m, end=""), filter=level_per_module, level=0)


async def publish(message):
    await api.post(message)

logger.add(publish, serialize=True)

from logging import StreamHandler
logger.add(StreamHandler(sys.stderr), format="{message}")


class RandomStream:
    def __init__(self, seed, threshold):
        self.threshold = threshold
        random.seed(seed)

    def write(self, message):
        if random.random() > self.threshold:
            print(message)


stream_object = RandomStream(seed=12345, threshold=0.25)
logger.add(stream_object, level="INFO")

try:
    1 / 0
except ZeroDivisionError:
   logger.opt(exception=True).debug("Exception logged with debug level:")

logger.opt(record=True).info("Current line is: {record[line]}")
logger.opt(lazy=True).debug("If sink <= DEBUG: {x}", x=lambda: math.factorial(2**5))

logger.opt(colors=True).warning("We got a <red>BIG</red> problem")

logger.opt(raw=True).debug("No formatting\n")

logger.opt(capture=False).info("Displayed but not captured: {value}", value=123)


def wrapped():
    logger.opt(depth=1).info("Get parent context")


def func():
    wrapped()


func()


def wrapper(func):
    @functools.wraps(func)

    def wrapped(*args, **kwargs):
        logger.patch(lambda r: r.update(function=func.__name__)).info("Wrapped!")
        return func(*args, **kwargs)
    return wrapped


def recv_record_from_network(pipe):
    record = pickle.loads(pipe.read())
    level, message = record["level"], record["message"]
    logger.patch(lambda r: r.update(record)).log(level, message)


level = logger.level("ERROR")
print(level)

logger.add(sys.stderr, format="{level.no} {level.icon} {message}")

logger.level("CUSTOM", no=15, color="<blue>", icon="@")

logger.log("CUSTOM", "Logging...")

logger.level("WARNING", icon="@")

logger.warning("Updated!")

logger.info("Allowed message by default")

logger.disable("my_library")
logger.info("While publishing a library, don't forget to disable logging")

logger.disable("__main__")
logger.info("Disabled, so nothing is logged.")
logger.enable("__main__")
logger.info("Re-enabled, messages are logged.")

logger.configure(
    handlers=[
        dict(sink=sys.stderr, format="[{time}] {message}"),
        dict(sink="file.log", enqueue=True, serialize=True),
    ],
    levels=[dict(name="NEW", no=13, icon="¤", color="")],
    extra={"common_to_all": "default"},
    patcher=lambda record: record["extra"].update(some_value=42),
    activation=[("my_module.secret", False), ("another_library.module", True)],
)

# Set a default "extra" dict to logger across all modules, without "bind()"
extra = {"context": "foo"}
logger.configure(extra=extra)
logger.add(sys.stderr, format="{extra[context]} - {message}")
logger.info("Context without bind")
# => "foo - Context without bind"
logger.bind(context="bar").info("Suppress global context")
# => "bar - Suppress global context"

reg = r"(?P<lvl>[0-9]+): (?P<msg>.*)"    # If log format is "{level.no} - {message}"
for e in logger.parse("file.log", reg):  # A file line could be "10 - A debug message"
    print(e)                             # => {'lvl': '10', 'msg': 'A debug message'}


caster = dict(lvl=int)                   # Parse 'lvl' key as an integer
for e in logger.parse("file.log", reg, cast=caster):
    print(e)                             # => {'lvl': 10, 'msg': 'A debug message'}


def cast(groups):
    if "date" in groups:
        groups["date"] = datetime.datetime.strptime(groups["date"], "%Y-%m-%d %H:%M:%S")


with open("file.log") as file:
    for log in logger.parse(file, reg, cast=cast):
        print(log["date"], log["something_else"])


import time

from loguru import logger
from tqdm import tqdm

logger.remove()
logger.add(lambda msg: tqdm.write(msg, end=""))

logger.info("Initializing")

for x in tqdm(range(100)):
    logger.info("Iterating #{}", x)
    time.sleep(0.1)


from loguru import logger


def task_A():
    logger_a = logger.bind(task="A")
    logger_a.info("Starting task A")
    do_something()
    logger_a.success("End of task A")


def task_B():
    logger_b = logger.bind(task="B")
    logger_b.info("Starting task B")
    do_something_else()
    logger_b.success("End of task B")


logger.add("file_A.log", filter=lambda record: record["extra"]["task"] == "A")
logger.add("file_B.log", filter=lambda record: record["extra"]["task"] == "B")

task_A()
task_B()

import copy
from loguru import logger


def task(task_id, logger):
    logger.info("Starting task {}", task_id)
    
    do_something(task_id)
    logger.success("End of task {}", task_id)


logger.remove()

for task_id in ["A", "B", "C", "D", "E"]:
    logger_ = copy.deepcopy(logger)
    logger_.add("file_%s.log" % task_id)
    task(task_id, logger_)
