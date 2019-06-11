import json
import requests
from requests import HTTPError
from urllib.parse import urlunparse, ParseResult, urlencode


DEFAULT_SCHEME = "http"


class StackStatus:
    ERROR = 'error'
    ENQUEUED = 'enqueued'
    PUSHED = 'pushed'
    PROCESSING = 'processing'


class BuilderApiError(Exception):
    pass


def raise_builder_api_error(func):
    def wrapped_func(*args):
        try:
            return func(*args)
        except HTTPError as e:
            raise BuilderApiError(f"Response is not ok: {e} in function {func}")
        except (ConnectionRefusedError, requests.exceptions.ConnectionError) as e:
            raise BuilderApiError(e)
    return wrapped_func


class BuilderApi:
    def __init__(self, hostport, token):
        self.hostport = hostport
        self.token = token

    def get_url(self, path: str):
        parse_result = ParseResult(DEFAULT_SCHEME, self.hostport, path, "", "", "")
        return urlunparse(parse_result)

    @raise_builder_api_error
    def upload_stack(self, name, data):
        url = self.get_url(f"/stacks/upload/{name}")
        r = requests.put(
            url,
            data=data,
            headers={
                'Content-Type': 'application/zip',
            },
            params={'file': name}
        )
        r.raise_for_status()

    @raise_builder_api_error
    def get_stack(self, name):
        url = self.get_url(f"/stacks/{name}")
        r = requests.get(
            url,
        )
        r.raise_for_status()
        stacks = json.loads(r.content)
        if stacks:
            return stacks[0]

    @raise_builder_api_error
    def list_stacks(self):
        url = self.get_url(f"/stacks/")
        r = requests.get(
            url,
        )
        r.raise_for_status()
        return json.loads(r.content)
