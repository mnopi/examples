import random
import datetime as dt
from typing import Callable

from returns.io import impure
from returns.io import IO


def get_random_number() -> IO[int]:  # or use `@impure` decorator
    return IO(random.randint(1, 10))  # isn't pure, because random


now: Callable[[], IO[dt.datetime]] = impure(dt.datetime.now)

@impure
def return_and_show_next_number(previous: int) -> int:
    next_number = previous + 1
    print(next_number)  # isn't pure, because does IO
    return next_number


import requests
from returns.io import IOResult, impure_safe
from returns.result import safe
from returns.pipeline import flow
from returns.pointfree import bind_result

def fetch_user_profile(user_id: int) -> IOResult['UserProfile', Exception]:
    """Fetches `UserProfile` TypedDict from foreign API."""
    return flow(
        user_id,
        _make_request,
        # before: def (Response) -> UserProfile
        # after safe: def (Response) -> ResultE[UserProfile]
        # after bind_result: def (IOResultE[Response]) -> IOResultE[UserProfile]
        bind_result(_parse_json),
    )

@impure_safe
def _make_request(user_id: int) -> requests.Response:
    response = requests.get('/api/users/{0}'.format(user_id))
    response.raise_for_status()
    return response

@safe
def _parse_json(response: requests.Response) -> 'UserProfile':
    return response.json()
