async def first() -> int:
    return 1


def second():  # How can we call `first()` from here?
    return first() + 1  # Boom! Don't do this. We illustrate a problem here.


from returns.future import Future


def second() -> Future[int]:
    return Future(first()).map(lambda num: num + 1)


import asyncio  # or asyncio, or any other lib

# We can then pass our `Future` to any library: asyncio, trio, curio.
# And use any event loop: regular, uvloop, even a custom one, etc
assert asyncio.run(second().awaitable) == 2

import anyio
from returns.future import future_safe
from returns.io import IOFailure

@future_safe
async def raising():
    raise ValueError('Not so fast!')

ioresult = anyio.run(raising.awaitable)  # all `Future`s return IO containers
assert ioresult == IOFailure(ValueError('Not so fast!'))  # True

async def fetch_user(user_id: int) -> 'User':
    ...

async def get_user_permissions(user: 'User') -> 'Permissions':
    ...

async def ensure_allowed(permissions: 'Permissions') -> bool:
    ...

async def main(user_id: int) -> bool:
    # Also, don't forget to handle all possible errors with `try / except`!
    user = await fetch_user(user_id)  # We will await each time we use a coro!
    permissions = await get_user_permissions(user)
    return await ensure_allowed(permissions)

import anyio
from returns.future import FutureResultE, future_safe
from returns.io import IOSuccess, IOFailure

@future_safe
async def fetch_user(user_id: int) -> 'User':
    ...

@future_safe
async def get_user_permissions(user: 'User') -> 'Permissions':
    ...

@future_safe
async def ensure_allowed(permissions: 'Permissions') -> bool:
    ...

def main(user_id: int) -> FutureResultE[bool]:
    # We can now turn `main` into a sync function, it does not `await` at all.
    # We also don't care about exceptions anymore, they are already handled.
    return fetch_user(user_id).bind(get_user_permissions).bind(ensure_allowed)

correct_user_id: int  # has required permissions
banned_user_id: int  # does not have required permissions
wrong_user_id: int  # does not exist

# We can have correct business results:
assert anyio.run(main(correct_user_id).awaitable) == IOSuccess(True)
assert anyio.run(main(banned_user_id).awaitable) == IOSuccess(False)

# Or we can have errors along the way:
assert anyio.run(main(wrong_user_id).awaitable) == IOFailure(
    UserDoesNotExistError(...),
)

from returns.pointfree import bind
from returns.pipeline import flow

def main(user_id: int) -> FutureResultE[bool]:
    return flow(
        fetch_user(user_id),
        bind(get_user_permissions),
        bind(ensure_allowed),
    )
