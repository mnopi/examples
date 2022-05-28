from icecream import ic
from loguru import logger


def print_logger(l=logger):
    options = dict(zip(('exception', 'depth', 'record', 'lazy', 'colors', 'raw', 'capture', 'patcher', 'extra'),
                       l._options))
    ic(l,
       l._core.__getstate__(),
       options)


def print_enabled(l=logger):
    ic(l._core.enabled)


def print_extra(l=logger):
    ic(l._core.extra)


def print_handlers(l=logger):
    ic(l._core.handlers)


def print_level(l=logger, name='DEBUG'):
    ic(l.level(name))


def print_levels(l=logger):
    ic(l._core.levels)


def print_min_level(l=logger):
    ic(l._core.min_level)


if __name__ == '__main__':
    print_logger()
