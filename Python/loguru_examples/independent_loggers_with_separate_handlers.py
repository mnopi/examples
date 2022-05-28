import copy

from icecream import ic
from loguru import logger


def task_A():
    def do_something():
        ic(task_A, do_something)
    logger_a = logger.bind(task="A")
    logger_a.info("Starting task A")
    do_something()
    logger_a.success("End of task A")


def task_B():
    def do_something_else():
        ic(task_A, do_something_else)
    logger_b = logger.bind(task="B")
    logger_b.info("Starting task B")
    do_something_else()
    logger_b.success("End of task B")


logger.add("file_A.log", filter=lambda record: record["extra"]["task"] == "A")
logger.add("file_B.log", filter=lambda record: record["extra"]["task"] == "B")

task_A()
task_B()

# Now, supposing that you have a lot of these tasks. It may be a bit cumbersome to configure every handlers like this.
# Most importantly, it may unnecessarily slow down your application as each log will need to be checked by the
# filter function of each handler. In such case, it is recommended to rely on the copy.deepcopy() built-in method
# that will create an independent logger object. If you add a handler to a deep copied logger, it will not be
# shared with others functions using the original logger:


def task(t_id, l):
    def do_something(tid):
        ic(task, do_something, tid)
    l.info("Starting task {}", t_id)
    do_something(t_id)
    logger.success("End of task {}", t_id)


logger.remove()


for task_id in ["A", "B", "C", "D", "E"]:
    logger_ = copy.deepcopy(logger)
    logger_.add("file_%s.log" % task_id)
    task(task_id, logger_)
