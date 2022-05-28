import sys

from loguru import logger
from logger_inspect import print_logger, print_enabled, print_extra, print_handlers, \
    print_level, print_levels, print_min_level

# The record is just a Python dict, accessible from sinks by ``message.record``. It contains
#         all contextual information of the logging call (time, function, file, line, level, etc.).
# Each of its key can be used in the handler's ``format`` so the corresponding value is
#         properly displayed in the logged message (e.g. ``"{level}"`` -> ``"INFO"``). Some record's
#         values are objects with two or more attributes, these can be formatted with ``"{key.attr}"``
#         (``"{key}"`` would display one by default). `Formatting directives`_ like ``"{key: >3}"``
#         also works and is particularly useful for time (see below).
# logger.opt(record=True).info("Current line is: {record[line]}")
# logger.add(sys.stderr, format="{extra[ip]} - {message}")
# logger.add(sys.stderr, format="{message} | {extra}")
logger.configure(
    # backtrace: exception trace formatted should be extended upward to show the full stacktrace
    # colorize: strip and converting color markups to ansi or stripped. (default: automatic tty or not)
    # diagnose: expands exception vars.
    # enqueue: first pass through a multiprocess-safe queue before sink. Useful for file, logging calls non-blocking.
    # serialize: to json string before going to sink.
    #
    # SINK: Coroutine
    # ---------------
    # loop: optional
    #
    # SINK: File Path
    # ---------------
    # rotation, retention, compression, delay, mode, buffering, encoding.
    #

    handlers=[
        dict(sink=sys.stderr, format="[{time}] {message}", backtrace=True, diagnose=True),
        dict(sink="file.log", enqueue=True, serialize=True, backtrace=True, diagnose=True),
    ],
    levels=[dict(name="NEW", no=13, icon="¤", color="")],
    extra={"common_to_all": "default"},
    patcher=lambda record: record["extra"].update(some_value=42),
    activation=[("my_module.secret", False), ("another_library.module", True)],
)

# Using the logger in your scripts is easy, and you can configure() it at start. To use Loguru from inside a library,
# remember to never call add() but use disable() instead so logging functions become no-op. If a developer wishes
# to see your library’s logs, he can enable() it again.


