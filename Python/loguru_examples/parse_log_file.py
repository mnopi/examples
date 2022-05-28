from datetime import datetime

from loguru import logger
reg = r"(?P<lvl>[0-9]+): (?P<msg>.*)"  # If log format is "{level.no} - {message}"
for e in logger.parse("file.log", reg):  # A file line could be "10 - A debug message"
    print(e)  # => {'lvl': '10', 'msg': 'A debug message'}

caster = dict(lvl=int)  # Parse 'lvl' key as an integer
for e in logger.parse("file.log", reg, cast=caster):
    print(e)  # => {'lvl': 10, 'msg': 'A debug message'}


def cast(groups):
    if "date" in groups:
        groups["date"] = datetime.strptime(groups["date"], "%Y-%m-%d %H:%M:%S")


with open("file.log") as file:
    for log in logger.parse(file, reg, cast=cast):
        print(log["date"], log["something_else"])


pattern = r"(?P<time>.*) - (?P<level>[0-9]+) - (?P<message>.*)"  # Regex with named groups
