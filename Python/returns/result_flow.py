import requests
from returns.result import Result, safe
from returns.pipeline import flow
from returns.pointfree import bind

def fetch_user_profile_original(user_id: int) -> 'UserProfile':
    """Fetches UserProfile dict from foreign API."""
    response = requests.get('/api/users/{0}'.format(user_id))

    # What if we try to find user that does not exist?
    # Or network will go down? Or the server will return 500?
    # In this case the next line will fail with an exception.
    # We need to handle all possible errors in this function
    # and do not return corrupt data to consumers.
    response.raise_for_status()

    # What if we have received invalid JSON?
    # Next line will raise an exception!
    return response.json()

def fetch_user_profile(user_id: int) -> Result['UserProfile', Exception]:
    """Fetches `UserProfile` TypedDict from foreign API."""
    return flow(
        user_id,
        _make_request,
        bind(_parse_json),
    )


@safe
def _make_request(user_id: int) -> requests.Response:
    # TODO: we are not yet done with this example, read more about `IO`:
    response = requests.get('/api/users/{0}'.format(user_id))
    response.raise_for_status()
    return response


@safe
def _parse_json(response: requests.Response) -> 'UserProfile':
    return response.json()
