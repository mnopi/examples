import functools
import sys
from asyncio import iscoroutinefunction
from functools import cached_property
import sys
sys.path.append('/Users/jose/upins')
# noinspection PyUnresolvedReferences
from upins import getname
from loguru import logger

handler = logger.add(sys.stderr, format="{extra[ip]} - {message}")


class Server:

    def __init__(self, ip):
        self.ip = ip
        self.logger = logger.bind(ip=ip)

    def call(self, message):
        self.logger.info(message)


def server():
    instance_1 = Server("192.168.0.200")
    instance_2 = Server("127.0.0.1")
    instance_1.call("First instance")
    instance_2.call("Second instance")


logger.remove(handler)
print()
handler = logger.add(sys.stderr, format="{extra[repo]} - {message}")


def trackcache():
    trackcache.cache = {}

    def track(func):
        if func not in trackcache.cache:
            trackcache.cache[func] = dict(name=getname(func), coro=iscoroutinefunction(func))
        coro, name = trackcache.cache[func]['coro'], trackcache.cache[func]['name']

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            args[0].logger.patch(lambda record: record.update(function=name)).debug("Start!")
            rv = func(*args, **kwargs)
            args[0].logger.patch(lambda record: record.update(function=name)).debug("Finish!")
            return rv
        return wrapped
    return track


version = 1


class Repo:
    def __init__(self, name):
        self.repo = name
        self.logger = logger.bind(repo=name)
        self.logger.success(self.clean)
        for func in [self.add, self.commit, self.push, self.upload, self.upgrade]:
            func()
        self.logger.success(self.version)

    @cached_property
    @trackcache()
    def clean(self):
        self.logger.info('OK')
        return version

    @trackcache()
    def add(self):
        self.logger.info('OK')

    @trackcache()
    def commit(self):
        self.logger.info('OK')

    @trackcache()
    def push(self):
        self.logger.info('OK')

    @trackcache()
    def upload(self):
        self.logger.info('OK')

    @trackcache()
    def upgrade(self):
        self.logger.info('OK')

    @property
    @trackcache()
    def version(self):
        self.logger.info('OK')
        return version + 1


if __name__ == '__main__':
    with logger.catch():
        server()
        list(map(Repo, ['bapy', 'pen']))
