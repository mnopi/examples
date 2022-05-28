import sys

from icecream import ic
from loguru import logger


def int_level():
    ic(int_level)
    number = logger.add(sys.stderr, format="{level.name} -> {level.no} -> {message}", colorize=False)
    logger.log(28, int_level.__name__)
    logger.remove(number)


def str_level():
    ic(str_level)
    number = logger.add(sys.stderr, format="{level.name} -> {level.no} -> {message}", colorize=False)
    logger.log("DEBUG", str_level.__name__)
    logger.remove(number)


def add_level():
    name = "L3V3L"
    icon = "[o]"
    level = 3

    logger.level(name, level, color="<red>", icon=icon)
    fmt = "<level>{level.name}</level> {level.no} <lg>{message}</>"
    number = logger.add(sys.stderr, format=fmt, colorize=True)

    logger.log(name, add_level.__name__)
    logger.remove(number)


def add_level_existing_fmt():
    name = "L4V4L"
    icon = "[o]"
    level = 4

    lvl = logger.level(name, level, color="<red>", icon=icon)
    fmt = "<level>{level.name}</level> {level.no} <lg>{message}</>"
    number = logger.add(sys.stderr, format=fmt, colorize=True)

    logger.log(name, add_level.__name__)
    logger.remove(number)


int_level()
str_level()
add_level()
