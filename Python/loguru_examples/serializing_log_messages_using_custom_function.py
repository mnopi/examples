import json
import sys

from loguru import logger


def serialize(record):
    subset = {"timestamp": record["time"].timestamp(), "message": record["message"]}
    return json.dumps(subset)


def sink(message):
    serialized = serialize(message.record)
    print(serialized)


i = logger.add(sink)

logger.info('Serial')

# If you need to send structured logs to a file (or any kind of sink in general), a similar result can be obtained by
# using a custom format function:

logger.remove(i)


def formatter(record):
    # Note this function returns the string to be formatted, not the actual message to be logged
    record["extra"]["serialized"] = serialize(record)
    return "{extra[serialized]}\n"


i = logger.add("serial_formatter.json", format=formatter)

logger.info('Serial & Formatter')


# You can also use patch() for this, so the serialization function will be called only once in case you want to use
# it in multiple sinks:
#
def patching(record):
    record["extra"]["serialized"] = serialize(record)


logger.remove(i)

logger = logger.patch(patching)

# Note that if "format" is not a function, possible exception will be appended to the message
logger.add(sys.stderr, format="{extra[serialized]}")
logger.add("serial_patching.json", format="{extra[serialized]}")

def serialize_record(record):
    print(record)
    return json.dumps(record['message'])

logger.add("serial.json", enqueue=True,
             backtrace=True, diagnose=True, format=None, level='DEBUG', retention='5 days',
             rotation='500 MB', serialize=serialize_record, compression='zip')

logger.info('Serial & Patching')
